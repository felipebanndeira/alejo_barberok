import sqlite3
import os

base = r"c:\Users\usser\Documents\Alejo barber"
db_path = os.path.join(base, "barber.db")

conn = sqlite3.connect(db_path)
conn.execute("UPDATE settings SET value='13:30' WHERE key='hours_mon_fri_end_1'")
conn.execute("UPDATE settings SET value='21:30' WHERE key='hours_mon_fri_end_2'")

# If the sat_end key doesn't exist, we insert it
sat_end = conn.execute("SELECT * FROM settings WHERE key='hours_sat_end'").fetchone()
if not sat_end:
    conn.execute("INSERT INTO settings (key, value) VALUES ('hours_sat_end', '13:30')")
else:
    conn.execute("UPDATE settings SET value='13:30' WHERE key='hours_sat_end'")

conn.commit()
conn.close()
