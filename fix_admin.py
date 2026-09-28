import os

base = r"c:\Users\usser\Documents\Alejo barber"

# 1. Fix admin_routes.py
routes_path = os.path.join(base, "routes/admin_routes.py")
with open(routes_path, "r", encoding="utf-8") as f:
    routes = f.read()

# Add settings fetch to dashboard
if "settings=dict(db.execute('SELECT key, value FROM settings').fetchall())" not in routes.split("def dashboard():")[1]:
    routes = routes.replace(
        "return render_template('admin/dashboard.html', \n                           appointments_today=appointments_today, \n                           total_clients=total_clients, caja_hoy=caja_hoy,\n                           schedule=schedule)",
        "settings=dict(db.execute('SELECT key, value FROM settings').fetchall())\n    return render_template('admin/dashboard.html', \n                           appointments_today=appointments_today, \n                           total_clients=total_clients, caja_hoy=caja_hoy,\n                           schedule=schedule, settings=settings)"
    )

# Add settings fetch to blocks
if "settings=dict(db.execute('SELECT key, value FROM settings').fetchall())" not in routes.split("def blocks():")[1]:
    routes = routes.replace(
        "blocks = db.execute(\"SELECT * FROM blocks\").fetchall()\n    return render_template('admin/blocks.html', blocks=blocks)",
        "blocks = db.execute(\"SELECT * FROM blocks\").fetchall()\n    settings=dict(db.execute('SELECT key, value FROM settings').fetchall())\n    return render_template('admin/blocks.html', blocks=blocks, settings=settings)"
    )

# Add settings fetch to users (in admin_routes.py if it's there)
if "def users():" in routes:
    if "settings=dict(db.execute('SELECT key, value FROM settings').fetchall())" not in routes.split("def users():")[1]:
        routes = routes.replace(
            "users_list = db.execute(\"SELECT id, username FROM users\").fetchall()\n    return render_template('admin/users.html', users=users_list)",
            "users_list = db.execute(\"SELECT id, username FROM users\").fetchall()\n    settings=dict(db.execute('SELECT key, value FROM settings').fetchall())\n    return render_template('admin/users.html', users=users_list, settings=settings)"
        )

with open(routes_path, "w", encoding="utf-8") as f:
    f.write(routes)


# 2. Update Font and Text
# Update base.html to use a more premium font like 'Outfit'
base_html = os.path.join(base, "templates/base.html")
with open(base_html, "r", encoding="utf-8") as f:
    html = f.read()
html = html.replace(
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">',
    '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">'
)
with open(base_html, "w", encoding="utf-8") as f:
    f.write(html)

# Update style.css
css_path = os.path.join(base, "static/css/style.css")
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()
css = css.replace("font-family: 'Inter', -apple-system, sans-serif;", "font-family: 'Outfit', -apple-system, sans-serif;")
with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)


# Update index.html
index_path = os.path.join(base, "templates/cliente/index.html")
with open(index_path, "r", encoding="utf-8") as f:
    index = f.read()
index = index.replace("¿Qué servicio buscas?", "Elige tu servicio")
with open(index_path, "w", encoding="utf-8") as f:
    f.write(index)

