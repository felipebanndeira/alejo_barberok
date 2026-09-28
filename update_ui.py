import os
import sqlite3
from datetime import datetime

base = r"c:\Users\usser\Documents\Alejo barber"

# 1. Update style.css to be cleaner
css_path = os.path.join(base, "static/css/style.css")
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# Make it cleaner
new_css = '''
:root {
    --bg-color: #0d0d0d;
    --card-bg: #151515;
    --primary-gold: #cfaa63;
    --primary-gold-dim: rgba(207, 170, 99, 0.1);
    --text-light: #f4f4f4;
    --text-dim: #888888;
    --border-color: #222222;
    
    font-family: 'Inter', -apple-system, sans-serif;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    background-color: var(--bg-color);
    color: var(--text-light);
    min-height: 100vh;
}

h1, h2, h3, h4 { font-weight: 400; }
.gold-text { color: var(--primary-gold); }
.text-dim { color: var(--text-dim); }

.glass-panel {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 2rem;
}

.btn-gold {
    background: var(--primary-gold);
    color: #000;
    border: none;
    padding: 0.8rem 1.5rem;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1rem;
    font-weight: 600;
    transition: opacity 0.2s;
    width: 100%;
}
.btn-gold:hover { opacity: 0.9; }

.btn-glass {
    background: transparent;
    color: var(--text-light);
    border: 1px solid var(--border-color);
    padding: 0.8rem 1.5rem;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.2s;
}
.btn-glass:hover { background: rgba(255,255,255,0.05); }

.container { max-width: 600px; margin: 0 auto; padding: 2rem 1rem; }

.step-container { display: none; animation: fadeIn 0.3s ease; }
.step-container.active { display: block; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

.service-card {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    padding: 1.5rem;
    border-radius: 12px;
    margin-bottom: 1rem;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.service-card:hover, .service-card.selected {
    border-color: var(--primary-gold);
    background: var(--primary-gold-dim);
}
.service-card h3 { font-size: 1.2rem; margin-bottom: 0.2rem; }
.service-price { font-size: 1.2rem; font-weight: 600; color: var(--primary-gold); }

input, select, textarea {
    width: 100%;
    background: var(--bg-color);
    border: 1px solid var(--border-color);
    color: var(--text-light);
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    font-family: inherit;
    font-size: 1rem;
}
input:focus, select:focus, textarea:focus { outline: none; border-color: var(--primary-gold); }

.time-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 0.8rem;
}
.time-slot {
    padding: 0.8rem;
    text-align: center;
    background: var(--bg-color);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
}
.time-slot:hover, .time-slot.selected {
    border-color: var(--primary-gold);
    color: var(--primary-gold);
    background: var(--primary-gold-dim);
}

/* Admin Dashboard layout */
.admin-layout { display: grid; grid-template-columns: 260px 1fr; min-height: 100vh; }
.sidebar { background: var(--card-bg); border-right: 1px solid var(--border-color); padding: 2rem; }
.sidebar ul { list-style: none; margin-top: 2.5rem; }
.sidebar li { margin-bottom: 0.5rem; }
.sidebar a {
    color: var(--text-dim);
    text-decoration: none;
    transition: color 0.2s;
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0.8rem 1rem;
    border-radius: 8px;
}
.sidebar a:hover, .sidebar a.active { color: var(--primary-gold); background: var(--primary-gold-dim); }
.admin-content { padding: 3rem; background: var(--bg-color); }

.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }
.stat-card { padding: 2rem; border-radius: 12px; }
.stat-card h3 { font-size: 2.5rem; margin: 0.5rem 0; font-weight: 600; }

.table-container { background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; overflow: hidden; }
table { width: 100%; border-collapse: collapse; }
th, td { padding: 1rem 1.5rem; text-align: left; border-bottom: 1px solid var(--border-color); }
th { color: var(--text-dim); font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.5px; }
tr:last-child td { border-bottom: none; }

.badge { padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.85rem; font-weight: 500; }
.badge.pending { background: rgba(255, 193, 7, 0.1); color: #ffc107; }
.badge.confirmed { background: rgba(40, 167, 69, 0.1); color: #28a745; }
.badge.cancelled { background: rgba(220, 53, 69, 0.1); color: #dc3545; }

.flex-between { display: flex; justify-content: space-between; align-items: center; }
.mt-2 { margin-top: 2rem; }
.mb-2 { margin-bottom: 2rem; }
.text-center { text-align: center; }
.w-100 { width: 100%; }

.logo-header {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
    margin-bottom: 2rem;
}
.logo-header img {
    height: 50px;
    width: auto;
}
.logo-header h1 {
    font-size: 1.8rem;
    font-weight: 600;
    margin: 0;
}
.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 12px;
}
.sidebar-logo img {
    height: 40px;
    width: auto;
}
.sidebar-logo h2 {
    font-size: 1.2rem;
    font-weight: 600;
    margin: 0;
}

/* Action buttons in table */
.actions-cell {
    display: flex;
    gap: 10px;
}
.btn-icon {
    background: transparent;
    border: 1px solid var(--border-color);
    color: var(--text-light);
    padding: 0.4rem;
    border-radius: 6px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}
.btn-icon:hover {
    background: rgba(255,255,255,0.05);
}
.btn-icon.delete:hover {
    background: rgba(220, 53, 69, 0.1);
    color: #dc3545;
    border-color: #dc3545;
}
'''
with open(css_path, "w", encoding="utf-8") as f:
    f.write(new_css)

# 2. Update JS to auto-advance on step 1
js_path = os.path.join(base, "static/js/main.js")
with open(js_path, "r", encoding="utf-8") as f:
    js = f.read()
# Replace step 1 logic
js = js.replace('''        document.getElementById('btn-next-1').style.display = 'inline-block';
    });''', '''        nextStep(2);
    });''')
with open(js_path, "w", encoding="utf-8") as f:
    f.write(js)

# 3. Update admin_routes.py to calculate "Caja"
admin_routes_path = os.path.join(base, "routes/admin_routes.py")
with open(admin_routes_path, "r", encoding="utf-8") as f:
    routes = f.read()

# Add caja calculation in dashboard route
if "caja_hoy" not in routes:
    routes = routes.replace(
        "total_clients = db.execute(\"SELECT COUNT(DISTINCT client_phone) FROM appointments\").fetchone()[0]",
        '''total_clients = db.execute("SELECT COUNT(DISTINCT client_phone) FROM appointments").fetchone()[0]
    
    # Calculate Caja
    caja = db.execute("""
        SELECT SUM(s.price) 
        FROM appointments a
        JOIN services s ON a.service_id = s.id
        WHERE a.date = ? AND a.status = 'confirmed'
    """, (today,)).fetchone()[0]
    caja_hoy = caja if caja else 0'''
    )
    routes = routes.replace(
        "total_clients=total_clients,",
        "total_clients=total_clients, caja_hoy=caja_hoy,"
    )
    with open(admin_routes_path, "w", encoding="utf-8") as f:
        f.write(routes)


# 4. Update index.html
index_path = os.path.join(base, "templates/cliente/index.html")
new_index = '''{% extends 'base.html' %}

{% block content %}
<div class="container">
    <div class="logo-header">
        {% if settings.get('logo_path') %}
            <img src="{{ url_for('static', filename='img/' + settings.get('logo_path')) }}" alt="Logo">
        {% endif %}
        <h1 class="gold-text">{{ settings.get('barber_name', 'Alejo Barber') }}</h1>
    </div>

    <!-- Step 1 -->
    <div id="step1" class="step-container active">
        <h2 class="mb-2 text-center" style="font-size: 1.2rem;">¿Qué servicio buscas?</h2>
        <div class="services-list">
            {% for s in services %}
            <div class="service-card" data-id="{{ s.id }}" data-name="{{ s.name }}" data-price="{{ s.price }}">
                <div>
                    <h3>{{ s.name }}</h3>
                    <p class="text-dim" style="font-size: 0.9rem;">30 min</p>
                </div>
                <div class="service-price">${{ s.price }}</div>
            </div>
            {% endfor %}
        </div>
    </div>

    <!-- Step 2 -->
    <div id="step2" class="step-container">
        <div class="glass-panel">
            <h2 class="mb-2" style="font-size: 1.2rem;">Elige fecha y hora</h2>
            <input type="date" id="date-picker">
            <div id="time-slots" class="time-grid mt-2"></div>
            
            <div class="flex-between mt-2">
                <button class="btn-glass" onclick="prevStep(1)">Volver</button>
                <button class="btn-gold" id="btn-next-2" style="display:none; width: auto;" onclick="nextStep(3)">Continuar</button>
            </div>
        </div>
    </div>

    <!-- Step 3 -->
    <div id="step3" class="step-container">
        <div class="glass-panel">
            <h2 class="mb-2" style="font-size: 1.2rem;">Tus datos</h2>
            <div style="background: var(--bg-color); padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;">
                <p style="margin-bottom: 0.5rem;"><span class="text-dim">Servicio:</span> <strong id="summary-service"></strong></p>
                <p style="margin-bottom: 0.5rem;"><span class="text-dim">Fecha:</span> <strong id="summary-date"></strong></p>
                <p><span class="text-dim">Total:</span> <strong id="summary-price" class="gold-text"></strong></p>
            </div>
            
            <input type="text" id="client-name" placeholder="Nombre completo" required>
            <input type="tel" id="client-phone" placeholder="Número de WhatsApp" required>
            
            <div class="flex-between mt-2">
                <button class="btn-glass" onclick="prevStep(2)">Volver</button>
                <button class="btn-gold" style="width: auto;" onclick="confirmBooking()">Confirmar</button>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script src="{{ url_for('static', filename='js/main.js') }}"></script>
{% endblock %}
'''
with open(index_path, "w", encoding="utf-8") as f:
    f.write(new_index)

# 5. Update dashboard.html
dashboard_path = os.path.join(base, "templates/admin/dashboard.html")
new_dash = '''{% extends 'base.html' %}
{% block title %}Dashboard - Admin{% endblock %}

{% block content %}
<div class="admin-layout">
    <div class="sidebar">
        <div class="sidebar-logo mb-2">
            {% if settings.get('logo_path') %}
                <img src="{{ url_for('static', filename='img/' + settings.get('logo_path')) }}" alt="Logo">
            {% endif %}
            <h2 class="gold-text">Alejo Barber</h2>
        </div>
        <ul>
            <li><a href="{{ url_for('admin.dashboard') }}" class="active"><i data-lucide="layout-dashboard"></i> Dashboard</a></li>
            <li><a href="{{ url_for('admin.settings') }}"><i data-lucide="settings"></i> Configuración</a></li>
            <li><a href="{{ url_for('admin.users') }}"><i data-lucide="users"></i> Accesos</a></li>
            <li><a href="{{ url_for('admin.blocks') }}"><i data-lucide="calendar-off"></i> Bloqueos</a></li>
            <li class="mt-2"><a href="{{ url_for('admin.logout') }}"><i data-lucide="log-out"></i> Salir</a></li>
        </ul>
    </div>
    <div class="admin-content">
        <h2 class="mb-2">Resumen de Hoy</h2>
        
        <div class="stats-grid">
            <div class="glass-panel stat-card">
                <i data-lucide="dollar-sign" class="gold-text"></i>
                <p class="text-dim" style="margin-top:0.5rem">Caja Hoy</p>
                <h3>${{ caja_hoy }}</h3>
            </div>
            <div class="glass-panel stat-card">
                <i data-lucide="calendar" class="gold-text"></i>
                <p class="text-dim" style="margin-top:0.5rem">Turnos Hoy</p>
                <h3>{{ appointments_today }}</h3>
            </div>
            <div class="glass-panel stat-card">
                <i data-lucide="users" class="gold-text"></i>
                <p class="text-dim" style="margin-top:0.5rem">Clientes Totales</p>
                <h3>{{ total_clients }}</h3>
            </div>
        </div>

        <h3 class="mb-2">Agenda de Hoy</h3>
        <div class="table-container">
            {% if schedule %}
            <table>
                <thead>
                    <tr>
                        <th>Hora</th>
                        <th>Cliente</th>
                        <th>Servicio</th>
                        <th>Estado</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {% for a in schedule %}
                    <tr>
                        <td style="font-size: 1.1rem; font-weight: 600; color: var(--primary-gold);">{{ a.time }}</td>
                        <td>
                            <div>{{ a.client_name }}</div>
                            <div class="text-dim" style="font-size:0.85rem">{{ a.client_phone }}</div>
                        </td>
                        <td>{{ a.service_name }}</td>
                        <td><span class="badge {{ a.status }}">{{ a.status|capitalize }}</span></td>
                        <td class="actions-cell">
                            {% if a.status == 'pending' %}
                            <form method="POST" action="{{ url_for('admin.update_status', id=a.id) }}" style="margin:0;">
                                <input type="hidden" name="status" value="confirmed">
                                <button type="submit" class="btn-icon" title="Confirmar"><i data-lucide="check"></i></button>
                            </form>
                            {% endif %}
                            
                            <a href="https://wa.me/{{a.client_phone|replace('+', '')}}?text=Hola {{a.client_name}}, te recordamos tu turno para hoy a las {{a.time}} en Alejo Barber!" target="_blank" class="btn-icon" title="Enviar Recordatorio">
                                <i data-lucide="message-circle"></i>
                            </a>
                            
                            <form method="POST" action="{{ url_for('admin.update_status', id=a.id) }}" style="margin:0;">
                                <input type="hidden" name="status" value="cancelled">
                                <button type="submit" class="btn-icon delete" title="Cancelar Turno"><i data-lucide="x"></i></button>
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <div style="padding: 3rem; text-align: center;">
                <p class="text-dim">No hay turnos agendados para hoy.</p>
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
'''
with open(dashboard_path, "w", encoding="utf-8") as f:
    f.write(new_dash)


# Update other admin templates to have the sidebar logo
for t in ["settings.html", "users.html", "blocks.html"]:
    path = os.path.join(base, f"templates/admin/{t}")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # replace the h2
    content = content.replace('<h2 class="gold-text"><i data-lucide="scissors"></i> Alejo Barber</h2>', '''<div class="sidebar-logo mb-2">
            {% if settings.get('logo_path') %}
                <img src="{{ url_for('static', filename='img/' + settings.get('logo_path')) }}" alt="Logo">
            {% endif %}
            <h2 class="gold-text">Alejo Barber</h2>
        </div>''')
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

