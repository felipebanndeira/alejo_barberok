import os
import re
import shutil

base = r"c:\Users\usser\Documents\Alejo barber"

# 1. Update admin_routes.py
routes_path = os.path.join(base, "routes/admin_routes.py")
with open(routes_path, "r", encoding="utf-8") as f:
    routes = f.read()

finances_route = """
@admin_bp.route('/finances')
@login_required
def finances():
    db = get_db()
    today = datetime.now().strftime('%Y-%m-%d')
    
    appointments_today = db.execute("SELECT COUNT(*) FROM appointments WHERE date = ?", (today,)).fetchone()[0]
    
    total_clients = db.execute("SELECT COUNT(DISTINCT client_phone) FROM appointments").fetchone()[0]
    
    caja_hoy_app = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE a.date = ? AND a.status = 'confirmed'", (today,)).fetchone()[0]
    caja_hoy_app = caja_hoy_app if caja_hoy_app else 0
    caja_hoy_sales = db.execute("SELECT SUM(price) FROM sales WHERE date(created_at, 'localtime') = ?", (today,)).fetchone()[0]
    caja_hoy_sales = caja_hoy_sales if caja_hoy_sales else 0
    caja_hoy = caja_hoy_app + caja_hoy_sales
    
    sales_today = db.execute("SELECT * FROM sales WHERE date(created_at, 'localtime') = ? ORDER BY created_at DESC", (today,)).fetchall()
    
    gastos_hoy = db.execute("SELECT SUM(amount) FROM expenses WHERE date(created_at, 'localtime') = ?", (today,)).fetchone()[0]
    gastos_hoy_val = gastos_hoy if gastos_hoy else 0
    gastos_hoy_str = f"{gastos_hoy_val:,.2f}".replace(",", ".")
    
    net_profit = caja_hoy - gastos_hoy_val
    net_profit_str = f"{net_profit:,.2f}".replace(",", ".")
    
    caja_hoy = f"{caja_hoy:,.2f}".replace(",", ".")
    
    days_es = ['Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom']
    chart_labels = []
    chart_data = []
    
    for i in range(6, -1, -1):
        d_obj = datetime.now() - timedelta(days=i)
        d_str = d_obj.strftime('%Y-%m-%d')
        chart_labels.append(days_es[d_obj.weekday()])
        
        inc_app = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE a.date = ? AND a.status = 'confirmed'", (d_str,)).fetchone()[0]
        inc_app = inc_app if inc_app else 0
        inc_sales = db.execute("SELECT SUM(price) FROM sales WHERE date(created_at, 'localtime') = ?", (d_str,)).fetchone()[0]
        inc_sales = inc_sales if inc_sales else 0
        chart_data.append(inc_app + inc_sales)
        
    settings=dict(db.execute('SELECT key, value FROM settings').fetchall())
    
    return render_template('admin/finances.html', 
                           appointments_today=appointments_today, 
                           total_clients=total_clients, caja_hoy=caja_hoy,
                           gastos_hoy=gastos_hoy_str, net_profit=net_profit_str,
                           chart_labels=chart_labels, chart_data=chart_data,
                           settings=settings, sales=sales_today)
"""

if "@admin_bp.route('/finances')" not in routes:
    # Insert before update_status
    routes = routes.replace("@admin_bp.route('/appointments/<int:id>/status'", finances_route + "\n@admin_bp.route('/appointments/<int:id>/status'")

# Fix redirects to request.referrer in sales/expenses
routes = routes.replace("return redirect(url_for('admin.dashboard'))", "return redirect(request.referrer or url_for('admin.dashboard'))")

with open(routes_path, "w", encoding="utf-8") as f:
    f.write(routes)

# 2. Create finances.html from dashboard.html
dash_path = os.path.join(base, "templates/admin/dashboard.html")
finances_path = os.path.join(base, "templates/admin/finances.html")

shutil.copy2(dash_path, finances_path)

with open(finances_path, "r", encoding="utf-8") as f:
    fin = f.read()

# Delete Agenda from finances
agenda_pattern = r'<div class="flex-between mb-2">\s*<h3 class="space-font">Agenda de Hoy.*?<!-- MOBILE CARDS VIEW -->.*?</div>\s*</div>'
fin = re.sub(agenda_pattern, '', fin, flags=re.DOTALL)
fin = fin.replace('Dashboard - Admin', 'Finanzas - Admin')
fin = fin.replace('<h2 class="mb-2 space-font">Panel de Control</h2>', '<h2 class="mb-2 space-font">Caja y Estadísticas</h2>')
# Make Chart bigger
fin = fin.replace('<canvas id="incomeChart" height="80"></canvas>', '<canvas id="incomeChart" height="150"></canvas>')

with open(finances_path, "w", encoding="utf-8") as f:
    f.write(fin)

# 3. Clean up dashboard.html
with open(dash_path, "r", encoding="utf-8") as f:
    dash = f.read()

stats_pattern = r'<div class="stats-grid">.*?<canvas id="incomeChart" height="80"></canvas>\s*</div>'
dash = re.sub(stats_pattern, '', dash, flags=re.DOTALL)

sales_pattern = r'<div class="mt-2 flex-between mb-2">\s*<h3 class="space-font">Venta de Mostrador rApida</h3>.*?</table>\s*{% else %}\s*<div style="padding: 2rem; text-align: center; border: 1px dashed #333; border-radius: 8px;">\s*<p class="text-dim">No hay ventas registradas hoy.</p>\s*</div>\s*{% endif %}\s*</div>'
dash = re.sub(sales_pattern, '', dash, flags=re.DOTALL)
# It might fail due to exact matching, let's do it safer:
if "Venta de Mostrador r" in dash:
    parts = dash.split('<div class="mt-2 flex-between mb-2">')
    dash = parts[0] + "\n</div>\n" + dash.split('<!-- Modal Turno Manual -->')[1]
    dash = dash.replace("</div>\n\n</div>", "</div>")
    dash = dash.replace("</div>\n<div id=\"modal-turno\"", "<!-- Modal Turno Manual -->\n<div id=\"modal-turno\"")

# Fix script section in dashboard since chart is gone
chart_script = r'// Chart Logic.*?\}\);'
dash = re.sub(chart_script, '', dash, flags=re.DOTALL)

with open(dash_path, "w", encoding="utf-8") as f:
    f.write(dash)

# 4. Update sidebar links in ALL admin templates
admin_templates = ["dashboard.html", "finances.html", "settings.html", "users.html", "blocks.html"]
for t in admin_templates:
    path = os.path.join(base, "templates/admin", t)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Determine active class
        fin_active = ' class="active"' if t == 'finances.html' else ''
        dash_active = ' class="active"' if t == 'dashboard.html' else ''
        
        new_links = f"""<li><a href="{{{{ url_for('admin.dashboard') }}}}"{dash_active}>Agenda</a></li>
            <li><a href="{{{{ url_for('admin.finances') }}}}"{fin_active}>Finanzas</a></li>"""
            
        content = re.sub(r'<li><a href="\{\{ url_for\(\'admin\.dashboard\'\) \}\}".*?</a></li>', new_links, content)
        # Clear double active if necessary (for settings, users, etc.)
        if t not in ['dashboard.html', 'finances.html']:
            content = content.replace(dash_active, "")
            content = content.replace(fin_active, "")
            
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

# Update layout style for chart on mobile to not be constrained
css_path = os.path.join(base, "static/css/style.css")
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()
css = css.replace("canvas#incomeChart { width: 100% !important; max-height: 150px; }", "canvas#incomeChart { width: 100% !important; height: 250px !important; }")
with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)

