import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "templates/cliente/index.html")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('minDate: "today",', 'minDate: "today",\n        dateFormat: "Y-m-d",\n        altInput: true,\n        altFormat: "d/m/Y",')

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
