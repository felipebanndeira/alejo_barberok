import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "routes/admin_routes.py")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# Find the finances logic end
target = "net_profit = caja_hoy - gastos_hoy_val"
monthly_logic = """net_profit = caja_hoy - gastos_hoy_val
    
    current_month = datetime.now().strftime('%Y-%m')
    
    caja_mes_app = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE a.date LIKE ? AND a.status = 'confirmed'", (current_month + '%',)).fetchone()[0]
    caja_mes_app = caja_mes_app if caja_mes_app else 0
    
    caja_mes_sales = db.execute("SELECT SUM(price) FROM sales WHERE strftime('%Y-%m', created_at, 'localtime') = ?", (current_month,)).fetchone()[0]
    caja_mes_sales = caja_mes_sales if caja_mes_sales else 0
    
    caja_mes = caja_mes_app + caja_mes_sales
    
    gastos_mes = db.execute("SELECT SUM(amount) FROM expenses WHERE strftime('%Y-%m', created_at, 'localtime') = ?", (current_month,)).fetchone()[0]
    gastos_mes = gastos_mes if gastos_mes else 0
    
    net_profit_mes = caja_mes - gastos_mes
    
    caja_mes_str = f"{caja_mes:,.2f}".replace(",", ".")
    gastos_mes_str = f"{gastos_mes:,.2f}".replace(",", ".")
    net_profit_mes_str = f"{net_profit_mes:,.2f}".replace(",", ".")
"""

content = content.replace(target, monthly_logic)

# Update render_template to pass the new variables
old_render = """return render_template('admin/finances.html', 
                           appointments_today=appointments_today,
                           total_clients=total_clients, caja_hoy=caja_hoy,
                           gastos_hoy=gastos_hoy_str, net_profit=net_profit_str,
                           chart_labels=chart_labels, chart_data=chart_data,
                           settings=settings, sales=sales_today)"""

new_render = """return render_template('admin/finances.html', 
                           appointments_today=appointments_today,
                           total_clients=total_clients, caja_hoy=caja_hoy,
                           gastos_hoy=gastos_hoy_str, net_profit=net_profit_str,
                           chart_labels=chart_labels, chart_data=chart_data,
                           settings=settings, sales=sales_today,
                           caja_mes=caja_mes_str, gastos_mes=gastos_mes_str, net_mes=net_profit_mes_str)"""

content = content.replace(old_render, new_render)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
