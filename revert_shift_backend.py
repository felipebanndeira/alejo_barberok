import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "routes/admin_routes.py")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace toggle_shift backend with reset_caja
toggle_route = """@admin_bp.route('/toggle_shift', methods=['POST'])
@login_required
def toggle_shift():
    db = get_db()
    shift_active = db.execute("SELECT value FROM settings WHERE key='shift_active'").fetchone()
    is_active = shift_active[0] == 'true' if shift_active else False
    
    if is_active:
        db.execute("UPDATE settings SET value='false' WHERE key='shift_active'")
    else:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.execute("UPDATE settings SET value='true' WHERE key='shift_active'")
        db.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('shift_start', ?)", (now,))
        
    db.commit()
    return redirect(request.referrer or url_for('admin.finances'))"""

reset_route = """@admin_bp.route('/reset_caja', methods=['POST'])
@login_required
def reset_caja():
    db = get_db()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('last_reset_date', ?)", (now,))
    db.commit()
    return redirect(request.referrer or url_for('admin.finances'))"""

content = content.replace(toggle_route, reset_route)

# Now revert the dashboard logic to just use start_datetime
dash_search = """    shift_active_row = db.execute("SELECT value FROM settings WHERE key='shift_active'").fetchone()
    shift_active = shift_active_row[0] == 'true' if shift_active_row else False
    shift_start_row = db.execute("SELECT value FROM settings WHERE key='shift_start'").fetchone()
    shift_start = shift_start_row[0] if shift_start_row else '2000-01-01 00:00:00'
    
    # Metrics
    appointments_today = db.execute("SELECT COUNT(*) FROM appointments WHERE date = ? AND status != 'cancelled'", (today,)).fetchone()[0]
    total_clients = db.execute("SELECT COUNT(DISTINCT client_phone) FROM appointments").fetchone()[0]
    
    caja_total = 0
    gastos_total = 0
    sales_today = []
    expenses_today = []
    
    if shift_active:
        caja_app = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE (a.date || ' ' || a.time || ':00') >= ? AND a.status = 'confirmed'", (shift_start,)).fetchone()[0] or 0
        sales_today = db.execute("SELECT * FROM sales WHERE created_at >= ?", (shift_start,)).fetchall()
        caja_sales = sum(s['price'] for s in sales_today)
        caja_total = caja_app + caja_sales
        expenses_today = db.execute("SELECT * FROM expenses WHERE created_at >= ?", (shift_start,)).fetchall()
        gastos_total = sum(e['amount'] for e in expenses_today)"""

dash_replace = """    last_reset_str = db.execute("SELECT value FROM settings WHERE key='last_reset_date'").fetchone()
    last_reset = last_reset_str[0] if last_reset_str else '2000-01-01 00:00:00'
    first_of_month = datetime.now().strftime('%Y-%m-01 00:00:00')
    start_datetime = max(last_reset, first_of_month)
    
    # Metrics
    appointments_today = db.execute("SELECT COUNT(*) FROM appointments WHERE date = ? AND status != 'cancelled'", (today,)).fetchone()[0]
    total_clients = db.execute("SELECT COUNT(DISTINCT client_phone) FROM appointments").fetchone()[0]
    
    caja_app = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE (a.date || ' ' || a.time || ':00') >= ? AND a.status = 'confirmed'", (start_datetime,)).fetchone()[0] or 0
    sales_today = db.execute("SELECT * FROM sales WHERE created_at >= ?", (start_datetime,)).fetchall()
    caja_sales = sum(s['price'] for s in sales_today)
    caja_total = caja_app + caja_sales
    expenses_today = db.execute("SELECT * FROM expenses WHERE created_at >= ?", (start_datetime,)).fetchall()
    gastos_total = sum(e['amount'] for e in expenses_today)"""

content = content.replace(dash_search, dash_replace)

# Revert finances logic
fin_search = """    shift_active_row = db.execute("SELECT value FROM settings WHERE key='shift_active'").fetchone()
    shift_active = shift_active_row[0] == 'true' if shift_active_row else False
    shift_start_row = db.execute("SELECT value FROM settings WHERE key='shift_start'").fetchone()
    shift_start = shift_start_row[0] if shift_start_row else '2000-01-01 00:00:00'

    caja_hoy_val = 0
    caja_efectivo = 0
    caja_transferencia = 0
    gastos_hoy_val = 0
    sales_today = []
    
    if shift_active:
        caja_hoy_app = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE (a.date || ' ' || a.time || ':00') >= ? AND a.status = 'confirmed'", (shift_start,)).fetchone()[0] or 0
        caja_efectivo = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE (a.date || ' ' || a.time || ':00') >= ? AND a.status = 'confirmed' AND a.payment_method = 'efectivo'", (shift_start,)).fetchone()[0] or 0
        caja_transferencia = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE (a.date || ' ' || a.time || ':00') >= ? AND a.status = 'confirmed' AND a.payment_method = 'transferencia'", (shift_start,)).fetchone()[0] or 0
        caja_hoy_sales = db.execute("SELECT SUM(price) FROM sales WHERE created_at >= ?", (shift_start,)).fetchone()[0] or 0
        caja_efectivo += caja_hoy_sales
        caja_hoy_val = caja_hoy_app + caja_hoy_sales
        sales_today = db.execute("SELECT * FROM sales WHERE created_at >= ? ORDER BY created_at DESC", (shift_start,)).fetchall()
        gastos_hoy_val = db.execute("SELECT SUM(amount) FROM expenses WHERE created_at >= ?", (shift_start,)).fetchone()[0] or 0"""

fin_replace = """    last_reset_str = db.execute("SELECT value FROM settings WHERE key='last_reset_date'").fetchone()
    last_reset = last_reset_str[0] if last_reset_str else '2000-01-01 00:00:00'
    first_of_month = datetime.now().strftime('%Y-%m-01 00:00:00')
    start_datetime = max(last_reset, first_of_month)

    caja_hoy_app = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE (a.date || ' ' || a.time || ':00') >= ? AND a.status = 'confirmed'", (start_datetime,)).fetchone()[0] or 0
    caja_efectivo = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE (a.date || ' ' || a.time || ':00') >= ? AND a.status = 'confirmed' AND a.payment_method = 'efectivo'", (start_datetime,)).fetchone()[0] or 0
    caja_transferencia = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE (a.date || ' ' || a.time || ':00') >= ? AND a.status = 'confirmed' AND a.payment_method = 'transferencia'", (start_datetime,)).fetchone()[0] or 0
    caja_hoy_sales = db.execute("SELECT SUM(price) FROM sales WHERE created_at >= ?", (start_datetime,)).fetchone()[0] or 0
    caja_efectivo += caja_hoy_sales
    caja_hoy_val = caja_hoy_app + caja_hoy_sales
    sales_today = db.execute("SELECT * FROM sales WHERE created_at >= ? ORDER BY created_at DESC", (start_datetime,)).fetchall()
    gastos_hoy_val = db.execute("SELECT SUM(amount) FROM expenses WHERE created_at >= ?", (start_datetime,)).fetchone()[0] or 0"""

content = content.replace(fin_search, fin_replace)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
