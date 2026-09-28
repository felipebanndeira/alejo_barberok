import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "routes/admin_routes.py")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_query = """    schedule = db.execute(\"\"\"
        SELECT a.id, a.client_name, a.client_phone, a.time, a.status, s.name as service_name 
        FROM appointments a
        JOIN services s ON a.service_id = s.id
        WHERE a.date = ?
        ORDER BY a.time
    \"\"\", (today,)).fetchall()"""

new_query = """    schedule = db.execute(\"\"\"
        SELECT a.id, a.client_name, a.client_phone, a.date, a.time, a.status, s.name as service_name 
        FROM appointments a
        JOIN services s ON a.service_id = s.id
        WHERE a.date >= ?
        ORDER BY a.date, a.time
    \"\"\", (today,)).fetchall()"""

content = content.replace(old_query, new_query)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
