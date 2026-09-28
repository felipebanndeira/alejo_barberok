import sqlite3
import os
from datetime import datetime

base = r"c:\Users\usser\Documents\Alejo barber"
db_path = os.path.join(base, "barber.db")
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row

last_reset = '2026-09-25 18:25:47'
today = datetime.now().strftime('%Y-%m-%d')
print("Caja app:", conn.execute("SELECT SUM(s.price) FROM appointments a JOIN services s ON a.service_id = s.id WHERE (a.date || ' ' || a.time || ':00') >= ? AND (a.date || ' ' || a.time || ':00') <= ? AND a.status = 'confirmed'", (last_reset, today + ' 23:59:59')).fetchone()[0])
conn.close()
