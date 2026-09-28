import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "routes/admin_routes.py")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Replace reset_caja with toggle_shift
content = re.sub(r"@admin_bp\.route\('/reset_caja', methods=\['POST'\]\).*?def reset_caja\(\):.*?return redirect\(request\.referrer or url_for\('admin\.finances'\)\)", """@admin_bp.route('/toggle_shift', methods=['POST'])
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
    return redirect(request.referrer or url_for('admin.finances'))""", content, flags=re.DOTALL)

# 2. Update dashboard logic
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

content = re.sub(r"    last_reset_str = db\.execute.*?net_profit:,\.0f}\"\.replace\(',', '\.'\)", new_dash_logic, content, flags=re.DOTALL, count=1)

# 3. Update finances logic
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
        caja_efectivo += caja_hoy_sales
        caja_hoy = caja_hoy_app + caja_hoy_sales
        
        sales_today = db.execute("SELECT * FROM sales WHERE created_at >= ? ORDER BY created_at DESC", (shift_start,)).fetchall()
        gastos_hoy_val = db.execute("SELECT SUM(amount) FROM expenses WHERE created_at >= ?", (shift_start,)).fetchone()[0] or 0

    gastos_hoy_str = f"{gastos_hoy_val:,.2f}".replace(",", ".")
    net_profit = caja_hoy - gastos_hoy_val
    net_profit_str = f"{net_profit:,.2f}".replace(",", ".")"""

content = re.sub(r"    last_reset_str = db\.execute.*?net_profit:,\.2f}\"\.replace\(\",\", \"\.\"\)", new_fin_search, content, flags=re.DOTALL, count=1)

# Pass shift_active
content = content.replace("schedule=schedule, settings=settings", "schedule=schedule, shift_active=shift_active, settings=settings")
content = content.replace("settings=settings, sales=sales_today,", "shift_active=shift_active, settings=settings, sales=sales_today,")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
