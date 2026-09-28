import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "templates/admin/dashboard.html")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("ASeguro que querAcs", "¿Seguro que quieres")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
