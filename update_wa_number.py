import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"
index_path = os.path.join(base, "templates/cliente/index.html")

with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the dynamic jinja tag with the hardcoded number
old_href = 'href="https://wa.me/{{ settings.get(\'whatsapp\', \'\')|replace(\'+\', \'\') }}"'
new_href = 'href="https://wa.me/3755283261"'

content = content.replace(old_href, new_href)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(content)

