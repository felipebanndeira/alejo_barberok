import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"

def fix_text(content):
    content = re.sub(r'Consult.*? tus turnos', 'Consultá tus turnos', content)
    content = re.sub(r'Ingres.*? tu n.*?mero', 'Ingresá tu número', content)
    content = re.sub(r'A.*?Qu.*? servicio necesit.*?s\?', '¿Qué servicio necesitás?', content)
    content = re.sub(r'A.*?Cu.*?ndo quer.*?s venir\?', '¿Cuándo querés venir?', content)
    content = re.sub(r'< Atr.*?s', '< Atrás', content)
    content = re.sub(r'A.*?Turno Confirmado!', '¡Turno Confirmado!', content)
    content = re.sub(r'Tel.*?fono', 'Teléfono', content)
    content = re.sub(r'APrefer.*?s agendar por mensaje o ten.*?s dudas\?', '¿Preferís agendar por mensaje o tenés dudas?', content)
    content = re.sub(r'No hay reservas asociadas a este n.*?mero de celular.', 'No hay reservas asociadas a este número de celular.', content)
    return content

for template in ["index.html", "mis_turnos.html"]:
    path = os.path.join(base, "templates/cliente", template)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    content = fix_text(content)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

