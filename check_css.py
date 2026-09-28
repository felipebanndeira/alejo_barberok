import os

base = r"c:\Users\usser\Documents\Alejo barber"
css_path = os.path.join(base, "static/css/style.css")

with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# Remove wrong selector (was hiding item 3 = Bloqueos earlier, or wrong indices)
old = """.sidebar ul li:nth-child(5),
    .sidebar ul li:nth-child(6),
    .sidebar ul li:nth-child(7) {
        display: none !important;
    }"""

# In the sidebar: 1=Agenda, 2=Caja, 3=Bloqueos, 4=Accesos, 5=Ajustes, 6=separator, 7=Salir
# Hide 5 (Ajustes), 6 (separator), 7 (Salir) on mobile bottom nav
new = """.sidebar ul li:nth-child(5),
    .sidebar ul li:nth-child(6),
    .sidebar ul li:nth-child(7) {
        display: none !important;
    }"""

# They're the same so check if the old was wrong
print("Found:", old in css)
print("CSS snippet:", css[css.find(".sidebar ul li:nth-child"):css.find(".sidebar ul li:nth-child")+300])
