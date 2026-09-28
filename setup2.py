import os

base = r"c:\Users\usser\Documents\Alejo barber"

files = {
    r"core\availability.py": '''from datetime import datetime, timedelta
from core.db import get_db

def get_available_times(date_str):
    db = get_db()
    
    # 1. Get Settings for hours
    settings = dict(db.execute('SELECT key, value FROM settings').fetchall())
    
    # Check if weekend (Mon=0, Sun=6)
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    if date_obj.weekday() >= 5:
        return [] # Sábados y domingos cerrados por defecto según el MVP
        
    start1 = settings.get('hours_mon_fri_start_1', '10:30')
    end1 = settings.get('hours_mon_fri_end_1', '13:00')
    start2 = settings.get('hours_mon_fri_start_2', '16:30')
    end2 = settings.get('hours_mon_fri_end_2', '21:00')
    
    # 2. Generate all possible slots (30 min increments)
    slots = []
    
    def generate_slots(start_str, end_str):
        if not start_str or not end_str: return
        current = datetime.strptime(f"{date_str} {start_str}", '%Y-%m-%d %H:%M')
        end_time = datetime.strptime(f"{date_str} {end_str}", '%Y-%m-%d %H:%M')
        
        while current + timedelta(minutes=30) <= end_time:
            slots.append(current.strftime('%H:%M'))
            current += timedelta(minutes=30)
            
    generate_slots(start1, end1)
    generate_slots(start2, end2)
    
    # 3. Filter past times if it's today
    now = datetime.now()
    if date_obj.date() == now.date():
        current_time_str = now.strftime('%H:%M')
        slots = [s for s in slots if s > current_time_str]
        
    # 4. Remove blocks (Specific date or recurring day_of_week)
    blocks = db.execute(
        "SELECT start_time, end_time FROM blocks WHERE (type='date' AND date=?) OR (type='recurring' AND day_of_week=?)",
        (date_str, date_obj.weekday())
    ).fetchall()
    
    for b in blocks:
        bs_time = b['start_time']
        be_time = b['end_time']
        # Remove any slot that falls inside the block
        slots = [s for s in slots if not (bs_time <= s < be_time)]
        
    # 5. Remove already booked appointments
    appointments = db.execute(
        "SELECT time FROM appointments WHERE date=? AND status != 'cancelled'",
        (date_str,)
    ).fetchall()
    
    booked_times = [a['time'] for a in appointments]
    slots = [s for s in slots if s not in booked_times]
    
    return slots
''',
    r"routes\cliente_routes.py": '''from flask import Blueprint, render_template, request, jsonify
from core.db import get_db
from core.availability import get_available_times

cliente_bp = Blueprint('cliente', __name__)

@cliente_bp.route('/')
def index():
    db = get_db()
    services = db.execute('SELECT * FROM services').fetchall()
    settings = dict(db.execute('SELECT key, value FROM settings').fetchall())
    return render_template('cliente/index.html', services=services, settings=settings)

@cliente_bp.route('/api/availability')
def api_availability():
    date_str = request.args.get('date')
    if not date_str:
        return jsonify([])
    times = get_available_times(date_str)
    return jsonify(times)

@cliente_bp.route('/api/book', methods=['POST'])
def api_book():
    data = request.json
    db = get_db()
    
    # Verify availability again just in case
    times = get_available_times(data['date'])
    if data['time'] not in times:
        return jsonify({'success': False, 'message': 'Horario no disponible'}), 400
        
    db.execute(
        "INSERT INTO appointments (client_name, client_phone, service_id, date, time) VALUES (?, ?, ?, ?, ?)",
        (data['name'], data['phone'], data['service_id'], data['date'], data['time'])
    )
    db.commit()
    
    return jsonify({'success': True})
''',
    r"routes\admin_routes.py": '''from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash
from werkzeug.security import check_password_hash
import os
from datetime import datetime
from core.db import get_db
from core.auth import login_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        
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
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Metrics
    appointments_today = db.execute("SELECT COUNT(*) FROM appointments WHERE date = ? AND status != 'cancelled'", (today,)).fetchone()[0]
    total_clients = db.execute("SELECT COUNT(DISTINCT client_phone) FROM appointments").fetchone()[0]
    
    # Today's schedule
    schedule = db.execute("""
        SELECT a.id, a.client_name, a.client_phone, a.time, a.status, s.name as service_name 
        FROM appointments a
        JOIN services s ON a.service_id = s.id
        WHERE a.date = ?
        ORDER BY a.time
    """, (today,)).fetchall()
    
    return render_template('admin/dashboard.html', 
                           appointments_today=appointments_today, 
                           total_clients=total_clients,
                           schedule=schedule)

@admin_bp.route('/appointments/<int:id>/status', methods=['POST'])
@login_required
def update_status(id):
    status = request.form['status']
    db = get_db()
    db.execute("UPDATE appointments SET status = ? WHERE id = ?", (status, id))
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
                db.execute("REPLACE INTO settings (key, value) VALUES ('logo_path', ?)", (filename,))
        
        # Handle other settings
        for key in ['barber_name', 'whatsapp', 'deposit_percentage', 'bank_details', 
                    'hours_mon_fri_start_1', 'hours_mon_fri_end_1', 
                    'hours_mon_fri_start_2', 'hours_mon_fri_end_2']:
            if key in request.form:
                db.execute("REPLACE INTO settings (key, value) VALUES (?, ?)", (key, request.form[key]))
                
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
            db.execute("INSERT INTO blocks (type, date, start_time, end_time) VALUES (?, ?, ?, ?)",
                       (b_type, date, start_time, end_time))
        elif b_type == 'recurring':
            day_of_week = request.form['day_of_week']
            db.execute("INSERT INTO blocks (type, day_of_week, start_time, end_time) VALUES (?, ?, ?, ?)",
                       (b_type, day_of_week, start_time, end_time))
            
        db.commit()
        return redirect(url_for('admin.blocks'))
        
    blocks = db.execute("SELECT * FROM blocks").fetchall()
    return render_template('admin/blocks.html', blocks=blocks)

@admin_bp.route('/blocks/<int:id>/delete', methods=['POST'])
@login_required
def delete_block(id):
    db = get_db()
    db.execute("DELETE FROM blocks WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for('admin.blocks'))
'''
}

for path, content in files.items():
    full_path = os.path.join(base, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
