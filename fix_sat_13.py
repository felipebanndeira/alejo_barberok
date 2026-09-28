import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "core/availability.py")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("sat_end = settings.get('hours_sat_end', '13:00')", "sat_end = settings.get('hours_sat_end', '13:30')")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
