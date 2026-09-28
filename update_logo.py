import sqlite3
db = sqlite3.connect('barber.db')
db.execute("REPLACE INTO settings (key, value) VALUES ('logo_path', 'logo.png')")
db.commit()
db.close()
