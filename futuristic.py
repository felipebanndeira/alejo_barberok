import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"

# 1. Update style.css colors and mouse aura
css_path = os.path.join(base, "static/css/style.css")
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# Replace gold colors with a bright, vibrant, futuristic gold
css = css.replace("--primary-gold: #C9A34E;", "--primary-gold: #FFCC00;")
css = css.replace("--light-gold: #E8CD8A;", "--light-gold: #FFE666;")
css = css.replace("--dark-gold: #8A6F2F;", "--dark-gold: #CC9900;")
css = css.replace("--primary-gold-dim: rgba(201, 163, 78, 0.15);", "--primary-gold-dim: rgba(255, 204, 0, 0.15);")
css = css.replace("rgba(201, 163, 78", "rgba(255, 204, 0")

# Mouse aura to gold (replace vinotinto)
css = css.replace(
"background: radial-gradient(circle, rgba(128, 0, 32, 0.25) 0%, rgba(128, 0, 32, 0) 70%);", 
"background: radial-gradient(circle, rgba(255, 204, 0, 0.15) 0%, rgba(255, 204, 0, 0) 70%);\n    filter: blur(10px);"
)

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)

# 2. Update index.html (Client) to remove icons from services
index_path = os.path.join(base, "templates/cliente/index.html")
with open(index_path, "r", encoding="utf-8") as f:
    index = f.read()

# The services currently have an icon block injected. 
# We'll just replace the whole div that wraps the icon and text back to a clean text-only div.
# We will use regex to find the block and remove the icon.
icon_block_pattern = r'<div style="display:flex; gap: 12px; align-items: center;">.*?<i data-lucide="[^"]+"[^>]*></i>\s*<div>\s*<h3 class="space-font">([^<]+)</h3>\s*<p class="text-dim"[^>]*>30 minutos</p>\s*</div>\s*</div>'

def replacer(match):
    name = match.group(1)
    return f'<div><h3 class="space-font">{name}</h3><p class="text-dim" style="font-size: 0.85rem;">30 minutos</p></div>'

index = re.sub(icon_block_pattern, replacer, index, flags=re.DOTALL)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(index)

# 3. Update dashboard.html (Admin) to remove icons from stats cards
dashboard_path = os.path.join(base, "templates/admin/dashboard.html")
with open(dashboard_path, "r", encoding="utf-8") as f:
    dashboard = f.read()

dashboard = dashboard.replace('<i data-lucide="dollar-sign" class="gold-text"></i>\n', '')
dashboard = dashboard.replace('<i data-lucide="calendar" class="gold-text"></i>\n', '')
dashboard = dashboard.replace('<i data-lucide="users" class="gold-text"></i>\n', '')

# Adjust margin so the text isn't pushed down since the icon is gone
dashboard = dashboard.replace('style="margin-top:0.5rem"', 'style="margin-top:0"')

with open(dashboard_path, "w", encoding="utf-8") as f:
    f.write(dashboard)

