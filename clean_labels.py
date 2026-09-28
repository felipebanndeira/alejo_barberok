import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "templates/admin/finances.html")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("Caja Mensual (Automática)", "Caja Mensual")
content = content.replace("Caja de Hoy (Manual)", "Caja de Hoy")
content = content.replace("Ganancia Neta (Manual)", "Ganancia Neta")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

path2 = os.path.join(base, "templates/admin/dashboard.html")
with open(path2, "r", encoding="utf-8") as f:
    content2 = f.read()
content2 = content2.replace("Caja de Hoy (Manual)", "Caja de Hoy")
with open(path2, "w", encoding="utf-8") as f:
    f.write(content2)
