import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "core/db.py")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("    db.execute('''\n        \n    db.execute('''\n        CREATE TABLE IF NOT EXISTS sales", "    db.execute('''\n        CREATE TABLE IF NOT EXISTS sales")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
