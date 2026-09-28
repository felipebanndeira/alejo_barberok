import os
import sqlite3
import re
from datetime import datetime, timedelta

base = r"c:\Users\usser\Documents\Alejo barber"
db_path = os.path.join(base, "barber.db")

# 1. Update DB (Add expenses table)
conn = sqlite3.connect(db_path)
conn.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        concept TEXT NOT NULL,
        amount REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()
conn.close()

# 2. Rewrite admin_routes.py to include new logic
routes_path = os.path.join(base, "routes/admin_routes.py")
with open(routes_path, "r", encoding="utf-8") as f:
    routes = f.read()

dashboard_logic_new = """
    # Calculate Caja from appointments
    caja_app = db.execute(\"""
        SELECT SUM(s.price) 
        FROM appointments a
        JOIN services s ON a.service_id = s.id
        WHERE a.date = ? AND a.status = 'confirmed'
    \""", (today,)).fetchone()[0]
    caja_app = caja_app if caja_app else 0

    # Get today's sales (Venta Mostrador)
    sales_today = db.execute("SELECT * FROM sales WHERE date(created_at, 'localtime') = ?", (today,)).fetchall()
    caja_sales = sum(s['price'] for s in sales_today)
    
    caja_total = caja_app + caja_sales
    caja_hoy = f"{caja_total:g}".replace('.', ',') if caja_total < 1000 else f"{caja_total:,.0f}".replace(',', '.')

    # Get today's expenses
    expenses_today = db.execute("SELECT * FROM expenses WHERE date(created_at, 'localtime') = ?", (today,)).fetchall()
    gastos_total = sum(e['amount'] for e in expenses_today)
    gastos_hoy_str = f"{gastos_total:g}".replace('.', ',') if gastos_total < 1000 else f"{gastos_total:,.0f}".replace(',', '.')
    
    # Net Profit
    net_profit = caja_total - gastos_total
    net_profit_str = f"{net_profit:g}".replace('.', ',') if abs(net_profit) < 1000 else f"{net_profit:,.0f}".replace(',', '.')

    # Chart Data (Last 7 Days Income)
    chart_labels = []
    chart_data = []
    days_es = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
    for i in range(6, -1, -1):
        d_obj = datetime.now() - timedelta(days=i)
        d_str = d_obj.strftime('%Y-%m-%d')
        chart_labels.append(days_es[d_obj.weekday()])
        
        # income for d_str
        inc_app = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE a.date = ? AND a.status = 'confirmed'", (d_str,)).fetchone()[0]
        inc_app = inc_app if inc_app else 0
        inc_sales = db.execute("SELECT SUM(price) FROM sales WHERE date(created_at, 'localtime') = ?", (d_str,)).fetchone()[0]
        inc_sales = inc_sales if inc_sales else 0
        chart_data.append(inc_app + inc_sales)
"""

# Replace old calculate logic with new
old_calc_pattern = r"# Calculate Caja from appointments.*?caja_hoy = .*?\n"
routes = re.sub(old_calc_pattern, dashboard_logic_new, routes, flags=re.DOTALL)

# Add new vars to render_template
old_render = r"render_template\('admin/dashboard.html',\s*appointments_today=appointments_today,\s*total_clients=total_clients,\s*caja_hoy=caja_hoy,\s*schedule=schedule,\s*settings=settings,\s*sales=sales_today\)"
new_render = """render_template('admin/dashboard.html', 
                           appointments_today=appointments_today, 
                           total_clients=total_clients, caja_hoy=caja_hoy,
                           gastos_hoy=gastos_hoy_str, net_profit=net_profit_str,
                           chart_labels=chart_labels, chart_data=chart_data,
                           schedule=schedule, settings=settings, sales=sales_today, expenses=expenses_today)"""
routes = re.sub(old_render, new_render, routes)

# Add API routes for Expenses and Client Profile
new_routes = """
@admin_bp.route('/expenses/add', methods=['POST'])
@login_required
def add_expense():
    concept = request.form['concept']
    amount = request.form['amount']
    db = get_db()
    db.execute("INSERT INTO expenses (concept, amount) VALUES (?, ?)", (concept, amount))
    db.commit()
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/api/client/<phone>')
@login_required
def get_client(phone):
    db = get_db()
    current_month = datetime.now().strftime('%Y-%m')
    
    # Visits this month
    visits = db.execute("SELECT COUNT(*) FROM appointments WHERE client_phone = ? AND status = 'confirmed' AND date LIKE ?", (phone, f"{current_month}%")).fetchone()[0]
    
    # LTV
    ltv = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE a.client_phone = ? AND a.status = 'confirmed'", (phone,)).fetchone()[0]
    ltv = ltv if ltv else 0
    
    # No shows
    no_shows = db.execute("SELECT COUNT(*) FROM appointments WHERE client_phone = ? AND status = 'cancelled'", (phone,)).fetchone()[0]
    
    return {"visits": visits, "ltv": ltv, "no_shows": no_shows}
"""
if "/expenses/add" not in routes:
    routes += new_routes

with open(routes_path, "w", encoding="utf-8") as f:
    f.write(routes)


# 3. Update dashboard.html
dash_path = os.path.join(base, "templates/admin/dashboard.html")
with open(dash_path, "r", encoding="utf-8") as f:
    dash = f.read()

# Add Chart.js
if "cdn.jsdelivr.net/npm/chart.js" not in dash:
    dash = dash.replace("{% block scripts %}", "{% block scripts %}\n<script src=\"https://cdn.jsdelivr.net/npm/chart.js\"></script>")
    if "{% block scripts %}" not in dash: # if block scripts wasn't there
        dash += "\n{% block scripts %}\n<script src=\"https://cdn.jsdelivr.net/npm/chart.js\"></script>\n{% endblock %}"

# Update stats grid to include Expenses and Net Profit
stats_grid_old = r'<div class="stats-grid">.*?</div>\s*<h3 class="mb-2 space-font">Agenda de Hoy</h3>'
stats_grid_new = """<div class="stats-grid">
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
            <h3 class="space-font mb-2" style="font-size: 1.1rem;">Ingresos últimos 7 días</h3>
            <canvas id="incomeChart" height="80"></canvas>
        </div>

        <h3 class="mb-2 space-font">Agenda de Hoy</h3>"""
dash = re.sub(stats_grid_old, stats_grid_new, dash, flags=re.DOTALL)

# Update WhatsApp Message
dash = re.sub(r'href="https://wa.me/[^"]+"', r'href="https://wa.me/{{a.client_phone|replace(\'+\', \'\')}}?text=Hola {{a.client_name}}, te recuerdo tu turno de hoy a las {{a.time}} para el servicio de {{a.service_name}}. ¡Te espero!"', dash)

# Rename "Ventas de Insumos" to "Venta de Mostrador rápida"
dash = dash.replace("Ventas de Insumos", "Venta de Mostrador rápida")

# Make client name clickable
dash = dash.replace('<div>{{ a.client_name }}</div>', '<div style="cursor: pointer; text-decoration: underline; color: var(--text-light);" onclick="openClientModal(\'{{ a.client_phone }}\', \'{{ a.client_name }}\')">{{ a.client_name }}</div>')

# Add Modals and Chart Logic at the end
modals_script = """
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
"""

if "id=\"modal-gasto\"" not in dash:
    dash = dash.replace("{% endblock %}", modals_script + "\n{% endblock %}")

with open(dash_path, "w", encoding="utf-8") as f:
    f.write(dash)

