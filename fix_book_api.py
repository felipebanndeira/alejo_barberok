import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "routes/cliente_routes.py")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("    if data['time'] not in times:", "    available_times = [t['time'] for t in times if t['available']]\n    if data['time'] not in available_times:")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
