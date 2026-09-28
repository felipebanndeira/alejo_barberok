import os

base = r"c:\Users\usser\Documents\Alejo barber"
index_path = os.path.join(base, "templates/cliente/index.html")

with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("¿Cuándo querés venir?", "Reserva tu horario")
content = content.replace("¿Qué servicio necesitás?", "Servicios disponibles")
content = content.replace(">Tus datos<", ">Información del cliente<")

with open(index_path, "w", encoding="utf-8") as f:
    f.write(content)

js_path = os.path.join(base, "static/js/main.js")
with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

js_content = js_content.replace('"Tus Datos"', '"Información del Cliente"')

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content)
