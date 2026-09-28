import os

base = r"c:\Users\usser\Documents\Alejo barber"
finances_path = os.path.join(base, "templates/admin/finances.html")

content = """{% extends 'base.html' %}
{% block title %}Caja - Admin{% endblock %}

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
            <li><a href="{{ url_for('admin.dashboard') }}">Agenda</a></li>
            <li><a href="{{ url_for('admin.finances') }}" class="active">Caja</a></li>
            <li><a href="{{ url_for('admin.settings') }}" {% if request.endpoint == 'admin.settings' %}class="active"{% endif %}>Configuración</a></li>
            <li><a href="{{ url_for('admin.users') }}" {% if request.endpoint == 'admin.users' %}class="active"{% endif %}>Accesos</a></li>
            <li><a href="{{ url_for('admin.blocks') }}">Bloqueos</a></li>
            <div class="sidebar-separator"></div>
            <li><a href="{{ url_for('admin.logout') }}">Salir</a></li>
        </ul>
    </div>
    
    <div class="admin-content">
        <h2 class="mb-2 space-font">Caja y Estadísticas</h2>
        
        <div class="stats-grid mb-2">
            <div class="glass-panel stat-card" style="display: flex; justify-content: space-between;">
                <div>
                    <p class="text-dim">Caja Hoy</p>
                    <h3 class="space-font" style="font-weight: 700;">${{ caja_hoy }}</h3>
                </div>
                <button onclick="document.getElementById('modal-gasto').style.display='flex'" class="btn-outline" style="font-size:0.8rem; border:1px solid #333; border-radius:4px; padding:0.4rem 0.6rem;">+ Cargar Gasto</button>
            </div>
            <div class="glass-panel stat-card">
                <p class="text-dim">Ganancia Neta</p>
                <h3 class="space-font" style="font-weight: 700; color: var(--primary-gold);">${{ net_profit }}</h3>
            </div>
            <div class="glass-panel stat-card">
                <p class="text-dim">Turnos Hoy</p>
                <h3 class="space-font" style="font-weight: 700;">{{ appointments_today }}</h3>
            </div>
        </div>

        <div class="glass-panel mb-2" style="padding: 1.5rem;">
            <h3 class="space-font mb-2" style="font-size: 1.1rem;">Ingresos Últimos 7 días</h3>
            <canvas id="incomeChart" height="250"></canvas>
        </div>

        <div class="mt-2 flex-between mb-2">
            <h3 class="space-font">Venta de Mostrador rápida</h3>
        </div>
        
        <div class="glass-panel mb-2" style="padding: 1.5rem;">
            <form method="POST" action="{{ url_for('admin.add_sale') }}" style="display: flex; gap: 1rem; align-items: flex-end;">
                <div style="flex: 2;">
                    <label>Producto / Insumo</label>
                    <input type="text" name="product_name" placeholder="Ej: Cera mate" required style="margin: 0;">
                </div>
                <div style="flex: 1;">
                    <label>Precio</label>
                    <input type="number" step="0.01" name="price" placeholder="Ej: 5000" required style="margin: 0;">
                </div>
                <div>
                    <button type="submit" class="btn-gold" style="margin: 0; padding: 1rem 1.5rem;"><i data-lucide="plus" style="width:18px; margin-right: 5px; vertical-align: text-bottom; color: #000;"></i> Agregar Venta</button>
                </div>
            </form>
        </div>

        <div class="table-container">
            {% if sales %}
            <table>
                <thead>
                    <tr>
                        <th>Producto</th>
                        <th>Precio</th>
                        <th>Hora de carga</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {% for s in sales %}
                    <tr>
                        <td>{{ s.product_name }}</td>
                        <td class="space-font" style="font-weight: 500; color: var(--primary-gold);">${{ "{:,}".format(s.price|int).replace(",", ".") }}</td>
                        <td class="text-dim">{{ s.created_at.split(' ')[1][:5] }}</td>
                        <td class="actions-cell">
                            <form method="POST" action="{{ url_for('admin.delete_sale', id=s.id) }}" style="margin:0;">
                                <button type="submit" class="btn-icon delete" title="Eliminar Venta"><i data-lucide="trash-2"></i></button>
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <div style="padding: 2rem; text-align: center;">
                <p class="text-dim">No hay ventas registradas hoy.</p>
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<!-- Modal Gasto -->
<div id="modal-gasto" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); z-index:1000; justify-content:center; align-items:center;">
    <div class="glass-panel" style="width: 400px; background: #050505;">
        <div class="flex-between mb-2">
            <h3 class="space-font">Cargar Gasto (Caja Chica)</h3>
            <button class="btn-icon" onclick="document.getElementById('modal-gasto').style.display='none'"><i data-lucide="x"></i></button>
        </div>
        <form method="POST" action="{{ url_for('admin.add_expense') }}">
            <label>Concepto</label>
            <input type="text" name="concept" placeholder="Ej: Luz, Bebidas" required>
            <label>Monto</label>
            <input type="number" step="0.01" name="amount" required>
            <button type="submit" class="btn-gold">Guardar Gasto</button>
        </form>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
// Chart Logic
document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('incomeChart');
    if(ctx) {
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: {{ chart_labels | safe }},
                datasets: [{
                    label: 'Ingresos ($)',
                    data: {{ chart_data | safe }},
                    borderColor: '#FFCC00',
                    backgroundColor: 'rgba(255, 204, 0, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                plugins: { legend: { display: false } },
                scales: {
                    y: { beginAtZero: true, grid: { color: '#1a1a1a' }, ticks: { color: '#7a7a7a' } },
                    x: { grid: { display: false }, ticks: { color: '#7a7a7a' } }
                }
            }
        });
    }
});
</script>
{% endblock %}
"""

with open(finances_path, "w", encoding="utf-8") as f:
    f.write(content)

# Update sidebar in all files to "Caja" instead of "Finanzas"
admin_templates = ["dashboard.html", "finances.html", "settings.html", "users.html", "blocks.html"]
for t in admin_templates:
    path = os.path.join(base, "templates/admin", t)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        c = c.replace(">Finanzas<", ">Caja<")
        with open(path, "w", encoding="utf-8") as f:
            f.write(c)

