import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "core/db.py")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

new_tables = """
    db.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            price INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    db.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            concept TEXT NOT NULL,
            amount INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
"""

if "CREATE TABLE IF NOT EXISTS sales" not in content:
    content = content.replace("CREATE TABLE IF NOT EXISTS users", new_tables + "\n    db.execute('''\n        CREATE TABLE IF NOT EXISTS users")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
