import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "routes/admin_routes.py")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add the reset route
reset_route = """
@admin_bp.route('/reset_caja', methods=['POST'])
@login_required
def reset_caja():
    db = get_db()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('last_reset_date', ?)", (now,))
    db.commit()
    return redirect(request.referrer or url_for('admin.finances'))

@admin_bp.route('/dashboard')
"""
content = content.replace("@admin_bp.route('/dashboard')", reset_route)

# 2. Update dashboard logic
dash_search = """    # Calculate Caja from appointments
    caja_app = db.execute(\"\"\"
        SELECT SUM(s.price) 
        FROM appointments a
        JOIN services s ON a.service_id = s.id
        WHERE a.date = ? AND a.status = 'confirmed'
    \"\"\", (today,)).fetchone()[0]
    caja_app = caja_app if caja_app else 0

    # Get today's sales (Venta Mostrador)
    sales_today = db.execute("SELECT * FROM sales WHERE date(created_at, 'localtime') = ?", (today,)).fetchall()
    caja_sales = sum(s['price'] for s in sales_today)
    
    caja_total = caja_app + caja_sales
    caja_hoy = f"{caja_total:g}".replace('.', ',') if caja_total < 1000 else f"{caja_total:,.0f}".replace(',', '.')

    # Get today's expenses
    expenses_today = db.execute("SELECT * FROM expenses WHERE date(created_at, 'localtime') = ?", (today,)).fetchall()
    gastos_total = sum(e['amount'] for e in expenses_today)"""

dash_replace = """    last_reset_str = db.execute("SELECT value FROM settings WHERE key='last_reset_date'").fetchone()
    last_reset = last_reset_str[0] if last_reset_str else '2000-01-01 00:00:00'
    first_of_month = datetime.now().strftime('%Y-%m-01 00:00:00')
    start_datetime = max(last_reset, first_of_month)

    # Calculate Caja from appointments
    caja_app = db.execute(\"\"\"
        SELECT SUM(s.price) 
        FROM appointments a
        JOIN services s ON a.service_id = s.id
        WHERE (a.date || ' ' || a.time || ':00') >= ? AND a.status = 'confirmed'
    \"\"\", (start_datetime,)).fetchone()[0] or 0

    # Get sales (Venta Mostrador)
    sales_today = db.execute("SELECT * FROM sales WHERE created_at >= ?", (start_datetime,)).fetchall()
    caja_sales = sum(s['price'] for s in sales_today)
    
    caja_total = caja_app + caja_sales
    caja_hoy = f"{caja_total:g}".replace('.', ',') if caja_total < 1000 else f"{caja_total:,.0f}".replace(',', '.')

    # Get expenses
    expenses_today = db.execute("SELECT * FROM expenses WHERE created_at >= ?", (start_datetime,)).fetchall()
    gastos_total = sum(e['amount'] for e in expenses_today)"""

content = content.replace(dash_search, dash_replace)

# 3. Update finances logic
finances_search = """    caja_hoy_app = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE a.date = ? AND a.status = 'confirmed'", (today,)).fetchone()[0]
    caja_hoy_app = caja_hoy_app if caja_hoy_app else 0
    
    # Breakdown Efectivo / Transferencia (Solo turnos)
    caja_efectivo = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE a.date = ? AND a.status = 'confirmed' AND a.payment_method = 'efectivo'", (today,)).fetchone()[0] or 0
    caja_transferencia = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE a.date = ? AND a.status = 'confirmed' AND a.payment_method = 'transferencia'", (today,)).fetchone()[0] or 0
    
    # Also add Venta Mostrador to Efectivo by default
    caja_hoy_sales = db.execute("SELECT SUM(price) FROM sales WHERE date(created_at, 'localtime') = ?", (today,)).fetchone()[0]
    caja_hoy_sales = caja_hoy_sales if caja_hoy_sales else 0
    caja_hoy = caja_hoy_app + caja_hoy_sales
    
    sales_today = db.execute("SELECT * FROM sales WHERE date(created_at, 'localtime') = ? ORDER BY created_at DESC", (today,)).fetchall()
    
    gastos_hoy = db.execute("SELECT SUM(amount) FROM expenses WHERE date(created_at, 'localtime') = ?", (today,)).fetchone()[0]"""

finances_replace = """    last_reset_str = db.execute("SELECT value FROM settings WHERE key='last_reset_date'").fetchone()
    last_reset = last_reset_str[0] if last_reset_str else '2000-01-01 00:00:00'
    first_of_month = datetime.now().strftime('%Y-%m-01 00:00:00')
    start_datetime = max(last_reset, first_of_month)

    caja_hoy_app = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE (a.date || ' ' || a.time || ':00') >= ? AND a.status = 'confirmed'", (start_datetime,)).fetchone()[0] or 0
    
    caja_efectivo = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE (a.date || ' ' || a.time || ':00') >= ? AND a.status = 'confirmed' AND a.payment_method = 'efectivo'", (start_datetime,)).fetchone()[0] or 0
    caja_transferencia = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE (a.date || ' ' || a.time || ':00') >= ? AND a.status = 'confirmed' AND a.payment_method = 'transferencia'", (start_datetime,)).fetchone()[0] or 0
    
    caja_hoy_sales = db.execute("SELECT SUM(price) FROM sales WHERE created_at >= ?", (start_datetime,)).fetchone()[0] or 0
    caja_hoy = caja_hoy_app + caja_hoy_sales
    
    sales_today = db.execute("SELECT * FROM sales WHERE created_at >= ? ORDER BY created_at DESC", (start_datetime,)).fetchall()
    
    gastos_hoy = db.execute("SELECT SUM(amount) FROM expenses WHERE created_at >= ?", (start_datetime,)).fetchone()[0]"""

content = content.replace(finances_search, finances_replace)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
