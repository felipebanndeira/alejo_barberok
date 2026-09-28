import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "routes/admin_routes.py")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace reset_caja with toggle_shift
reset_route = """@admin_bp.route('/reset_caja', methods=['POST'])
@login_required
def reset_caja():
    db = get_db()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('last_reset_date', ?)", (now,))
    db.commit()
    return redirect(request.referrer or url_for('admin.finances'))"""

toggle_route = """@admin_bp.route('/toggle_shift', methods=['POST'])
@login_required
def toggle_shift():
    db = get_db()
    shift_active = db.execute("SELECT value FROM settings WHERE key='shift_active'").fetchone()
    is_active = shift_active[0] == 'true' if shift_active else False
    
    if is_active:
        # Cerrar jornada
        db.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('shift_active', 'false')")
    else:
        # Iniciar jornada
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('shift_active', 'true')")
        db.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('shift_start', ?)", (now,))
        
    db.commit()
    return redirect(request.referrer or url_for('admin.finances'))"""

content = content.replace(reset_route, toggle_route)

# Now we need to update dashboard and finances logic to respect `shift_active`.
# I'll create a function or just replace the blocks.

dash_logic = """    last_reset_str = db.execute("SELECT value FROM settings WHERE key='last_reset_date'").fetchone()
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
    gastos_total = sum(e['amount'] for e in expenses_today)
    gastos_hoy_str = f"{gastos_total:g}".replace('.', ',') if gastos_total < 1000 else f"{gastos_total:,.0f}".replace(',', '.')
    
    # Net Profit
    net_profit = caja_total - gastos_total
    net_profit_str = f"{net_profit:g}".replace('.', ',') if abs(net_profit) < 1000 else f"{net_profit:,.0f}".replace(',', '.')"""

new_dash_logic = """    shift_active_row = db.execute("SELECT value FROM settings WHERE key='shift_active'").fetchone()
    shift_active = shift_active_row[0] == 'true' if shift_active_row else False
    
    shift_start_row = db.execute("SELECT value FROM settings WHERE key='shift_start'").fetchone()
    shift_start = shift_start_row[0] if shift_start_row else '2000-01-01 00:00:00'
    
    caja_total = 0
    gastos_total = 0
    sales_today = []
    expenses_today = []
    
    if shift_active:
        caja_app = db.execute(\"\"\"
            SELECT SUM(s.price) 
            FROM appointments a
            JOIN services s ON a.service_id = s.id
            WHERE (a.date || ' ' || a.time || ':00') >= ? AND a.status = 'confirmed'
        \"\"\", (shift_start,)).fetchone()[0] or 0

        sales_today = db.execute("SELECT * FROM sales WHERE created_at >= ?", (shift_start,)).fetchall()
        caja_sales = sum(s['price'] for s in sales_today)
        
        caja_total = caja_app + caja_sales
        
        expenses_today = db.execute("SELECT * FROM expenses WHERE created_at >= ?", (shift_start,)).fetchall()
        gastos_total = sum(e['amount'] for e in expenses_today)

    caja_hoy = f"{caja_total:g}".replace('.', ',') if caja_total < 1000 else f"{caja_total:,.0f}".replace(',', '.')
    gastos_hoy_str = f"{gastos_total:g}".replace('.', ',') if gastos_total < 1000 else f"{gastos_total:,.0f}".replace(',', '.')
    
    net_profit = caja_total - gastos_total
    net_profit_str = f"{net_profit:g}".replace('.', ',') if abs(net_profit) < 1000 else f"{net_profit:,.0f}".replace(',', '.')"""

content = content.replace(dash_logic, new_dash_logic)

# finances logic
fin_search = """    last_reset_str = db.execute("SELECT value FROM settings WHERE key='last_reset_date'").fetchone()
    last_reset = last_reset_str[0] if last_reset_str else '2000-01-01 00:00:00'
    first_of_month = datetime.now().strftime('%Y-%m-01 00:00:00')
    start_datetime = max(last_reset, first_of_month)

    caja_hoy_app = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE (a.date || ' ' || a.time || ':00') >= ? AND a.status = 'confirmed'", (start_datetime,)).fetchone()[0] or 0
    
    caja_efectivo = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE (a.date || ' ' || a.time || ':00') >= ? AND a.status = 'confirmed' AND a.payment_method = 'efectivo'", (start_datetime,)).fetchone()[0] or 0
    caja_transferencia = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE (a.date || ' ' || a.time || ':00') >= ? AND a.status = 'confirmed' AND a.payment_method = 'transferencia'", (start_datetime,)).fetchone()[0] or 0
    
    caja_hoy_sales = db.execute("SELECT SUM(price) FROM sales WHERE created_at >= ?", (start_datetime,)).fetchone()[0] or 0
    caja_hoy = caja_hoy_app + caja_hoy_sales
    
    sales_today = db.execute("SELECT * FROM sales WHERE created_at >= ? ORDER BY created_at DESC", (start_datetime,)).fetchall()
    
    gastos_hoy = db.execute("SELECT SUM(amount) FROM expenses WHERE created_at >= ?", (start_datetime,)).fetchone()[0] or 0
    gastos_hoy_val = gastos_hoy
    gastos_hoy_str = f"{gastos_hoy_val:,.2f}".replace(",", ".")
    
    net_profit = caja_hoy - gastos_hoy_val
    net_profit_str = f"{net_profit:,.2f}".replace(",", ".")"""

new_fin_search = """    shift_active_row = db.execute("SELECT value FROM settings WHERE key='shift_active'").fetchone()
    shift_active = shift_active_row[0] == 'true' if shift_active_row else False
    
    shift_start_row = db.execute("SELECT value FROM settings WHERE key='shift_start'").fetchone()
    shift_start = shift_start_row[0] if shift_start_row else '2000-01-01 00:00:00'

    caja_hoy = 0
    caja_efectivo = 0
    caja_transferencia = 0
    gastos_hoy_val = 0
    sales_today = []
    
    if shift_active:
        caja_hoy_app = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE (a.date || ' ' || a.time || ':00') >= ? AND a.status = 'confirmed'", (shift_start,)).fetchone()[0] or 0
        caja_efectivo = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE (a.date || ' ' || a.time || ':00') >= ? AND a.status = 'confirmed' AND a.payment_method = 'efectivo'", (shift_start,)).fetchone()[0] or 0
        caja_transferencia = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE (a.date || ' ' || a.time || ':00') >= ? AND a.status = 'confirmed' AND a.payment_method = 'transferencia'", (shift_start,)).fetchone()[0] or 0
        
        caja_hoy_sales = db.execute("SELECT SUM(price) FROM sales WHERE created_at >= ?", (shift_start,)).fetchone()[0] or 0
        # By default sales count as efectivo
        caja_efectivo += caja_hoy_sales
        caja_hoy = caja_hoy_app + caja_hoy_sales
        
        sales_today = db.execute("SELECT * FROM sales WHERE created_at >= ? ORDER BY created_at DESC", (shift_start,)).fetchall()
        gastos_hoy_val = db.execute("SELECT SUM(amount) FROM expenses WHERE created_at >= ?", (shift_start,)).fetchone()[0] or 0

    gastos_hoy_str = f"{gastos_hoy_val:,.2f}".replace(",", ".")
    net_profit = caja_hoy - gastos_hoy_val
    net_profit_str = f"{net_profit:,.2f}".replace(",", ".")"""

content = content.replace(fin_search, new_fin_search)

# Pass shift_active to templates
content = content.replace("settings=settings, sales=sales_today, expenses=expenses_today", "shift_active=shift_active, settings=settings, sales=sales_today, expenses=expenses_today")
content = content.replace("settings=settings, sales=sales_today,\n                           caja_mes", "shift_active=shift_active, settings=settings, sales=sales_today,\n                           caja_mes")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
