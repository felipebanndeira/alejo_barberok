import os
import urllib.parse

base = r"c:\Users\usser\Documents\Alejo barber"

text = "Hola Felipe vengo de la pagina de alejo barber me gustaria un trabajo tuyo"
# Use urllib to encode properly, but simple replace works too. Actually, jinja or html requires url encoding for spaces in href.
url_text = urllib.parse.quote(text)
wa_link = f"https://wa.me/3755802727?text={url_text}"

old_a_tag = '<a href="#" style="color: #666; text-decoration: none; border-bottom: 1px solid #444; padding-bottom: 1px;">[Tu Nombre / Agencia]</a>'
new_a_tag = f'<a href="{wa_link}" target="_blank" style="color: #666; text-decoration: none; border-bottom: 1px solid #444; padding-bottom: 1px; transition: color 0.3s;" onmouseover="this.style.color=\'#FFCC00\'" onmouseout="this.style.color=\'#666\'">Felipe Bandeira</a>'

for template in ["index.html", "mis_turnos.html"]:
    path = os.path.join(base, "templates/cliente", template)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    content = content.replace(old_a_tag, new_a_tag)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

