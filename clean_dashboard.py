import os

base = r"c:\Users\usser\Documents\Alejo barber"
dash_path = os.path.join(base, "templates/admin/dashboard.html")

content = """{% extends 'base.html' %}
{% block title %}Agenda - Admin{% endblock %}

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
            <li><a href="{{ url_for('admin.dashboard') }}" class="active">Agenda</a></li>
            <li><a href="{{ url_for('admin.finances') }}">Finanzas</a></li>
            <li><a href="{{ url_for('admin.settings') }}" {% if request.endpoint == 'admin.settings' %}class="active"{% endif %}>Configuración</a></li>
            <li><a href="{{ url_for('admin.users') }}" {% if request.endpoint == 'admin.users' %}class="active"{% endif %}>Accesos</a></li>
            <li><a href="{{ url_for('admin.blocks') }}">Bloqueos</a></li>
            <div class="sidebar-separator"></div>
            <li><a href="{{ url_for('admin.logout') }}">Salir</a></li>
        </ul>
    </div>
    
    <div class="admin-content">
        <h2 class="mb-2 space-font">Agenda</h2>
        
        <div class="flex-between mb-2">
            <h3 class="space-font">Agenda de Hoy</h3>
            <button onclick="document.getElementById('modal-turno').style.display='flex'" class="btn-gold d-none-mobile" style="padding: 0.5rem 1rem; font-size: 0.9rem;"><i data-lucide="plus" style="width:16px; margin-right:5px; vertical-align:text-bottom;"></i> Agendar Manual</button>
        </div>
        <button onclick="document.getElementById('modal-turno').style.display='flex'" class="btn-gold d-none-desktop w-full mb-2" style="padding: 1rem; font-size: 1rem;"><i data-lucide="plus" style="width:18px; margin-right:5px; vertical-align:text-bottom;"></i> Agendar Manual</button>

        <div class="table-container desktop-only">
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
                        <td class="space-font" style="font-size: 1.05rem; font-weight: 500; color: var(--primary-gold);">{{ a.time }}</td>
                        <td>
                            <div style="cursor: pointer; text-decoration: underline; color: var(--text-light);" onclick="openClientModal('{{ a.client_phone }}', '{{ a.client_name }}')">{{ a.client_name }}</div>
                            <div class="text-dim" style="font-size:0.85rem">{{ a.client_phone }}</div>
                        </td>
                        <td>{{ a.service_name }}</td>
                        <td><span class="badge {{ a.status }}">
                            {% if a.status == 'pending' %}Pendiente{% endif %}
                            {% if a.status == 'confirmed' %}Confirmado{% endif %}
                            {% if a.status == 'cancelled' %}Cancelado{% endif %}
                        </span></td>
                        <td class="actions-cell">
                            {% if a.status == 'pending' %}
                            <form method="POST" action="{{ url_for('admin.update_status', id=a.id) }}" style="margin:0;">
                                <input type="hidden" name="status" value="confirmed">
                                <button type="submit" class="btn-icon" title="Confirmar"><i data-lucide="check"></i></button>
                            </form>
                            {% endif %}
                            
                            <a href="https://wa.me/{{a.client_phone|replace('+', '')}}?text=Hola {{a.client_name}}, te recuerdo tu turno de hoy a las {{a.time}} para el servicio de {{a.service_name}}." target="_blank" class="btn-icon" title="Enviar Recordatorio">
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

        <!-- MOBILE CARDS VIEW -->
        <div class="mobile-only mb-2">
            {% if schedule %}
                <div style="display: flex; flex-direction: column; gap: 1rem;">
                {% for a in schedule %}
                    <div class="glass-panel" style="padding: 1rem; border-color: {% if a.status == 'cancelled' %}#dc3545{% elif a.status == 'confirmed' %}var(--primary-gold){% else %}#222{% endif %};">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                            <div class="space-font gold-text" style="font-size: 1.3rem; font-weight: 700;">{{ a.time }}</div>
                            <div style="text-align: right;">
                                <div style="font-weight: 600; font-size: 1.1rem; color: var(--text-light);" onclick="openClientModal('{{ a.client_phone }}', '{{ a.client_name }}')">{{ a.client_name }}</div>
                                <div class="text-dim" style="font-size: 0.9rem;">{{ a.client_phone }}</div>
                            </div>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding-bottom: 0.8rem; border-bottom: 1px solid rgba(255,255,255,0.05);">
                            <div class="text-dim" style="font-size: 1.05rem;">{{ a.service_name }}</div>
                            <span class="badge {{ a.status }}" style="margin:0;">
                                {% if a.status == 'pending' %}Pendiente{% endif %}
                                {% if a.status == 'confirmed' %}Confirmado{% endif %}
                                {% if a.status == 'cancelled' %}Cancelado{% endif %}
                            </span>
                        </div>
                        <div style="display: flex; justify-content: space-between; gap: 0.5rem;">
                            {% if a.status == 'pending' %}
                            <form method="POST" action="{{ url_for('admin.update_status', id=a.id) }}" style="margin:0; flex:1;">
                                <input type="hidden" name="status" value="confirmed">
                                <button type="submit" class="btn-outline" style="width:100%; border-color:rgba(40,167,69,0.3); color:#28a745; padding:0.8rem; background:rgba(40,167,69,0.05);"><i data-lucide="check" style="width:20px;"></i></button>
                            </form>
                            {% endif %}
                            
                            <a href="https://wa.me/{{a.client_phone|replace('+', '')}}?text=Hola {{a.client_name}}, te recuerdo tu turno de hoy a las {{a.time}} para el servicio de {{a.service_name}}." target="_blank" class="btn-outline" style="flex:1; text-align:center; padding:0.8rem; border-color:rgba(255,204,0,0.3); color:var(--primary-gold); background:rgba(255,204,0,0.05);">
                                <i data-lucide="message-circle" style="width:20px; display:inline-block; vertical-align:middle;"></i>
                            </a>
                            
                            <form method="POST" action="{{ url_for('admin.update_status', id=a.id) }}" style="margin:0; flex:1;">
                                <input type="hidden" name="status" value="cancelled">
                                <button type="submit" class="btn-outline delete" style="width:100%; padding:0.8rem; border-color:rgba(220,53,69,0.3); color:#dc3545; background:rgba(220,53,69,0.05);"><i data-lucide="x" style="width:20px;"></i></button>
                            </form>
                        </div>
                    </div>
                {% endfor %}
                </div>
            {% else %}
                <div style="padding: 2rem; text-align: center; border: 1px dashed #333; border-radius: 8px;">
                    <p class="text-dim">No hay turnos agendados para hoy.</p>
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
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

<!-- Modal Cliente -->
<div id="modal-cliente" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); z-index:1000; justify-content:center; align-items:center;">
    <div class="glass-panel" style="width: 400px; background: #050505;">
        <div class="flex-between mb-2">
            <h3 class="space-font" id="modal-client-name">Perfil de Cliente</h3>
            <button class="btn-icon" onclick="document.getElementById('modal-cliente').style.display='none'"><i data-lucide="x"></i></button>
        </div>
        <div id="client-loading" class="text-dim">Cargando...</div>
        <div id="client-data" style="display:none;">
            <div style="margin-bottom: 1rem;">
                <p class="text-dim">Visitas este mes</p>
                <h2 class="space-font" id="client-visits">0</h2>
            </div>
            <div style="margin-bottom: 1rem;">
                <p class="text-dim">Total gastado (LTV)</p>
                <h2 class="space-font gold-text" id="client-ltv">$0</h2>
            </div>
            <div>
                <p class="text-dim">Faltas sin cancelar (No-Shows)</p>
                <h2 class="space-font" id="client-noshows">0</h2>
            </div>
        </div>
    </div>
</div>

<script>
// Client Modal Logic
async function openClientModal(phone, name) {
    document.getElementById('modal-cliente').style.display = 'flex';
    document.getElementById('modal-client-name').textContent = name;
    document.getElementById('client-loading').style.display = 'block';
    document.getElementById('client-data').style.display = 'none';
    
    try {
        const res = await fetch(`/admin/api/client/${phone}`);
        const data = await res.json();
        
        document.getElementById('client-visits').textContent = data.visits;
        document.getElementById('client-ltv').textContent = '$' + data.ltv.toLocaleString('es-AR');
        
        const noShowsEl = document.getElementById('client-noshows');
        noShowsEl.textContent = data.no_shows;
        if(data.no_shows > 0) {
            noShowsEl.style.color = '#dc3545';
        } else {
            noShowsEl.style.color = 'var(--text-light)';
        }
        
        document.getElementById('client-loading').style.display = 'none';
        document.getElementById('client-data').style.display = 'block';
    } catch(e) {
        document.getElementById('client-loading').textContent = 'Error al cargar';
    }
}
</script>
{% endblock %}
"""

with open(dash_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Dashboard cleaned up.")
