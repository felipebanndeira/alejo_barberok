import sqlite3
import os

base = r"c:\Users\usser\Documents\Alejo barber"
db_path = os.path.join(base, "barber.db")
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row

print("Today confirmed:")
for r in conn.execute("SELECT * FROM appointments WHERE date='2026-09-25' AND status='confirmed'").fetchall():
    print(dict(r))
conn.close()
