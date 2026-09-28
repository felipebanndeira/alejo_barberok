from flask import Blueprint, render_template, request, jsonify, redirect, url_for
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
    available_times = [t['time'] for t in times if t['available']]
    if data['time'] not in available_times:
        return jsonify({'success': False, 'message': 'Horario no disponible'}), 400
        
    db.execute(
        "INSERT INTO appointments (client_name, client_phone, service_id, date, time) VALUES (%s, %s, %s, %s, %s)",
        (data['name'], data['phone'], data['service_id'], data['date'], data['time'])
    )
    db.commit()
    
    return jsonify({'success': True})

@cliente_bp.route('/mis-turnos', methods=['GET', 'POST'])
def mis_turnos():
    db = get_db()
    settings = dict(db.execute('SELECT key, value FROM settings').fetchall())
    turnos = None
    searched = False
    
    if request.method == 'POST':
        phone = request.form.get('phone', '').strip()
        searched = True
        if phone:
            rows = db.execute('''
                SELECT a.*, s.name as service_name, s.price 
                FROM appointments a 
                JOIN services s ON a.service_id = s.id 
                WHERE a.client_phone = %s 
                ORDER BY a.date DESC, a.time DESC
            ''', (phone,)).fetchall()
            
            from datetime import datetime, timedelta
            now = datetime.now()
            turnos = []
            for r in rows:
                t = dict(r)
                # Compute if it can be cancelled
                try:
                    appt_dt = datetime.strptime(f"{t['date']} {t['time']}", "%Y-%m-%d %H:%M")
                    t['can_cancel'] = (appt_dt - now) > timedelta(hours=1) and t['status'] != 'cancelled'
                    t['appt_dt'] = appt_dt
                except Exception:
                    t['can_cancel'] = False
                    t['appt_dt'] = now
                turnos.append(t)
            
            # Re-sort to show upcoming first, then past
            turnos.sort(key=lambda x: (x['appt_dt'] < now, abs((x['appt_dt'] - now).total_seconds())))

            
    return render_template('cliente/mis_turnos.html', settings=settings, turnos=turnos, searched=searched)

@cliente_bp.route('/cancelar-turno/<int:id>', methods=['POST'])
def cancelar_turno_cliente(id):
    db = get_db()
    from datetime import datetime, timedelta
    
    a = db.execute("SELECT date, time, status FROM appointments WHERE id = %s", (id,)).fetchone()
    if a and a['status'] != 'cancelled':
        now = datetime.now()
        appt_dt = datetime.strptime(f"{a['date']} {a['time']}", "%Y-%m-%d %H:%M")
        if (appt_dt - now) > timedelta(hours=1):
            db.execute("UPDATE appointments SET status = 'cancelled' WHERE id = %s", (id,))
            db.commit()
            
    # Need to keep the phone number in the form submission so we redirect back with phone or something
    # Since we are returning redirect, we can't easily POST back the phone. 
    # Let's just render a template or flash a message. We'll use a simple flash + redirect to index, or we'll pass phone in form.
    # Actually, we can expect phone in the form data
    phone = request.form.get('phone', '')
    if phone:
        # 307 Temporary Redirect preserves POST data
        return redirect(url_for('cliente.mis_turnos'), code=307)
    return redirect(url_for('cliente.index'))
