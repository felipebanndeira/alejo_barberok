import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"
css_path = os.path.join(base, "static/css/style.css")

with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# 1. Update colors
css = css.replace("--primary-gold: #D4AF37;", "--primary-gold: #C9A34E;")
css = css.replace("--primary-gold-dim: rgba(212, 175, 55, 0.1);", "--primary-gold-dim: rgba(201, 163, 78, 0.15);")
css = css.replace("--neon-gold: #FFB300;", "--light-gold: #E8CD8A;\n    --dark-gold: #8A6F2F;")

# Replace mentions of primary-gold and neon-gold
css = css.replace("color: var(--neon-gold);", "color: var(--light-gold);")
css = css.replace("rgba(255, 215, 0", "rgba(201, 163, 78")

# 2. Update fonts
css = css.replace("font-family: 'Plus Jakarta Sans'", "font-family: 'Inter'")
# ensure space grotesk class
if ".space-font" not in css:
    css += "\n.space-font { font-family: 'Space Grotesk', sans-serif; letter-spacing: -0.02em; }\n"

# 3. Sidebar updates
# glow on active sidebar item
css = css.replace(
".sidebar a:hover, .sidebar a.active { color: var(--text-light); background: var(--card-bg); }",
".sidebar a:hover { color: var(--text-light); background: rgba(255,255,255,0.03); }\n.sidebar a.active { color: var(--primary-gold); background: var(--primary-gold-dim); box-shadow: 0 0 15px rgba(201, 163, 78, 0.15); border: 1px solid rgba(201, 163, 78, 0.3); }"
)

# Sidebar separators
css += "\n.sidebar-separator { border-top: 1px solid var(--border-color); margin: 1.5rem 0; }\n"

# 4. Spacing updates
css = css.replace("gap: 1.25rem; margin-bottom: 2.5rem;", "gap: 2rem; margin-bottom: 3rem;") # stats grid
css = css.replace("padding: 1rem 1.5rem;", "padding: 1.25rem 1.5rem;") # table cells

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)

# Update base.html fonts and lucide configuration
base_html = os.path.join(base, "templates/base.html")
with open(base_html, "r", encoding="utf-8") as f:
    html = f.read()

html = re.sub(r'<link href="https://fonts.googleapis.com/css2[^>]+>', '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">', html)
html = html.replace('lucide.createIcons();', "lucide.createIcons({\n            attrs: {\n                'stroke-width': 1.5\n            }\n        });")

with open(base_html, "w", encoding="utf-8") as f:
    f.write(html)

# Add thousands separator in Jinja context (we can use a custom filter, or just format inside Python)
dash_path = os.path.join(base, "routes/admin_routes.py")
with open(dash_path, "r", encoding="utf-8") as f:
    routes = f.read()

if "caja_hoy = f\"{caja:,}\".replace(',', '.')" not in routes:
    routes = routes.replace(
        "caja_hoy = caja if caja else 0",
        "caja_hoy = f\"{caja:,}\".replace(',', '.') if caja else '0'"
    )
    with open(dash_path, "w", encoding="utf-8") as f:
        f.write(routes)

# Add space-font class to numbers in templates/admin/dashboard.html
dashboard = os.path.join(base, "templates/admin/dashboard.html")
with open(dashboard, "r", encoding="utf-8") as f:
    d_html = f.read()

d_html = d_html.replace('<h3>', '<h3 class="space-font" style="font-weight: 700;">')
d_html = d_html.replace('<h3 class="num-font">', '<h3 class="space-font" style="font-weight: 700;">')
d_html = d_html.replace('class="num-font"', 'class="space-font"')
d_html = d_html.replace('<h2 class="mb-2">', '<h2 class="mb-2 space-font">')
d_html = d_html.replace('<h3 class="mb-2">', '<h3 class="mb-2 space-font">')
d_html = d_html.replace('<li class="mt-2">', '<div class="sidebar-separator"></div>\n            <li>')

with open(dashboard, "w", encoding="utf-8") as f:
    f.write(d_html)

# Update sidebar in other templates
for template in ["settings.html", "users.html", "blocks.html"]:
    t_path = os.path.join(base, f"templates/admin/{template}")
    with open(t_path, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace('<li class="mt-2">', '<div class="sidebar-separator"></div>\n            <li>')
    content = content.replace('<h2 class="mb-2">', '<h2 class="mb-2 space-font">')
    content = content.replace('<h3 class="mb-2">', '<h3 class="mb-2 space-font">')
    with open(t_path, "w", encoding="utf-8") as f:
        f.write(content)

