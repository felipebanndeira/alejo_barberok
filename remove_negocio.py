import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"
settings_path = os.path.join(base, "templates/admin/settings.html")

with open(settings_path, "r", encoding="utf-8") as f:
    content = f.read()

# Pattern to remove the Negocio panel
pattern = r'<div class="glass-panel">\s*<h3 class="mb-2 space-font">Negocio</h3>.*?</div>\s*<div class="glass-panel">'
replacement = '<div class="glass-panel" style="max-width: 600px;">'

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open(settings_path, "w", encoding="utf-8") as f:
    f.write(content)

