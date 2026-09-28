import sqlite3
import os

base = r"c:\Users\usser\Documents\Alejo barber"
db_path = os.path.join(base, "barber.db")

conn = sqlite3.connect(db_path)
try:
    conn.execute("ALTER TABLE appointments ADD COLUMN payment_method TEXT DEFAULT 'efectivo'")
    conn.commit()
    print("Column added")
except sqlite3.OperationalError as e:
    print(f"Error (maybe already exists): {e}")
conn.close()
