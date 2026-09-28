import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"

# 1. Update index.html to remove placeholders and icons in step 3
index_path = os.path.join(base, "templates/cliente/index.html")
with open(index_path, "r", encoding="utf-8") as f:
    index = f.read()

index = index.replace('placeholder="Ej: Felipe Bandeira" ', '')
index = index.replace('placeholder="Ej: 3755-123456" ', '')
index = re.sub(r'<i data-lucide="user"[^>]*></i>\s*', '', index)
index = re.sub(r'<i data-lucide="phone"[^>]*></i>\s*', '', index)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(index)

# 2. Update admin templates to remove sidebar icons
admin_templates = ["dashboard.html", "settings.html", "users.html", "blocks.html"]
for template in admin_templates:
    t_path = os.path.join(base, "templates/admin", template)
    if os.path.exists(t_path):
        with open(t_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Remove lucide icons from sidebar links
        content = re.sub(r'<i data-lucide="layout-dashboard"></i>\s*', '', content)
        content = re.sub(r'<i data-lucide="settings"></i>\s*', '', content)
        content = re.sub(r'<i data-lucide="users"></i>\s*', '', content)
        content = re.sub(r'<i data-lucide="calendar-off"></i>\s*', '', content)
        content = re.sub(r'<i data-lucide="log-out"></i>\s*', '', content)
        
        with open(t_path, "w", encoding="utf-8") as f:
            f.write(content)

