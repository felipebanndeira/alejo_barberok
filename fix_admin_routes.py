import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "routes/admin_routes.py")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("shift_active=shift_active, shift_active=shift_active", "shift_active=shift_active")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
