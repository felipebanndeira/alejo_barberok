import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "templates/cliente/index.html")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('<p class="text-dim" style="font-size: 0.85rem;">30 minutos</p>', '')

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
