import sqlite3
import os

base = r"c:\Users\usser\Documents\Alejo barber"
db_path = os.path.join(base, "barber.db")
conn = sqlite3.connect(db_path)
conn.execute("UPDATE appointments SET confirmed_at = datetime(confirmed_at, 'utc') WHERE status='confirmed'")
conn.commit()
conn.close()
