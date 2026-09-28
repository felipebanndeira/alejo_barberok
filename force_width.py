import os

base = r"c:\Users\usser\Documents\Alejo barber"
dash_path = os.path.join(base, "templates/admin/dashboard.html")

with open(dash_path, "r", encoding="utf-8") as f:
    dash = f.read()

# Make sure the container and cards have explicit 100% width and stretch
dash = dash.replace('<div style="display: flex; flex-direction: column; gap: 1rem;">', '<div style="display: flex; flex-direction: column; gap: 1rem; width: 100%; align-items: stretch;">')

# Make sure the cards have width: 100% !important
dash = dash.replace('class="glass-panel" style="width: 100%;', 'class="glass-panel" style="width: 100% !important; max-width: 100% !important;')

with open(dash_path, "w", encoding="utf-8") as f:
    f.write(dash)

