import sqlite3
import os

base = r"c:\Users\usser\Documents\Alejo barber"
db_path = os.path.join(base, "barber.db")
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row

print("Settings:", dict(conn.execute("SELECT * FROM settings WHERE key='last_reset_date'").fetchall()))
print("Recent Sales:", [dict(r) for r in conn.execute("SELECT * FROM sales ORDER BY id DESC LIMIT 3").fetchall()])
print("Recent Appointments:", [dict(r) for r in conn.execute("SELECT * FROM appointments ORDER BY id DESC LIMIT 3").fetchall()])
conn.close()
