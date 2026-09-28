import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"

# 1. Update admin_routes.py
routes_path = os.path.join(base, "routes/admin_routes.py")
with open(routes_path, "r", encoding="utf-8") as f:
    routes = f.read()

# Pass services to dashboard
if "services=services" not in routes:
    routes = routes.replace("settings=dict(db.execute('SELECT key, value FROM settings').fetchall())",
                            "settings=dict(db.execute('SELECT key, value FROM settings').fetchall())\n    services = db.execute('SELECT * FROM services').fetchall()")
    routes = routes.replace("expenses=expenses_today)", "expenses=expenses_today, services=services)")

# Add manual appointment route
manual_route = """
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
        "INSERT INTO appointments (client_name, client_phone, service_id, date, time, status) VALUES (?, ?, ?, ?, ?, 'confirmed')",
        (client_name, client_phone, service_id, date, time)
    )
    db.commit()
    return redirect(url_for('admin.dashboard'))
"""
if "/appointments/add" not in routes:
    routes += manual_route

with open(routes_path, "w", encoding="utf-8") as f:
    f.write(routes)


# 2. Update admin/dashboard.html (Add button and modal)
dash_path = os.path.join(base, "templates/admin/dashboard.html")
with open(dash_path, "r", encoding="utf-8") as f:
    dash = f.read()

btn_html = """<div class="flex-between mb-2">
            <h3 class="space-font">Agenda de Hoy</h3>
            <button onclick="document.getElementById('modal-turno').style.display='flex'" class="btn-gold" style="padding: 0.5rem 1rem; font-size: 0.9rem;"><i data-lucide="plus" style="width:16px; margin-right:5px; vertical-align:text-bottom;"></i> Agendar Manual</button>
        </div>"""
dash = dash.replace('<h3 class="mb-2 space-font">Agenda de Hoy</h3>', btn_html)

modal_turno_html = """
<!-- Modal Turno Manual -->
<div id="modal-turno" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); z-index:1000; justify-content:center; align-items:center;">
    <div class="glass-panel" style="width: 400px; background: #050505;">
        <div class="flex-between mb-2">
            <h3 class="space-font">Agendar Turno Manual</h3>
            <button class="btn-icon" onclick="document.getElementById('modal-turno').style.display='none'"><i data-lucide="x"></i></button>
        </div>
        <form method="POST" action="{{ url_for('admin.add_appointment') }}">
            <label>Nombre del Cliente</label>
            <input type="text" name="client_name" required>
            
            <label>Celular</label>
            <input type="tel" name="client_phone" required>
            
            <label>Servicio</label>
            <select name="service_id" required style="width:100%; padding:0.8rem; background:rgba(255,255,255,0.05); color:white; border:1px solid var(--glass-border); border-radius:8px; margin-bottom:1rem;">
                {% for s in services %}
                <option value="{{ s.id }}">{{ s.name }}</option>
                {% endfor %}
            </select>
            
            <div style="display:flex; gap:1rem;">
                <div style="flex:1;">
                    <label>Fecha</label>
                    <input type="date" name="date" required>
                </div>
                <div style="flex:1;">
                    <label>Hora</label>
                    <input type="time" name="time" required>
                </div>
            </div>
            
            <button type="submit" class="btn-gold mt-2">Guardar Turno</button>
        </form>
    </div>
</div>
"""
if 'id="modal-turno"' not in dash:
    dash = dash.replace("<!-- Modal Gasto -->", modal_turno_html + "\n<!-- Modal Gasto -->")

with open(dash_path, "w", encoding="utf-8") as f:
    f.write(dash)


# 3. Update cliente/index.html (Add WhatsApp support link)
index_path = os.path.join(base, "templates/cliente/index.html")
with open(index_path, "r", encoding="utf-8") as f:
    index = f.read()

wa_support_html = """
<div style="text-align: center; margin-top: 3rem;">
    <p class="text-dim" style="font-size: 0.9rem;">
        APreferA-s agendar por mensaje o tenAcs dudas?<br>
        <a href="https://wa.me/{{ settings.get('whatsapp', '')|replace('+', '') }}" target="_blank" class="gold-text" style="text-decoration:none; display:inline-block; margin-top:0.5rem; font-weight: 500;">
            <i data-lucide="message-circle" style="width: 16px; vertical-align: text-bottom;"></i> Escribinos al WhatsApp
        </a>
    </p>
</div>
<!-- Developer Footer -->
"""

if "Escribinos al WhatsApp" not in index:
    index = index.replace("<!-- Developer Footer -->", wa_support_html)
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index)

