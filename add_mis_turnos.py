import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"

# 1. Update cliente_routes.py
routes_path = os.path.join(base, "routes/cliente_routes.py")
with open(routes_path, "r", encoding="utf-8") as f:
    routes = f.read()

new_route = """
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
            turnos = db.execute('''
                SELECT a.*, s.name as service_name, s.price 
                FROM appointments a 
                JOIN services s ON a.service_id = s.id 
                WHERE a.client_phone = ? 
                ORDER BY a.date DESC, a.time DESC
            ''', (phone,)).fetchall()
            
    return render_template('cliente/mis_turnos.html', settings=settings, turnos=turnos, searched=searched)
"""
if "/mis-turnos" not in routes:
    routes += new_route
    with open(routes_path, "w", encoding="utf-8") as f:
        f.write(routes)


# 2. Update index.html Header
index_path = os.path.join(base, "templates/cliente/index.html")
with open(index_path, "r", encoding="utf-8") as f:
    index = f.read()

header_old = """<div class="header-nav">
        <a href="#" class="active">Nuevo Turno</a>
    </div>"""
header_new = """<div class="header-nav">
        <a href="{{ url_for('cliente.index') }}" class="active">Nuevo Turno</a>
        <a href="{{ url_for('cliente.mis_turnos') }}">Mis Turnos</a>
    </div>"""

index = index.replace(header_old, header_new)
# Since the header is duplicated in HTML, just to be sure we'll write it out.
with open(index_path, "w", encoding="utf-8") as f:
    f.write(index)


# 3. Create mis_turnos.html
template_content = """{% extends 'base.html' %}

{% block content %}
<header class="top-header">
    <div class="header-logo">
        {% if settings.get('logo_path') %}
            <img src="{{ url_for('static', filename='img/' + settings.get('logo_path')) }}" alt="Logo">
        {% endif %}
        <span>{{ settings.get('barber_name', 'Alejo Barber') }}</span>
    </div>
    <div class="header-nav">
        <a href="{{ url_for('cliente.index') }}">Nuevo Turno</a>
        <a href="{{ url_for('cliente.mis_turnos') }}" class="active">Mis Turnos</a>
    </div>
</header>

<div class="container" style="margin-top: 3rem;">
    <h2 class="mb-2 space-font text-center">Consultá tus turnos</h2>
    <p class="text-dim text-center mb-2">Ingresá tu número de celular para ver tus reservas confirmadas y pendientes.</p>
    
    <div class="glass-panel" style="background: #0a0a0a; border: 1px solid #1a1a1a; padding: 2rem; border-radius: 12px; margin-bottom: 2rem;">
        <form method="POST" action="{{ url_for('cliente.mis_turnos') }}" style="display: flex; gap: 1rem; align-items: flex-end;">
            <div style="flex: 1;">
                <label style="color: var(--text-dim); margin-bottom: 0.5rem; display:block; font-size:0.9rem;">Número de Celular</label>
                <input type="tel" name="phone" placeholder="Ej: 3755123456" required style="margin: 0; background: #030303; border-color: #222;">
            </div>
            <div>
                <button type="submit" class="btn-gold" style="margin: 0; padding: 1rem 1.5rem; white-space: nowrap;">Buscar Turnos</button>
            </div>
        </form>
    </div>

    {% if searched %}
        {% if turnos %}
            <h3 class="mb-2 space-font text-center" style="margin-top: 3rem;">Historial de Turnos</h3>
            <div class="services-list">
                {% for t in turnos %}
                <div class="service-card" style="cursor: default; border-color: {% if t.status == 'cancelled' %}#dc3545{% elif t.status == 'confirmed' %}var(--primary-gold){% else %}#1a1a1a{% endif %};">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <h3 class="space-font mb-2">{{ t.service_name }}</h3>
                            <p class="text-dim" style="font-size: 0.95rem; margin-bottom: 0.3rem;"><i data-lucide="calendar" style="width: 14px; vertical-align: middle;"></i> {{ t.date }}</p>
                            <p class="text-dim" style="font-size: 0.95rem;"><i data-lucide="clock" style="width: 14px; vertical-align: middle;"></i> {{ t.time }}</p>
                        </div>
                        <div style="text-align: right;">
                            <span class="badge {{ t.status }} space-font" style="
                                display: inline-block; 
                                margin-bottom: 1rem;
                                padding: 0.4rem 0.8rem;
                                border-radius: 4px;
                                {% if t.status == 'pending' %}background: rgba(255,193,7,0.1); color:#ffc107; border: 1px solid rgba(255,193,7,0.2);{% endif %}
                                {% if t.status == 'confirmed' %}background: rgba(40,167,69,0.1); color:#28a745; border: 1px solid rgba(40,167,69,0.2);{% endif %}
                                {% if t.status == 'cancelled' %}background: rgba(220,53,69,0.1); color:#dc3545; border: 1px solid rgba(220,53,69,0.2);{% endif %}
                            ">
                                {% if t.status == 'pending' %}Pendiente{% endif %}
                                {% if t.status == 'confirmed' %}Confirmado{% endif %}
                                {% if t.status == 'cancelled' %}Cancelado{% endif %}
                            </span>
                            <br>
                            <span class="gold-text space-font" style="font-size: 1.2rem; font-weight: 600;">${{ "{:,}".format(t.price|int).replace(",", ".") }}</span>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        {% else %}
            <div class="text-center" style="margin-top: 3rem; padding: 2rem; border: 1px dashed #333; border-radius: 12px;">
                <i data-lucide="search-x" class="text-dim mb-2" style="width: 48px; height: 48px;"></i>
                <h3 class="space-font mb-2">No se encontraron turnos</h3>
                <p class="text-dim">No hay reservas asociadas a este número de celular.</p>
            </div>
        {% endif %}
    {% endif %}
</div>
{% endblock %}
"""

mis_turnos_path = os.path.join(base, "templates/cliente/mis_turnos.html")
with open(mis_turnos_path, "w", encoding="utf-8") as f:
    f.write(template_content)

