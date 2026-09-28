import os

base = r"c:\Users\usser\Documents\Alejo barber"

files = {
    r"templates\admin\dashboard.html": '''{% extends 'base.html' %}
{% block title %}Dashboard - Admin{% endblock %}

{% block content %}
<div class="admin-layout">
    <div class="sidebar">
        <h2 class="gold-text"><i data-lucide="scissors"></i> Alejo Barber</h2>
        <ul>
            <li><a href="{{ url_for('admin.dashboard') }}" class="active"><i data-lucide="layout-dashboard"></i> Dashboard</a></li>
            <li><a href="{{ url_for('admin.settings') }}"><i data-lucide="settings"></i> Configuración</a></li>
            <li><a href="{{ url_for('admin.blocks') }}"><i data-lucide="calendar-off"></i> Bloqueos</a></li>
            <li class="mt-2"><a href="{{ url_for('admin.logout') }}"><i data-lucide="log-out"></i> Salir</a></li>
        </ul>
    </div>
    <div class="admin-content">
        <h2 class="mb-2">Dashboard de Hoy</h2>
        
        <div class="stats-grid">
            <div class="glass-panel stat-card">
                <i data-lucide="calendar" class="gold-text"></i>
                <h3>{{ appointments_today }}</h3>
                <p class="text-dim">Turnos Hoy</p>
            </div>
            <div class="glass-panel stat-card">
                <i data-lucide="users" class="gold-text"></i>
                <h3>{{ total_clients }}</h3>
                <p class="text-dim">Clientes Totales</p>
            </div>
        </div>

        <div class="glass-panel">
            <h3 class="mb-2">Agenda de Hoy</h3>
            {% if schedule %}
            <table>
                <thead>
                    <tr>
                        <th>Hora</th>
                        <th>Cliente</th>
                        <th>Teléfono</th>
                        <th>Servicio</th>
                        <th>Estado</th>
                        <th>Acción</th>
                    </tr>
                </thead>
                <tbody>
                    {% for a in schedule %}
                    <tr>
                        <td><strong>{{ a.time }}</strong></td>
                        <td>{{ a.client_name }}</td>
                        <td>{{ a.client_phone }}</td>
                        <td>{{ a.service_name }}</td>
                        <td><span class="badge {{ a.status }}">{{ a.status|capitalize }}</span></td>
                        <td>
                            <form method="POST" action="{{ url_for('admin.update_status', id=a.id) }}" style="display:inline;">
                                <select name="status" onchange="this.form.submit()" style="padding: 0.25rem; margin:0; width:auto;">
                                    <option value="pending" {% if a.status == 'pending' %}selected{% endif %}>Pendiente</option>
                                    <option value="confirmed" {% if a.status == 'confirmed' %}selected{% endif %}>Confirmar</option>
                                    <option value="cancelled" {% if a.status == 'cancelled' %}selected{% endif %}>Cancelar</option>
                                </select>
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <p class="text-dim text-center">No hay turnos para hoy.</p>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
''',
    r"templates\admin\settings.html": '''{% extends 'base.html' %}
{% block title %}Configuración - Admin{% endblock %}

{% block content %}
<div class="admin-layout">
    <div class="sidebar">
        <h2 class="gold-text"><i data-lucide="scissors"></i> Alejo Barber</h2>
        <ul>
            <li><a href="{{ url_for('admin.dashboard') }}"><i data-lucide="layout-dashboard"></i> Dashboard</a></li>
            <li><a href="{{ url_for('admin.settings') }}" class="active"><i data-lucide="settings"></i> Configuración</a></li>
            <li><a href="{{ url_for('admin.blocks') }}"><i data-lucide="calendar-off"></i> Bloqueos</a></li>
            <li class="mt-2"><a href="{{ url_for('admin.logout') }}"><i data-lucide="log-out"></i> Salir</a></li>
        </ul>
    </div>
    <div class="admin-content">
        <h2 class="mb-2">Configuración</h2>
        
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                <div style="color: #28a745; margin-bottom: 1rem;">{{ messages[0] }}</div>
            {% endif %}
        {% endwith %}

        <form method="POST" enctype="multipart/form-data">
            <div class="stats-grid">
                <div class="glass-panel">
                    <h3 class="mb-2"><i data-lucide="store" class="gold-text"></i> Negocio</h3>
                    <label>Nombre de la Barbería</label>
                    <input type="text" name="barber_name" value="{{ settings.get('barber_name', '') }}">
                    
                    <label>Logo (PNG/JPG)</label>
                    <input type="file" name="logo" accept="image/*">
                    {% if settings.get('logo_path') %}
                    <p class="text-dim text-sm mb-2">Logo actual: {{ settings.get('logo_path') }}</p>
                    {% endif %}
                    
                    <label>WhatsApp (Ej: 123456789)</label>
                    <input type="text" name="whatsapp" value="{{ settings.get('whatsapp', '') }}">
                    
                    <label>Porcentaje de Seña (%)</label>
                    <input type="number" name="deposit_percentage" value="{{ settings.get('deposit_percentage', '') }}">
                    
                    <label>Datos Bancarios</label>
                    <textarea name="bank_details" style="width:100%; height:100px; background:rgba(255,255,255,0.05); color:white; border:1px solid var(--glass-border); padding:1rem; border-radius:8px; margin-bottom:1rem; font-family:inherit;">{{ settings.get('bank_details', '') }}</textarea>
                </div>
                
                <div class="glass-panel">
                    <h3 class="mb-2"><i data-lucide="clock" class="gold-text"></i> Horarios (Lunes a Viernes)</h3>
                    <label>Mañana - Inicio</label>
                    <input type="time" name="hours_mon_fri_start_1" value="{{ settings.get('hours_mon_fri_start_1', '') }}">
                    <label>Mañana - Fin</label>
                    <input type="time" name="hours_mon_fri_end_1" value="{{ settings.get('hours_mon_fri_end_1', '') }}">
                    <hr style="border-color:var(--glass-border); margin:1rem 0;">
                    <label>Tarde - Inicio</label>
                    <input type="time" name="hours_mon_fri_start_2" value="{{ settings.get('hours_mon_fri_start_2', '') }}">
                    <label>Tarde - Fin</label>
                    <input type="time" name="hours_mon_fri_end_2" value="{{ settings.get('hours_mon_fri_end_2', '') }}">
                </div>
            </div>
            
            <button type="submit" class="btn-gold mt-2">Guardar Configuración</button>
        </form>
    </div>
</div>
{% endblock %}
''',
    r"templates\admin\blocks.html": '''{% extends 'base.html' %}
{% block title %}Bloqueos - Admin{% endblock %}

{% block content %}
<div class="admin-layout">
    <div class="sidebar">
        <h2 class="gold-text"><i data-lucide="scissors"></i> Alejo Barber</h2>
        <ul>
            <li><a href="{{ url_for('admin.dashboard') }}"><i data-lucide="layout-dashboard"></i> Dashboard</a></li>
            <li><a href="{{ url_for('admin.settings') }}"><i data-lucide="settings"></i> Configuración</a></li>
            <li><a href="{{ url_for('admin.blocks') }}" class="active"><i data-lucide="calendar-off"></i> Bloqueos</a></li>
            <li class="mt-2"><a href="{{ url_for('admin.logout') }}"><i data-lucide="log-out"></i> Salir</a></li>
        </ul>
    </div>
    <div class="admin-content">
        <h2 class="mb-2">Bloqueos de Agenda</h2>
        
        <div class="stats-grid">
            <div class="glass-panel">
                <h3 class="mb-2">Nuevo Bloqueo</h3>
                <form method="POST">
                    <label>Tipo de Bloqueo</label>
                    <select name="type" id="block-type" onchange="toggleBlockType()">
                        <option value="date">Fecha Específica</option>
                        <option value="recurring">Día Recurrente</option>
                    </select>
                    
                    <div id="date-input">
                        <label>Fecha</label>
                        <input type="date" name="date">
                    </div>
                    
                    <div id="recurring-input" style="display:none;">
                        <label>Día de la semana</label>
                        <select name="day_of_week">
                            <option value="0">Lunes</option>
                            <option value="1">Martes</option>
                            <option value="2">Miércoles</option>
                            <option value="3">Jueves</option>
                            <option value="4">Viernes</option>
                        </select>
                    </div>
                    
                    <label>Hora Inicio</label>
                    <input type="time" name="start_time" required>
                    <label>Hora Fin</label>
                    <input type="time" name="end_time" required>
                    
                    <button type="submit" class="btn-gold mt-2 w-100">Agregar Bloqueo</button>
                </form>
            </div>
            
            <div class="glass-panel">
                <h3 class="mb-2">Bloqueos Activos</h3>
                {% if blocks %}
                <table>
                    <thead>
                        <tr>
                            <th>Tipo / Día</th>
                            <th>Rango</th>
                            <th>Acción</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for b in blocks %}
                        <tr>
                            <td>
                                {% if b.type == 'date' %}
                                    Fecha: {{ b.date }}
                                {% else %}
                                    Recurrente: 
                                    {% if b.day_of_week == 0 %}Lunes{% endif %}
                                    {% if b.day_of_week == 1 %}Martes{% endif %}
                                    {% if b.day_of_week == 2 %}Miércoles{% endif %}
                                    {% if b.day_of_week == 3 %}Jueves{% endif %}
                                    {% if b.day_of_week == 4 %}Viernes{% endif %}
                                {% endif %}
                            </td>
                            <td>{{ b.start_time }} a {{ b.end_time }}</td>
                            <td>
                                <form method="POST" action="{{ url_for('admin.delete_block', id=b.id) }}">
                                    <button type="submit" class="btn-glass" style="padding:0.25rem 0.5rem;"><i data-lucide="trash-2" style="width:16px;"></i></button>
                                </form>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <p class="text-dim">No hay bloqueos activos.</p>
                {% endif %}
            </div>
        </div>
    </div>
</div>

<script>
function toggleBlockType() {
    const type = document.getElementById('block-type').value;
    if (type === 'date') {
        document.getElementById('date-input').style.display = 'block';
        document.getElementById('recurring-input').style.display = 'none';
    } else {
        document.getElementById('date-input').style.display = 'none';
        document.getElementById('recurring-input').style.display = 'block';
    }
}
</script>
{% endblock %}
'''
}

for path, content in files.items():
    full_path = os.path.join(base, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
