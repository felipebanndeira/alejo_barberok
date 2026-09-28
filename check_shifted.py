import sqlite3
import os

base = r"c:\Users\usser\Documents\Alejo barber"
db_path = os.path.join(base, "barber.db")
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
print("Test:", conn.execute("SELECT confirmed_at, datetime(confirmed_at, 'localtime') as shifted FROM appointments WHERE status='confirmed'").fetchall()[0][0])
conn.close()
