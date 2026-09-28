import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"

def fix_text(content):
    content = re.sub(r'ConsultA.*?\s+tus turnos', 'Consultá tus turnos', content)
    content = re.sub(r'IngresA.*?\s+tu n.*?mero', 'Ingresá tu número', content)
    content = re.sub(r'A.*?QuA.*? servicio necesitA.*?s\?', '¿Qué servicio necesitás?', content)
    content = re.sub(r'A.*?CuA.*?ndo querA.*?s venir\?', '¿Cuándo querés venir?', content)
    content = re.sub(r'AtrA.*?s', 'Atrás', content)
    content = re.sub(r'A.*?Turno Confirmado!', '¡Turno Confirmado!', content)
    content = re.sub(r'TelA.*?fono', 'Teléfono', content)
    content = re.sub(r'APreferA.*?s agendar por mensaje o tenA.*?s dudas\?', '¿Preferís agendar por mensaje o tenés dudas?', content)
    content = re.sub(r'n.*?mero de celular.', 'número de celular.', content)
    return content

for template in ["index.html", "mis_turnos.html"]:
    path = os.path.join(base, "templates/cliente", template)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    content = fix_text(content)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# And main.js
js_path = os.path.join(base, "static/js/main.js")
with open(js_path, "r", encoding="utf-8") as f:
    js = f.read()
    
js = fix_text(js)
js = re.sub(r'conexiA.*?n', 'conexión', js)

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js)

