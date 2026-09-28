import os

base = r"c:\Users\usser\Documents\Alejo barber"
routes_path = os.path.join(base, "routes/admin_routes.py")

with open(routes_path, "r", encoding="utf-8") as f:
    routes = f.read()

routes = routes.replace("from datetime import datetime", "from datetime import datetime, timedelta")

with open(routes_path, "w", encoding="utf-8") as f:
    f.write(routes)
