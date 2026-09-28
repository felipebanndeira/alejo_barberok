import sqlite3
import os

base = r"c:\Users\usser\Documents\Alejo barber"
db_path = os.path.join(base, "barber.db")
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row

for r in conn.execute("SELECT (a.date || ' ' || a.time || ':00') as ts, a.time FROM appointments a WHERE a.status = 'confirmed'").fetchall():
    print(dict(r))
conn.close()
