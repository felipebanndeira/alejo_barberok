import os
import sqlite3
from datetime import datetime

base = r"c:\Users\usser\Documents\Alejo barber"
db_path = os.path.join(base, "barber.db")

# 1. Update Database
conn = sqlite3.connect(db_path)
conn.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        price REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()
conn.close()

# 2. Update style.css for sidebar icons and colors
css_path = os.path.join(base, "static/css/style.css")
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# Make sidebar icons grey by default, gold when active
if ".sidebar a i {" not in css:
    css += "\n.sidebar a i { color: #9CA3AF; transition: color 0.2s; }\n.sidebar a:hover i, .sidebar a.active i { color: var(--primary-gold); }\n"
if ".btn-icon i {" not in css:
    css += "\n.btn-icon i { color: #9CA3AF; }\n.btn-icon:hover i { color: var(--primary-gold); }\n.btn-icon.delete:hover i { color: #dc3545; }\n"

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)

# 3. Update admin_routes.py
routes_path = os.path.join(base, "routes/admin_routes.py")
with open(routes_path, "r", encoding="utf-8") as f:
    routes = f.read()

# Update caja_hoy calculation to include sales
dashboard_calc_old = """
    # Calculate Caja
    caja = db.execute(\"""
        SELECT SUM(s.price) 
        FROM appointments a
        JOIN services s ON a.service_id = s.id
        WHERE a.date = ? AND a.status = 'confirmed'
    \""", (today,)).fetchone()[0]
    caja_hoy = f"{caja:,}".replace(',', '.') if caja else '0'
"""

dashboard_calc_new = """
    # Calculate Caja from appointments
    caja_app = db.execute(\"""
        SELECT SUM(s.price) 
        FROM appointments a
        JOIN services s ON a.service_id = s.id
        WHERE a.date = ? AND a.status = 'confirmed'
    \""", (today,)).fetchone()[0]
    caja_app = caja_app if caja_app else 0

    # Get today's sales
    sales_today = db.execute("SELECT * FROM sales WHERE date(created_at, 'localtime') = ?", (today,)).fetchall()
    caja_sales = sum(s['price'] for s in sales_today)
    
    caja_total = caja_app + caja_sales
    caja_hoy = f"{caja_total:g}".replace('.', ',') if caja_total < 1000 else f"{caja_total:,.0f}".replace(',', '.')
"""

if "caja_total = caja_app + caja_sales" not in routes:
    routes = routes.replace(dashboard_calc_old, dashboard_calc_new)

# Pass sales_today to template
if "sales=sales_today" not in routes:
    routes = routes.replace(
        "schedule=schedule, settings=settings)",
        "schedule=schedule, settings=settings, sales=sales_today)"
    )

# Add sales routes
sales_routes = """
@admin_bp.route('/sales/add', methods=['POST'])
@login_required
def add_sale():
    product_name = request.form['product_name']
    price = request.form['price']
    db = get_db()
    db.execute("INSERT INTO sales (product_name, price) VALUES (?, ?)", (product_name, price))
    db.commit()
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/sales/<int:id>/delete', methods=['POST'])
@login_required
def delete_sale(id):
    db = get_db()
    db.execute("DELETE FROM sales WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for('admin.dashboard'))
"""
if "/sales/add" not in routes:
    routes += sales_routes

with open(routes_path, "w", encoding="utf-8") as f:
    f.write(routes)


# 4. Update dashboard.html to add Sales module
dash_path = os.path.join(base, "templates/admin/dashboard.html")
with open(dash_path, "r", encoding="utf-8") as f:
    dash = f.read()

sales_html = """
        <div class="mt-2 flex-between mb-2">
            <h3 class="space-font">Ventas de Insumos</h3>
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
"""

# Insert sales module at the end of the content area
if "Ventas de Insumos" not in dash:
    dash = dash.replace(
        "    </div>\n</div>\n{% endblock %}",
        sales_html + "\n    </div>\n</div>\n{% endblock %}"
    )
    with open(dash_path, "w", encoding="utf-8") as f:
        f.write(dash)

