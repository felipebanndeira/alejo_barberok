import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "core/availability.py")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("end1 = settings.get('hours_mon_fri_end_1', '13:00')", "end1 = settings.get('hours_mon_fri_end_1', '13:30')")
content = content.replace("end2 = settings.get('hours_mon_fri_end_2', '21:00')", "end2 = settings.get('hours_mon_fri_end_2', '21:30')")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
