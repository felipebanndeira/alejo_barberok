import os

base = r"c:\Users\usser\Documents\Alejo barber"
file_path = os.path.join(base, "templates/cliente/mis_turnos.html")

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace {{ t.date }} with split format for dd/mm/yyyy
content = content.replace("{{ t.date }}", "{{ t.date.split('-')[2] }}/{{ t.date.split('-')[1] }}/{{ t.date.split('-')[0] }}")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

