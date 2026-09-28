import os
import re
from datetime import datetime

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "routes/admin_routes.py")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Add <= today + ' 23:59:59' to all appointment queries in dashboard and finances

dash_replace = """    caja_app = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE (a.date || ' ' || a.time || ':00') >= ? AND (a.date || ' ' || a.time || ':00') <= ? AND a.status = 'confirmed'", (start_datetime, today + ' 23:59:59')).fetchone()[0] or 0"""
content = re.sub(r'caja_app = db.execute\("SELECT SUM\(s.price\).*?start_datetime,\)\)\.fetchone\(\)\[0\] or 0', dash_replace, content)

fin_replace_1 = """caja_hoy_app = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE (a.date || ' ' || a.time || ':00') >= ? AND (a.date || ' ' || a.time || ':00') <= ? AND a.status = 'confirmed'", (start_datetime, today + ' 23:59:59')).fetchone()[0] or 0"""
content = re.sub(r'caja_hoy_app = db.execute\("SELECT SUM\(s.price\).*?start_datetime,\)\)\.fetchone\(\)\[0\] or 0', fin_replace_1, content)

fin_replace_2 = """caja_efectivo = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE (a.date || ' ' || a.time || ':00') >= ? AND (a.date || ' ' || a.time || ':00') <= ? AND a.status = 'confirmed' AND a.payment_method = 'efectivo'", (start_datetime, today + ' 23:59:59')).fetchone()[0] or 0"""
content = re.sub(r'caja_efectivo = db.execute\("SELECT SUM\(s.price\).*?start_datetime,\)\)\.fetchone\(\)\[0\] or 0', fin_replace_2, content)

fin_replace_3 = """caja_transferencia = db.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE (a.date || ' ' || a.time || ':00') >= ? AND (a.date || ' ' || a.time || ':00') <= ? AND a.status = 'confirmed' AND a.payment_method = 'transferencia'", (start_datetime, today + ' 23:59:59')).fetchone()[0] or 0"""
content = re.sub(r'caja_transferencia = db.execute\("SELECT SUM\(s.price\).*?start_datetime,\)\)\.fetchone\(\)\[0\] or 0', fin_replace_3, content)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
