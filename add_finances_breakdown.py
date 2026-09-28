import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "routes/admin_routes.py")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# In finances()
search = """    caja_hoy_sales = db.execute("SELECT SUM(price) FROM sales WHERE date(created_at, 'localtime') = ?", (today,)).fetchone()[0]"""

replace = """    # Breakdown Efectivo / Transferencia (Solo turnos)
    caja_efectivo = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE a.date = ? AND a.status = 'confirmed' AND a.payment_method = 'efectivo'", (today,)).fetchone()[0] or 0
    caja_transferencia = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE a.date = ? AND a.status = 'confirmed' AND a.payment_method = 'transferencia'", (today,)).fetchone()[0] or 0
    
    # Also add Venta Mostrador to Efectivo by default
    caja_hoy_sales = db.execute("SELECT SUM(price) FROM sales WHERE date(created_at, 'localtime') = ?", (today,)).fetchone()[0]
"""

content = content.replace(search, replace)

# In render_template
old_render = "caja_mes=caja_mes_str, gastos_mes=gastos_mes_str, net_mes=net_profit_mes_str,"
new_render = "caja_mes=caja_mes_str, gastos_mes=gastos_mes_str, net_mes=net_profit_mes_str, caja_efectivo=caja_efectivo, caja_transferencia=caja_transferencia,"
content = content.replace(old_render, new_render)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
