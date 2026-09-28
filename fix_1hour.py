import os

base = r"c:\Users\usser\Documents\Alejo barber"
path_routes = os.path.join(base, "routes/cliente_routes.py")

with open(path_routes, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("timedelta(hours=2)", "timedelta(hours=1)")

with open(path_routes, "w", encoding="utf-8") as f:
    f.write(content)

path_template = os.path.join(base, "templates/cliente/mis_turnos.html")
with open(path_template, "r", encoding="utf-8") as f:
    content2 = f.read()

content2 = content2.replace("con más de 2 hs de anticipación", "con más de 1 hs de anticipación")

with open(path_template, "w", encoding="utf-8") as f:
    f.write(content2)

