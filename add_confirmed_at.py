import sqlite3
import os

base = r"c:\Users\usser\Documents\Alejo barber"
db_path = os.path.join(base, "barber.db")

conn = sqlite3.connect(db_path)
try:
    conn.execute("ALTER TABLE appointments ADD COLUMN confirmed_at TIMESTAMP")
    # For existing confirmed appointments, set confirmed_at to something old or their date+time
    conn.execute("UPDATE appointments SET confirmed_at = date || ' ' || time || ':00' WHERE status = 'confirmed'")
    conn.commit()
    print("Column added")
except sqlite3.OperationalError as e:
    print(f"Error: {e}")
conn.close()
