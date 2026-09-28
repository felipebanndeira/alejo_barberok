import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "routes/admin_routes.py")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# We will just replace everything between `def dashboard():` and `@admin_bp.route('/appointments/<int:id>/status', methods=['POST'])`
# with our perfectly crafted new logic.

new_logic = """def dashboard():
    db = get_db()
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Shift logic
    shift_active_row = db.execute("SELECT value FROM settings WHERE key='shift_active'").fetchone()
    shift_active = shift_active_row[0] == 'true' if shift_active_row else False
    shift_start_row = db.execute("SELECT value FROM settings WHERE key='shift_start'").fetchone()
    shift_start = shift_start_row[0] if shift_start_row else '2000-01-01 00:00:00'
    
    # Metrics
    appointments_today = db.execute("SELECT COUNT(*) FROM appointments WHERE date = ? AND status != 'cancelled'", (today,)).fetchone()[0]
    total_clients = db.execute("SELECT COUNT(DISTINCT client_phone) FROM appointments").fetchone()[0]
    
    caja_total = 0
    gastos_total = 0
    sales_today = []
    expenses_today = []
    
    if shift_active:
        caja_app = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE (a.date || ' ' || a.time || ':00') >= ? AND a.status = 'confirmed'", (shift_start,)).fetchone()[0] or 0
        sales_today = db.execute("SELECT * FROM sales WHERE created_at >= ?", (shift_start,)).fetchall()
        caja_sales = sum(s['price'] for s in sales_today)
        caja_total = caja_app + caja_sales
        expenses_today = db.execute("SELECT * FROM expenses WHERE created_at >= ?", (shift_start,)).fetchall()
        gastos_total = sum(e['amount'] for e in expenses_today)

    caja_hoy = f"{caja_total:g}".replace('.', ',') if caja_total < 1000 else f"{caja_total:,.0f}".replace(',', '.')
    gastos_hoy_str = f"{gastos_total:g}".replace('.', ',') if gastos_total < 1000 else f"{gastos_total:,.0f}".replace(',', '.')
    
    net_profit = caja_total - gastos_total
    net_profit_str = f"{net_profit:g}".replace('.', ',') if abs(net_profit) < 1000 else f"{net_profit:,.0f}".replace(',', '.')

    # Chart 7 days
    chart_labels = []
    chart_data = []
    for i in range(6, -1, -1):
        d = datetime.now() - timedelta(days=i)
        d_str = d.strftime('%Y-%m-%d')
        chart_labels.append(['Dom','Lun','Mar','Mie','Jue','Vie','Sab'][int(d.strftime('%w'))])
        inc_app = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE a.date = ? AND a.status = 'confirmed'", (d_str,)).fetchone()[0] or 0
        inc_sales = db.execute("SELECT SUM(price) FROM sales WHERE date(created_at, 'localtime') = ?", (d_str,)).fetchone()[0] or 0
        chart_data.append(inc_app + inc_sales)
    
    schedule = db.execute('''
        SELECT a.id, a.client_name, a.client_phone, a.date, a.time, a.status, s.name as service_name 
        FROM appointments a
        JOIN services s ON a.service_id = s.id
        WHERE a.date >= ? AND a.status != 'cancelled'
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
                           schedule=schedule, shift_active=shift_active, settings=settings, sales=sales_today, expenses=expenses_today, services=services)

@admin_bp.route('/finances')
@login_required
def finances():
    db = get_db()
    today = datetime.now().strftime('%Y-%m-%d')
    appointments_today = db.execute("SELECT COUNT(*) FROM appointments WHERE date = ?", (today,)).fetchone()[0]
    total_clients = db.execute("SELECT COUNT(DISTINCT client_phone) FROM appointments").fetchone()[0]
    
    # Shift logic
    shift_active_row = db.execute("SELECT value FROM settings WHERE key='shift_active'").fetchone()
    shift_active = shift_active_row[0] == 'true' if shift_active_row else False
    shift_start_row = db.execute("SELECT value FROM settings WHERE key='shift_start'").fetchone()
    shift_start = shift_start_row[0] if shift_start_row else '2000-01-01 00:00:00'

    caja_hoy_val = 0
    caja_efectivo = 0
    caja_transferencia = 0
    gastos_hoy_val = 0
    sales_today = []
    
    if shift_active:
        caja_hoy_app = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE (a.date || ' ' || a.time || ':00') >= ? AND a.status = 'confirmed'", (shift_start,)).fetchone()[0] or 0
        caja_efectivo = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE (a.date || ' ' || a.time || ':00') >= ? AND a.status = 'confirmed' AND a.payment_method = 'efectivo'", (shift_start,)).fetchone()[0] or 0
        caja_transferencia = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE (a.date || ' ' || a.time || ':00') >= ? AND a.status = 'confirmed' AND a.payment_method = 'transferencia'", (shift_start,)).fetchone()[0] or 0
        caja_hoy_sales = db.execute("SELECT SUM(price) FROM sales WHERE created_at >= ?", (shift_start,)).fetchone()[0] or 0
        caja_efectivo += caja_hoy_sales
        caja_hoy_val = caja_hoy_app + caja_hoy_sales
        sales_today = db.execute("SELECT * FROM sales WHERE created_at >= ? ORDER BY created_at DESC", (shift_start,)).fetchall()
        gastos_hoy_val = db.execute("SELECT SUM(amount) FROM expenses WHERE created_at >= ?", (shift_start,)).fetchone()[0] or 0

    caja_hoy = f"{caja_hoy_val:,.2f}".replace(",", ".")
    gastos_hoy_str = f"{gastos_hoy_val:,.2f}".replace(",", ".")
    net_profit = caja_hoy_val - gastos_hoy_val
    net_profit_str = f"{net_profit:,.2f}".replace(",", ".")
    
    # Monthly logic
    current_month = datetime.now().strftime('%Y-%m')
    caja_mes_app = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE a.date LIKE ? AND a.status = 'confirmed'", (current_month + '%',)).fetchone()[0] or 0
    caja_mes_sales = db.execute("SELECT SUM(price) FROM sales WHERE strftime('%Y-%m', created_at, 'localtime') = ?", (current_month,)).fetchone()[0] or 0
    caja_mes = caja_mes_app + caja_mes_sales
    gastos_mes = db.execute("SELECT SUM(amount) FROM expenses WHERE strftime('%Y-%m', created_at, 'localtime') = ?", (current_month,)).fetchone()[0] or 0
    net_profit_mes = caja_mes - gastos_mes
    
    caja_mes_str = f"{caja_mes:,.2f}".replace(",", ".")
    gastos_mes_str = f"{gastos_mes:,.2f}".replace(",", ".")
    net_profit_mes_str = f"{net_profit_mes:,.2f}".replace(",", ".")
    
    # Chart 7 days
    chart_labels = []
    chart_data = []
    for i in range(6, -1, -1):
        d = datetime.now() - timedelta(days=i)
        d_str = d.strftime('%Y-%m-%d')
        chart_labels.append(['Dom','Lun','Mar','Mie','Jue','Vie','Sab'][int(d.strftime('%w'))])
        inc_app = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE a.date = ? AND a.status = 'confirmed'", (d_str,)).fetchone()[0] or 0
        inc_sales = db.execute("SELECT SUM(price) FROM sales WHERE date(created_at, 'localtime') = ?", (d_str,)).fetchone()[0] or 0
        chart_data.append(inc_app + inc_sales)
        
    settings = dict(db.execute('SELECT key, value FROM settings').fetchall())
    
    return render_template('admin/finances.html', 
                           appointments_today=appointments_today, 
                           total_clients=total_clients, caja_hoy=caja_hoy,
                           gastos_hoy=gastos_hoy_str, net_profit=net_profit_str,
                           chart_labels=chart_labels, chart_data=chart_data,
                           shift_active=shift_active, settings=settings, sales=sales_today,
                           caja_mes=caja_mes_str, gastos_mes=gastos_mes_str, net_mes=net_profit_mes_str,
                           caja_efectivo=caja_efectivo, caja_transferencia=caja_transferencia)
"""

content = re.sub(r"def dashboard\(\):.*?@admin_bp\.route\('/appointments/<int:id>/status', methods=\['POST'\]\)", new_logic + "\n@admin_bp.route('/appointments/<int:id>/status', methods=['POST'])", content, flags=re.DOTALL)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
