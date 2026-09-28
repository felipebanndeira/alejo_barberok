from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash
from werkzeug.security import check_password_hash
import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from core.db import get_db
from core.auth import login_required

admin_bp = Blueprint('admin', __name__)

# Postgres timezone used for all localtime conversions
_TZ = 'America/Argentina/Buenos_Aires'
ARG_TZ = ZoneInfo(_TZ)

def now_arg():
    return datetime.now(ARG_TZ)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = %s', (username,)).fetchone()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('admin.dashboard'))
            
        flash('Credenciales incorrectas')
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('admin.login'))

@admin_bp.route('/')
@login_required
def dashboard():
    db = get_db()
    current_time_arg = now_arg()
    today = current_time_arg.strftime('%Y-%m-%d')
    
    # Shift logic
    last_reset_str = db.execute("SELECT value FROM settings WHERE key='last_reset_date'").fetchone()
    last_reset = last_reset_str[0] if last_reset_str else '2000-01-01 00:00:00'
    first_of_month = current_time_arg.strftime('%Y-%m-01 00:00:00')
    # Evitar desfasajes si last_reset tiene hora futura por UTC
    if last_reset > current_time_arg.strftime('%Y-%m-%d %H:%M:%S'):
        last_reset = first_of_month
    start_datetime = max(last_reset, first_of_month)
    
    # Metrics
    appointments_today = db.execute(
        "SELECT COUNT(*) FROM appointments WHERE date = %s AND status != 'cancelled'",
        (today,)
    ).fetchone()[0]
    total_clients = db.execute("SELECT COUNT(DISTINCT client_phone) FROM appointments").fetchone()[0]
    
    caja_app = db.execute(
        f"SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id"
        f" WHERE (a.confirmed_at AT TIME ZONE '{_TZ}') >= %s"
        f" AND (a.confirmed_at AT TIME ZONE '{_TZ}') <= %s"
        f" AND a.status = 'confirmed'",
        (start_datetime, today + ' 23:59:59')
    ).fetchone()[0] or 0

    sales_today = db.execute(
        f"SELECT * FROM sales WHERE (created_at AT TIME ZONE '{_TZ}') >= %s",
        (start_datetime,)
    ).fetchall()
    caja_sales = sum(s['price'] for s in sales_today)
    caja_total = caja_app + caja_sales

    expenses_today = db.execute(
        f"SELECT * FROM expenses WHERE (created_at AT TIME ZONE '{_TZ}') >= %s",
        (start_datetime,)
    ).fetchall()
    gastos_total = sum(e['amount'] for e in expenses_today)

    caja_hoy = f"{caja_total:g}".replace('.', ',') if caja_total < 1000 else f"{caja_total:,.0f}".replace(',', '.')
    gastos_hoy_str = f"{gastos_total:g}".replace('.', ',') if gastos_total < 1000 else f"{gastos_total:,.0f}".replace(',', '.')
    
    net_profit = caja_total - gastos_total
    net_profit_str = f"{net_profit:g}".replace('.', ',') if abs(net_profit) < 1000 else f"{net_profit:,.0f}".replace(',', '.')

    # Chart 7 days
    chart_labels = []
    chart_data = []
    for i in range(6, -1, -1):
        d = now_arg() - timedelta(days=i)
        d_str = d.strftime('%Y-%m-%d')
        chart_labels.append(['Dom','Lun','Mar','Mie','Jue','Vie','Sab'][int(d.strftime('%w'))])
        inc_app = db.execute(
            f"SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id"
            f" WHERE a.date = %s AND (a.confirmed_at AT TIME ZONE '{_TZ}') >= %s AND a.status = 'confirmed'",
            (d_str, start_datetime)
        ).fetchone()[0] or 0
        inc_sales = db.execute(
            f"SELECT SUM(price) FROM sales"
            f" WHERE (created_at AT TIME ZONE '{_TZ}')::date = %s"
            f" AND (created_at AT TIME ZONE '{_TZ}') >= %s",
            (d_str, start_datetime)
        ).fetchone()[0] or 0
        chart_data.append(inc_app + inc_sales)
    
    schedule = db.execute('''
        SELECT a.id, a.client_name, a.client_phone, a.date, a.time, a.status, s.name as service_name 
        FROM appointments a
        JOIN services s ON a.service_id = s.id
        WHERE a.date >= %s AND a.status != 'cancelled'
        ORDER BY a.date ASC, a.time ASC
        LIMIT 50
    ''', (today,)).fetchall()
    
    services = db.execute('SELECT * FROM services').fetchall()
    settings = dict(db.execute('SELECT key, value FROM settings').fetchall())
    
    return render_template('admin/dashboard.html', 
                           appointments_today=appointments_today, 
                           total_clients=total_clients, caja_hoy=caja_hoy,
                           gastos_hoy=gastos_hoy_str, net_profit=net_profit_str,
                           chart_labels=chart_labels, chart_data=chart_data,
                           schedule=schedule, settings=settings, sales=sales_today, expenses=expenses_today, services=services)

@admin_bp.route('/finances')
@login_required
def finances():
    db = get_db()
    current_time_arg = now_arg()
    today = current_time_arg.strftime('%Y-%m-%d')
    appointments_today = db.execute("SELECT COUNT(*) FROM appointments WHERE date = %s", (today,)).fetchone()[0]
    total_clients = db.execute("SELECT COUNT(DISTINCT client_phone) FROM appointments").fetchone()[0]
    
    # Shift logic
    last_reset_str = db.execute("SELECT value FROM settings WHERE key='last_reset_date'").fetchone()
    last_reset = last_reset_str[0] if last_reset_str else '2000-01-01 00:00:00'
    first_of_month = current_time_arg.strftime('%Y-%m-01 00:00:00')
    if last_reset > current_time_arg.strftime('%Y-%m-%d %H:%M:%S'):
        last_reset = first_of_month
    start_datetime = max(last_reset, first_of_month)

    caja_hoy_app = db.execute(
        f"SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id"
        f" WHERE (a.confirmed_at AT TIME ZONE '{_TZ}') >= %s"
        f" AND (a.confirmed_at AT TIME ZONE '{_TZ}') <= %s AND a.status = 'confirmed'",
        (start_datetime, today + ' 23:59:59')
    ).fetchone()[0] or 0

    caja_efectivo = db.execute(
        f"SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id"
        f" WHERE (a.confirmed_at AT TIME ZONE '{_TZ}') >= %s"
        f" AND (a.confirmed_at AT TIME ZONE '{_TZ}') <= %s"
        f" AND a.status = 'confirmed' AND a.payment_method = 'efectivo'",
        (start_datetime, today + ' 23:59:59')
    ).fetchone()[0] or 0

    caja_transferencia = db.execute(
        f"SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id"
        f" WHERE (a.confirmed_at AT TIME ZONE '{_TZ}') >= %s"
        f" AND (a.confirmed_at AT TIME ZONE '{_TZ}') <= %s"
        f" AND a.status = 'confirmed' AND a.payment_method = 'transferencia'",
        (start_datetime, today + ' 23:59:59')
    ).fetchone()[0] or 0

    caja_hoy_sales = db.execute(
        f"SELECT SUM(price) FROM sales WHERE (created_at AT TIME ZONE '{_TZ}') >= %s",
        (start_datetime,)
    ).fetchone()[0] or 0
    caja_efectivo += caja_hoy_sales
    caja_hoy_val = caja_hoy_app + caja_hoy_sales

    sales_today = db.execute(
        f"SELECT * FROM sales WHERE (created_at AT TIME ZONE '{_TZ}') >= %s ORDER BY created_at DESC",
        (start_datetime,)
    ).fetchall()

    gastos_hoy_val = db.execute(
        f"SELECT SUM(amount) FROM expenses WHERE (created_at AT TIME ZONE '{_TZ}') >= %s",
        (start_datetime,)
    ).fetchone()[0] or 0

    caja_hoy = f"{caja_hoy_val:,.2f}".replace(",", ".")
    gastos_hoy_str = f"{gastos_hoy_val:,.2f}".replace(",", ".")
    net_profit = caja_hoy_val - gastos_hoy_val
    net_profit_str = f"{net_profit:,.2f}".replace(",", ".")
    
    # Monthly logic
    current_month = current_time_arg.strftime('%Y-%m')
    caja_mes_app = db.execute(
        f"SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id"
        f" WHERE a.date LIKE %s AND (a.confirmed_at AT TIME ZONE '{_TZ}') >= %s AND a.status = 'confirmed'",
        (current_month + '%', start_datetime)
    ).fetchone()[0] or 0

    caja_mes_sales = db.execute(
        f"SELECT SUM(price) FROM sales"
        f" WHERE TO_CHAR(created_at AT TIME ZONE '{_TZ}', 'YYYY-MM') = %s"
        f" AND (created_at AT TIME ZONE '{_TZ}') >= %s",
        (current_month, start_datetime)
    ).fetchone()[0] or 0

    caja_mes = caja_mes_app + caja_mes_sales
    gastos_mes = db.execute(
        f"SELECT SUM(amount) FROM expenses"
        f" WHERE TO_CHAR(created_at AT TIME ZONE '{_TZ}', 'YYYY-MM') = %s"
        f" AND (created_at AT TIME ZONE '{_TZ}') >= %s",
        (current_month, start_datetime)
    ).fetchone()[0] or 0
    net_profit_mes = caja_mes - gastos_mes
    
    caja_mes_str = f"{caja_mes:,.2f}".replace(",", ".")
    gastos_mes_str = f"{gastos_mes:,.2f}".replace(",", ".")
    net_profit_mes_str = f"{net_profit_mes:,.2f}".replace(",", ".")
    
    # Chart 7 days
    chart_labels = []
    chart_data = []
    for i in range(6, -1, -1):
        d = current_time_arg - timedelta(days=i)
        d_str = d.strftime('%Y-%m-%d')
        chart_labels.append(['Dom','Lun','Mar','Mie','Jue','Vie','Sab'][int(d.strftime('%w'))])
        inc_app = db.execute(
            f"SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id"
            f" WHERE a.date = %s AND (a.confirmed_at AT TIME ZONE '{_TZ}') >= %s AND a.status = 'confirmed'",
            (d_str, start_datetime)
        ).fetchone()[0] or 0
        inc_sales = db.execute(
            f"SELECT SUM(price) FROM sales"
            f" WHERE (created_at AT TIME ZONE '{_TZ}')::date = %s"
            f" AND (created_at AT TIME ZONE '{_TZ}') >= %s",
            (d_str, start_datetime)
        ).fetchone()[0] or 0
        chart_data.append(inc_app + inc_sales)
        
    settings = dict(db.execute('SELECT key, value FROM settings').fetchall())
    
    return render_template('admin/finances.html', 
                           appointments_today=appointments_today, 
                           total_clients=total_clients, caja_hoy=caja_hoy,
                           gastos_hoy=gastos_hoy_str, net_profit=net_profit_str,
                           chart_labels=chart_labels, chart_data=chart_data,
                           settings=settings, sales=sales_today,
                           caja_mes=caja_mes_str, gastos_mes=gastos_mes_str, net_mes=net_profit_mes_str,
                           caja_efectivo=caja_efectivo, caja_transferencia=caja_transferencia)

@admin_bp.route('/appointments/<int:id>/status', methods=['POST'])
@login_required
def update_status(id):
    status = request.form['status']
    payment_method = request.form.get('payment_method', 'efectivo')
    db = get_db()
    if status == 'confirmed':
        db.execute(
            "UPDATE appointments SET status = %s, payment_method = %s, confirmed_at = CURRENT_TIMESTAMP WHERE id = %s",
            (status, payment_method, id)
        )
    else:
        db.execute(
            "UPDATE appointments SET status = %s, payment_method = %s WHERE id = %s",
            (status, payment_method, id)
        )
    db.commit()
    return redirect(request.referrer)

@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    db = get_db()
    if request.method == 'POST':
        # Handle file upload
        if 'logo' in request.files:
            file = request.files['logo']
            if file.filename != '':
                filename = 'logo.png'
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                db.execute(
                    "INSERT INTO settings (key, value) VALUES ('logo_path', %s)"
                    " ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value",
                    (filename,)
                )
        
        # Handle other settings
        for key in ['barber_name', 'whatsapp', 'deposit_percentage', 'bank_details', 
                    'hours_mon_fri_start_1', 'hours_mon_fri_end_1', 
                    'hours_mon_fri_start_2', 'hours_mon_fri_end_2']:
            if key in request.form:
                db.execute(
                    "INSERT INTO settings (key, value) VALUES (%s, %s)"
                    " ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value",
                    (key, request.form[key])
                )
                
        db.commit()
        flash('Configuración guardada')
        return redirect(url_for('admin.settings'))
        
    settings = dict(db.execute('SELECT key, value FROM settings').fetchall())
    return render_template('admin/settings.html', settings=settings)

@admin_bp.route('/blocks', methods=['GET', 'POST'])
@login_required
def blocks():
    db = get_db()
    if request.method == 'POST':
        b_type = request.form['type']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        
        if b_type == 'date':
            date = request.form['date']
            db.execute(
                "INSERT INTO blocks (type, date, start_time, end_time) VALUES (%s, %s, %s, %s)",
                (b_type, date, start_time, end_time)
            )
        elif b_type == 'recurring':
            day_of_week = request.form['day_of_week']
            db.execute(
                "INSERT INTO blocks (type, day_of_week, start_time, end_time) VALUES (%s, %s, %s, %s)",
                (b_type, day_of_week, start_time, end_time)
            )
            
        db.commit()
        return redirect(url_for('admin.blocks'))
        
    blocks = db.execute("SELECT * FROM blocks").fetchall()
    
    # HISTORIAL MENSUAL
    months_query = db.execute(f'''
        SELECT DISTINCT LEFT(date, 7) as m FROM appointments WHERE status='confirmed'
        UNION
        SELECT DISTINCT TO_CHAR(created_at AT TIME ZONE '{_TZ}', 'YYYY-MM') as m FROM sales
        UNION
        SELECT DISTINCT TO_CHAR(created_at AT TIME ZONE '{_TZ}', 'YYYY-MM') as m FROM expenses
    ''').fetchall()
    
    monthly_history = []
    for row in months_query:
        m = row['m']
        if not m: continue
        
        c_app = db.execute(
            "SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id"
            " WHERE a.date LIKE %s AND a.status = 'confirmed'",
            (m + '%',)
        ).fetchone()[0] or 0
        c_sales = db.execute(
            f"SELECT SUM(price) FROM sales WHERE TO_CHAR(created_at AT TIME ZONE '{_TZ}', 'YYYY-MM') = %s",
            (m,)
        ).fetchone()[0] or 0
        c_exp = db.execute(
            f"SELECT SUM(amount) FROM expenses WHERE TO_CHAR(created_at AT TIME ZONE '{_TZ}', 'YYYY-MM') = %s",
            (m,)
        ).fetchone()[0] or 0
        
        c_total = c_app + c_sales
        c_net = c_total - c_exp
        
        monthly_history.append({
            'month': m,
            'caja': f"{c_total:,.2f}".replace(",", "."),
            'gastos': f"{c_exp:,.2f}".replace(",", "."),
            'neto': f"{c_net:,.2f}".replace(",", ".")
        })
        
    # Sort history descending (newest first)
    monthly_history.sort(key=lambda x: x['month'], reverse=True)

    settings=dict(db.execute('SELECT key, value FROM settings').fetchall())
    services = db.execute('SELECT * FROM services').fetchall()
    return render_template('admin/blocks.html', blocks=blocks, settings=settings)

@admin_bp.route('/blocks/<int:id>/delete', methods=['POST'])
@login_required
def delete_block(id):
    db = get_db()
    db.execute("DELETE FROM blocks WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('admin.blocks'))


@admin_bp.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    db = get_db()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        from werkzeug.security import generate_password_hash
        try:
            db.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (email, generate_password_hash(password))
            )
            db.commit()
            flash('Usuario agregado correctamente')
        except:
            flash('Error: El usuario/correo ya existe')
        return redirect(url_for('admin.users'))
        
    users_list = db.execute("SELECT id, username FROM users").fetchall()
    
    # HISTORIAL MENSUAL
    months_query = db.execute(f'''
        SELECT DISTINCT LEFT(date, 7) as m FROM appointments WHERE status='confirmed'
        UNION
        SELECT DISTINCT TO_CHAR(created_at AT TIME ZONE '{_TZ}', 'YYYY-MM') as m FROM sales
        UNION
        SELECT DISTINCT TO_CHAR(created_at AT TIME ZONE '{_TZ}', 'YYYY-MM') as m FROM expenses
    ''').fetchall()
    
    monthly_history = []
    for row in months_query:
        m = row['m']
        if not m: continue
        
        c_app = db.execute(
            "SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id"
            " WHERE a.date LIKE %s AND a.status = 'confirmed'",
            (m + '%',)
        ).fetchone()[0] or 0
        c_sales = db.execute(
            f"SELECT SUM(price) FROM sales WHERE TO_CHAR(created_at AT TIME ZONE '{_TZ}', 'YYYY-MM') = %s",
            (m,)
        ).fetchone()[0] or 0
        c_exp = db.execute(
            f"SELECT SUM(amount) FROM expenses WHERE TO_CHAR(created_at AT TIME ZONE '{_TZ}', 'YYYY-MM') = %s",
            (m,)
        ).fetchone()[0] or 0
        
        c_total = c_app + c_sales
        c_net = c_total - c_exp
        
        monthly_history.append({
            'month': m,
            'caja': f"{c_total:,.2f}".replace(",", "."),
            'gastos': f"{c_exp:,.2f}".replace(",", "."),
            'neto': f"{c_net:,.2f}".replace(",", ".")
        })
        
    # Sort history descending (newest first)
    monthly_history.sort(key=lambda x: x['month'], reverse=True)

    settings=dict(db.execute('SELECT key, value FROM settings').fetchall())
    services = db.execute('SELECT * FROM services').fetchall()
    return render_template('admin/users.html', users=users_list, settings=settings)

@admin_bp.route('/users/<int:id>/delete', methods=['POST'])
@login_required
def delete_user(id):
    if id == session.get('user_id'):
        flash('No puedes borrar tu propia cuenta')
        return redirect(url_for('admin.users'))
        
    db = get_db()
    db.execute("DELETE FROM users WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('admin.users'))

@admin_bp.route('/sales/add', methods=['POST'])
@login_required
def add_sale():
    product_name = request.form['product_name']
    price = request.form['price']
    db = get_db()
    db.execute("INSERT INTO sales (product_name, price) VALUES (%s, %s)", (product_name, price))
    db.commit()
    return redirect(request.referrer or url_for('admin.dashboard'))

@admin_bp.route('/sales/<int:id>/delete', methods=['POST'])
@login_required
def delete_sale(id):
    db = get_db()
    db.execute("DELETE FROM sales WHERE id = %s", (id,))
    db.commit()
    return redirect(request.referrer or url_for('admin.dashboard'))

@admin_bp.route('/expenses/add', methods=['POST'])
@login_required
def add_expense():
    concept = request.form['concept']
    amount = request.form['amount']
    db = get_db()
    db.execute("INSERT INTO expenses (concept, amount) VALUES (%s, %s)", (concept, amount))
    db.commit()
    return redirect(request.referrer or url_for('admin.dashboard'))

@admin_bp.route('/api/client/<phone>')
@login_required
def get_client(phone):
    db = get_db()
    current_month = now_arg().strftime('%Y-%m')
    
    # Visits this month
    visits = db.execute(
        "SELECT COUNT(*) FROM appointments WHERE client_phone = %s AND status = 'confirmed' AND date LIKE %s",
        (phone, f"{current_month}%")
    ).fetchone()[0]
    
    # LTV
    ltv = db.execute(
        "SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id"
        " WHERE a.client_phone = %s AND a.status = 'confirmed'",
        (phone,)
    ).fetchone()[0]
    ltv = ltv if ltv else 0
    
    # No shows
    no_shows = db.execute(
        "SELECT COUNT(*) FROM appointments WHERE client_phone = %s AND status = 'cancelled'",
        (phone,)
    ).fetchone()[0]
    
    return {"visits": visits, "ltv": ltv, "no_shows": no_shows}

@admin_bp.route('/appointments/add', methods=['POST'])
@login_required
def add_appointment():
    client_name = request.form['client_name']
    client_phone = request.form['client_phone']
    service_id = request.form['service_id']
    date = request.form['date']
    time = request.form['time']
    
    db = get_db()
    db.execute(
        "INSERT INTO appointments (client_name, client_phone, service_id, date, time, status) VALUES (%s, %s, %s, %s, %s, 'pending')",
        (client_name, client_phone, service_id, date, time)
    )
    db.commit()
    return redirect(request.referrer or url_for('admin.dashboard'))

@admin_bp.route('/reset_caja', methods=['POST'])
@login_required
def reset_caja():
    db = get_db()
    now = now_arg().strftime('%Y-%m-%d %H:%M:%S')
    db.execute(
        "INSERT INTO settings (key, value) VALUES ('last_reset_date', %s)"
        " ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value",
        (now,)
    )
    db.commit()
    return redirect(request.referrer or url_for('admin.finances'))
