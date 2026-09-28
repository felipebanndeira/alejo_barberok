import os

base = r"c:\Users\usser\Documents\Alejo barber"
finances_path = os.path.join(base, "templates/admin/finances.html")
dash_path = os.path.join(base, "templates/admin/dashboard.html")

# 1. Fix chart tension in finances.html
with open(finances_path, "r", encoding="utf-8") as f:
    fin = f.read()

fin = fin.replace("tension: 0.4", "tension: 0")

with open(finances_path, "w", encoding="utf-8") as f:
    f.write(fin)

# 2. Fix card width in dashboard.html
with open(dash_path, "r", encoding="utf-8") as f:
    dash = f.read()

# Make the cards width: 100% and padding 1.25rem to match stats cards
dash = dash.replace('class="glass-panel" style="padding: 1rem;', 'class="glass-panel" style="width: 100%; padding: 1.25rem;')

with open(dash_path, "w", encoding="utf-8") as f:
    f.write(dash)

