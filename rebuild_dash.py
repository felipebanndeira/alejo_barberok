import os

base = r"c:\Users\usser\Documents\Alejo barber"
dash_path = os.path.join(base, "templates/admin/dashboard.html")

html_content = """{% extends 'base.html' %}
{% block title %}Agenda - Admin{% endblock %}

{% block content %}
<div class="admin-layout">
    <aside class="sidebar">
        <div class="sidebar-logo">
            {% if settings.get('logo_path') %}
                <img src="{{ url_for('static', filename='img/' + settings.get('logo_path')) }}" alt="Logo">
            {% endif %}
            <h2 class="space-font">{{ settings.get('barber_name', 'Alejo Barber') }}</h2>
        </div>
        <ul>
            <li><a href="{{ url_for('admin.dashboard') }}" class="active"><i data-lucide="calendar"></i> Agenda</a></li>
            <li><a href="{{ url_for('admin.finances') }}"><i data-lucide="dollar-sign"></i> Caja</a></li>
            <li><a href="{{ url_for('admin.blocks') }}"><i data-lucide="clock"></i> Horarios</a></li>
            <li><a href="{{ url_for('admin.users') }}"><i data-lucide="users"></i> Accesos</a></li>
            <li><a href="{{ url_for('admin.settings') }}"><i data-lucide="settings"></i> Ajustes</a></li>
            <li class="sidebar-separator"></li>
            <li><a href="{{ url_for('admin.logout') }}"><i data-lucide="log-out"></i> Salir</a></li>
        </ul>
    </aside>
    
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
                                <button type="submit" class="btn-icon confirm" title="Confirmar Turno"><i data-lucide="check"></i></button>
                            </form>
                            {% endif %}
                            
                            <a href="https://wa.me/{{a.client_phone|replace('+', '')}}?text=Hola {{a.client_name}}, estoy con una pequeña demora. ¿Podrías venir unos 15 minutitos más tarde de tu turno de las {{a.time}}? ¡Gracias y disculpá!" target="_blank" class="btn-icon" title="Avisar Demora 15 min" style="color: #ffc107;">
                                <i data-lucide="clock"></i>
                            </a>
                            
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
            <div style="padding: 2rem; text-align: center;">
                <p class="text-dim">No hay turnos agendados para hoy.</p>
            </div>
            {% endif %}
        </div>

        <!-- MOBILE CARDS VIEW -->
        <div class="mobile-only mb-2">
            {% if schedule %}
                <div style="display: flex; flex-direction: column; gap: 1rem; width: 100%; align-items: stretch;">
                    <style>
                    .premium-card { background: #18181b; border-radius: 0.75rem; border: 1px solid #27272a; padding: 1.25rem; width: 100%; box-sizing: border-box; }
                    .pc-top { display: flex; justify-content: space-between; align-items: flex-start; }
                    .pc-time { font-size: 1.25rem; font-weight: 700; color: #facc15; font-family: 'Plus Jakarta Sans', sans-serif; line-height: 1.2; }
                    .pc-service { font-size: 0.875rem; color: #a1a1aa; margin-top: 0.25rem; }
                    .pc-client { text-align: right; }
                    .pc-name { font-size: 1rem; font-weight: 600; color: #ffffff; cursor: pointer; text-decoration: underline; text-decoration-color: #52525b; }
                    .pc-phone { font-size: 0.875rem; color: #a1a1aa; margin-top: 0.25rem; display: flex; align-items: center; justify-content: flex-end; gap: 4px; }
                    .pc-middle { margin-top: 0.75rem; display: flex; justify-content: flex-start; }
                    .pc-badge { border-radius: 9999px; padding: 0.25rem 0.75rem; font-size: 0.75rem; font-weight: 500; }
                    .pc-badge.pending { background: rgba(234, 179, 8, 0.1); color: #facc15; border: 1px solid rgba(234, 179, 8, 0.2); }
                    .pc-badge.confirmed { background: rgba(34, 197, 94, 0.1); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.2); }
                    .pc-badge.cancelled { background: rgba(239, 68, 68, 0.1); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.2); }
                    .pc-actions { border-top: 1px solid #27272a; padding-top: 0.75rem; margin-top: 0.75rem; display: flex; justify-content: flex-end; gap: 0.75rem; }
                    .pc-btn { width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; background: transparent; border: 1px solid #27272a; cursor: pointer; transition: background 0.2s, border-color 0.2s; padding: 0; }
                    .pc-btn:hover { background: #27272a; border-color: #3f3f46; }
                    .pc-btn.confirm { color: #22c55e; }
                    .pc-btn.delay { color: #eab308; }
                    .pc-btn.wa { color: #10b981; }
                    .pc-btn.cancel { color: #ef4444; }
                    .pc-btn svg { width: 18px !important; height: 18px !important; }
                    </style>
                    {% for a in schedule %}
                    <div class="premium-card">
                        <div class="pc-top">
                            <div>
                                <div class="pc-time">{{ a.time }}</div>
                                <div class="pc-service">{{ a.service_name }}</div>
                            </div>
                            <div class="pc-client">
                                <div class="pc-name" onclick="openClientModal('{{ a.client_phone }}', '{{ a.client_name }}')">{{ a.client_name }}</div>
                                <div class="pc-phone">
                                    <i data-lucide="phone" style="width: 12px; height: 12px; display:inline-block;"></i> {{ a.client_phone }}
                                </div>
                            </div>
                        </div>
                        <div class="pc-middle">
                            <span class="pc-badge {{ a.status }}">
                                {% if a.status == 'pending' %}Pendiente{% endif %}
                                {% if a.status == 'confirmed' %}Confirmado{% endif %}
                                {% if a.status == 'cancelled' %}Cancelado{% endif %}
                            </span>
                        </div>
                        <div class="pc-actions">
                            {% if a.status == 'pending' %}
                            <form method="POST" action="{{ url_for('admin.update_status', id=a.id) }}" style="margin:0;">
                                <input type="hidden" name="status" value="confirmed">
                                <button type="submit" class="pc-btn confirm" title="Confirmar"><i data-lucide="check"></i></button>
                            </form>
                            {% endif %}
                            
                            <a href="https://wa.me/{{a.client_phone|replace('+', '')}}?text=Hola {{a.client_name}}, estoy con una pequeña demora. ¿Podrías venir unos 15 minutitos más tarde de tu turno de las {{a.time}}? ¡Gracias y disculpá!" target="_blank" class="pc-btn delay" title="Avisar Demora 15m">
                                <i data-lucide="clock"></i>
                            </a>
                            
                            <a href="https://wa.me/{{a.client_phone|replace('+', '')}}?text=Hola {{a.client_name}}, te recuerdo tu turno de hoy a las {{a.time}} para el servicio de {{a.service_name}}." target="_blank" class="pc-btn wa" title="Enviar WhatsApp">
                                <i data-lucide="message-circle"></i>
                            </a>
                            
                            <form method="POST" action="{{ url_for('admin.update_status', id=a.id) }}" style="margin:0;">
                                <input type="hidden" name="status" value="cancelled">
                                <button type="submit" class="pc-btn cancel" title="Cancelar"><i data-lucide="x"></i></button>
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
    f.write(html_content)

print("Rebuilt dashboard.html fully clean.")
