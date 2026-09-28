import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "routes/admin_routes.py")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Update chart queries in dashboard to include >= start_datetime
dash_chart_replace = """        inc_app = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE a.date = ? AND (a.date || ' ' || a.time || ':00') >= ? AND a.status = 'confirmed'", (d_str, start_datetime)).fetchone()[0] or 0
        inc_sales = db.execute("SELECT SUM(price) FROM sales WHERE date(created_at, 'localtime') = ? AND datetime(created_at, 'localtime') >= ?", (d_str, start_datetime)).fetchone()[0] or 0"""
content = re.sub(r'        inc_app = db\.execute\("SELECT SUM\(s\.price\).*?a\.status = \'confirmed\'", \(d_str,\)\)\.fetchone\(\)\[0\] or 0\s*inc_sales = db\.execute\("SELECT SUM\(price\).*?=\ \?", \(d_str,\)\)\.fetchone\(\)\[0\] or 0', dash_chart_replace, content, count=1)

# Update chart queries in finances to include >= start_datetime
content = re.sub(r'        inc_app = db\.execute\("SELECT SUM\(s\.price\).*?a\.status = \'confirmed\'", \(d_str,\)\)\.fetchone\(\)\[0\] or 0\s*inc_sales = db\.execute\("SELECT SUM\(price\).*?=\ \?", \(d_str,\)\)\.fetchone\(\)\[0\] or 0', dash_chart_replace, content, count=1)


# Update Monthly queries to include >= start_datetime
monthly_replace = """    caja_mes_app = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE a.date LIKE ? AND (a.date || ' ' || a.time || ':00') >= ? AND a.status = 'confirmed'", (current_month + '%', start_datetime)).fetchone()[0] or 0
    caja_mes_sales = db.execute("SELECT SUM(price) FROM sales WHERE strftime('%Y-%m', created_at, 'localtime') = ? AND datetime(created_at, 'localtime') >= ?", (current_month, start_datetime)).fetchone()[0] or 0
    caja_mes = caja_mes_app + caja_mes_sales
    gastos_mes = db.execute("SELECT SUM(amount) FROM expenses WHERE strftime('%Y-%m', created_at, 'localtime') = ? AND datetime(created_at, 'localtime') >= ?", (current_month, start_datetime)).fetchone()[0] or 0"""
content = re.sub(r'    caja_mes_app = db\.execute\("SELECT SUM\(s\.price\).*?\n.*?gastos_mes = db\.execute\("SELECT SUM\(amount\).*?or 0', monthly_replace, content, flags=re.DOTALL)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
