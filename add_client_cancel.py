import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "routes/cliente_routes.py")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_post = """    if request.method == 'POST':
        phone = request.form.get('phone', '').strip()
        searched = True
        if phone:
            turnos = db.execute('''
                SELECT a.*, s.name as service_name, s.price 
                FROM appointments a 
                JOIN services s ON a.service_id = s.id 
                WHERE a.client_phone = ? 
                ORDER BY a.date DESC, a.time DESC
            ''', (phone,)).fetchall()"""

new_post = """    if request.method == 'POST':
        phone = request.form.get('phone', '').strip()
        searched = True
        if phone:
            rows = db.execute('''
                SELECT a.*, s.name as service_name, s.price 
                FROM appointments a 
                JOIN services s ON a.service_id = s.id 
                WHERE a.client_phone = ? 
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
                    t['can_cancel'] = (appt_dt - now) > timedelta(hours=2) and t['status'] != 'cancelled'
                    t['appt_dt'] = appt_dt
                except Exception:
                    t['can_cancel'] = False
                    t['appt_dt'] = now
                turnos.append(t)
            
            # Re-sort to show upcoming first, then past
            turnos.sort(key=lambda x: (x['appt_dt'] < now, abs((x['appt_dt'] - now).total_seconds())))
"""
content = content.replace(old_post, new_post)

cancel_route = """
@cliente_bp.route('/cancelar-turno/<int:id>', methods=['POST'])
def cancelar_turno_cliente(id):
    db = get_db()
    from datetime import datetime, timedelta
    
    a = db.execute("SELECT date, time, status FROM appointments WHERE id = ?", (id,)).fetchone()
    if a and a['status'] != 'cancelled':
        now = datetime.now()
        appt_dt = datetime.strptime(f"{a['date']} {a['time']}", "%Y-%m-%d %H:%M")
        if (appt_dt - now) > timedelta(hours=2):
            db.execute("UPDATE appointments SET status = 'cancelled' WHERE id = ?", (id,))
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
"""
content += cancel_route

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
