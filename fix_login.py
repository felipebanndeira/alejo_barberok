import os

base = r"c:\Users\usser\Documents\Alejo barber"
routes_path = os.path.join(base, "routes/admin_routes.py")

with open(routes_path, "r", encoding="utf-8") as f:
    routes = f.read()

# Replace the redirect in login
routes = routes.replace(
    "return redirect(request.referrer or url_for('admin.dashboard'))",
    "return redirect(url_for('admin.dashboard'))",
    1 # Only replace the first occurrence which is in login()
)

with open(routes_path, "w", encoding="utf-8") as f:
    f.write(routes)

