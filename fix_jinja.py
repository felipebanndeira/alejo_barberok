import os

base = r"c:\Users\usser\Documents\Alejo barber"
dash_path = os.path.join(base, "templates/admin/dashboard.html")

with open(dash_path, "r", encoding="utf-8") as f:
    dash = f.read()

dash = dash.replace(r"replace(\'+\', \'\')", "replace('+', '')")

with open(dash_path, "w", encoding="utf-8") as f:
    f.write(dash)
