import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "routes/admin_routes.py")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# We will add logic to fetch monthly history
# We need to get all unique months from appointments, sales, and expenses, and calculate totals per month.
logic = """
    # HISTORIAL MENSUAL
    # Get all months where there is activity
    months_query = db.execute('''
        SELECT DISTINCT strftime('%Y-%m', date) as m FROM appointments WHERE status='confirmed'
        UNION
        SELECT DISTINCT strftime('%Y-%m', created_at, 'localtime') as m FROM sales
        UNION
        SELECT DISTINCT strftime('%Y-%m', created_at, 'localtime') as m FROM expenses
    ''').fetchall()
    
    monthly_history = []
    for row in months_query:
        m = row['m']
        if not m: continue
        
        # Calculate for this month `m`
        c_app = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE a.date LIKE ? AND a.status = 'confirmed'", (m + '%',)).fetchone()[0] or 0
        c_sales = db.execute("SELECT SUM(price) FROM sales WHERE strftime('%Y-%m', created_at, 'localtime') = ?", (m,)).fetchone()[0] or 0
        c_exp = db.execute("SELECT SUM(amount) FROM expenses WHERE strftime('%Y-%m', created_at, 'localtime') = ?", (m,)).fetchone()[0] or 0
        
        c_total = c_app + c_sales
        c_net = c_total - c_exp
        
        monthly_history.append({
            'month': m,
            'caja': f"{c_total:,.2f}".replace(",", "."),
            'gastos': f"{c_exp:,.2f}".replace(",", "."),
            'neto': f"{c_net:,.2f}".replace(",", ".")
        })
        
    # Sort history descending (newest first)
    monthly_history.sort(key=lambda x: x['month'], reverse=True)
"""

# Insert before settings = dict(...)
content = content.replace("settings=dict(db.execute('SELECT key, value FROM settings').fetchall())", logic + "\n    settings=dict(db.execute('SELECT key, value FROM settings').fetchall())")

# Update render_template
old_render = """                           settings=settings, sales=sales_today,
                           caja_mes=caja_mes_str, gastos_mes=gastos_mes_str, net_mes=net_profit_mes_str)"""

new_render = """                           settings=settings, sales=sales_today,
                           caja_mes=caja_mes_str, gastos_mes=gastos_mes_str, net_mes=net_profit_mes_str,
                           monthly_history=monthly_history)"""

content = content.replace(old_render, new_render)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
