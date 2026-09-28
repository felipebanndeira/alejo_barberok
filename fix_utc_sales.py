import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "routes/admin_routes.py")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Fix dashboard sales & expenses
content = content.replace('sales_today = db.execute("SELECT * FROM sales WHERE created_at >= ?", (start_datetime,)).fetchall()', 
                          'sales_today = db.execute("SELECT * FROM sales WHERE datetime(created_at, \'localtime\') >= ?", (start_datetime,)).fetchall()')
content = content.replace('expenses_today = db.execute("SELECT * FROM expenses WHERE created_at >= ?", (start_datetime,)).fetchall()', 
                          'expenses_today = db.execute("SELECT * FROM expenses WHERE datetime(created_at, \'localtime\') >= ?", (start_datetime,)).fetchall()')

# Fix finances sales & expenses
content = content.replace('caja_hoy_sales = db.execute("SELECT SUM(price) FROM sales WHERE created_at >= ?", (start_datetime,)).fetchone()[0] or 0', 
                          'caja_hoy_sales = db.execute("SELECT SUM(price) FROM sales WHERE datetime(created_at, \'localtime\') >= ?", (start_datetime,)).fetchone()[0] or 0')
content = content.replace('sales_today = db.execute("SELECT * FROM sales WHERE created_at >= ? ORDER BY created_at DESC", (start_datetime,)).fetchall()', 
                          'sales_today = db.execute("SELECT * FROM sales WHERE datetime(created_at, \'localtime\') >= ? ORDER BY created_at DESC", (start_datetime,)).fetchall()')
content = content.replace('gastos_hoy_val = db.execute("SELECT SUM(amount) FROM expenses WHERE created_at >= ?", (start_datetime,)).fetchone()[0] or 0', 
                          'gastos_hoy_val = db.execute("SELECT SUM(amount) FROM expenses WHERE datetime(created_at, \'localtime\') >= ?", (start_datetime,)).fetchone()[0] or 0')

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
