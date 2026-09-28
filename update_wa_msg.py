import os
import urllib.parse
import re

base = r"c:\Users\usser\Documents\Alejo barber"

old_text = "Hola Felipe vengo de la pagina de alejo barber me gustaria un trabajo tuyo"
new_text = "Hola Felipe, me comunico porque vi tu trabajo en la web de Alejo Barber. Estoy interesado en conocer tus servicios y cotizar un proyecto."

old_url_text = urllib.parse.quote(old_text)
new_url_text = urllib.parse.quote(new_text)

for template in ["index.html", "mis_turnos.html"]:
    path = os.path.join(base, "templates/cliente", template)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    content = content.replace(old_url_text, new_url_text)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

