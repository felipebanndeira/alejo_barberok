import sqlite3
import os

base = r"c:\Users\usser\Documents\Alejo barber"
db_path = os.path.join(base, "barber.db")

conn = sqlite3.connect(db_path)
try:
    conn.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('shift_active', 'false')")
    conn.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('shift_start', '2000-01-01 00:00:00')")
    conn.commit()
    print("Settings initialized")
except sqlite3.OperationalError as e:
    print(f"Error: {e}")
conn.close()
