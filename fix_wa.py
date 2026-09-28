import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "templates/cliente/mis_turnos.html")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

import re
content = re.sub(
    r'<a href="https://wa\.me/\{\{ settings\.get\(\'barber_phone\'.*?\}\}.*?</a>',
    '<a href="https://wa.me/5493755283261?text=Hola Alejo, te quería avisar que no voy a poder ir a mi turno de las {{t.time}}." target="_blank" style="font-size:0.75rem; color:#a1a1aa; text-decoration:underline;">Avisar tardanza/ausencia</a>',
    content
)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
