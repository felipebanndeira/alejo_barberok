import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"

# 1. Dashboard to "Panel de Control"
admin_templates = ["dashboard.html", "settings.html", "users.html", "blocks.html"]
for template in admin_templates:
    path = os.path.join(base, "templates/admin", template)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace(">Dashboard<", ">Panel de Control<")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

# 2. Remove Logo upload in settings.html
settings_path = os.path.join(base, "templates/admin/settings.html")
with open(settings_path, "r", encoding="utf-8") as f:
    content = f.read()

logo_pattern = r'<label>Logo \(PNG/JPG\).*?{% endif %}'
content = re.sub(logo_pattern, '', content, flags=re.DOTALL)

with open(settings_path, "w", encoding="utf-8") as f:
    f.write(content)

# 3. Password visibility in users.html
users_path = os.path.join(base, "templates/admin/users.html")
with open(users_path, "r", encoding="utf-8") as f:
    content = f.read()

old_pwd = '<input type="password" name="password" required>'
new_pwd = """<div style="position: relative;">
                        <input type="password" id="password" name="password" required style="padding-right: 40px;">
                        <button type="button" onclick="const p = document.getElementById('password'); p.type = p.type === 'password' ? 'text' : 'password';" style="position:absolute; right:10px; top:15px; background:none; border:none; color:var(--text-dim); cursor:pointer;"><i data-lucide="eye" style="width:18px;"></i></button>
                    </div>"""
if old_pwd in content:
    content = content.replace(old_pwd, new_pwd)
with open(users_path, "w", encoding="utf-8") as f:
    f.write(content)

# 4. Translate Statuses in dashboard.html
dash_path = os.path.join(base, "templates/admin/dashboard.html")
with open(dash_path, "r", encoding="utf-8") as f:
    dash = f.read()

old_status = '<td><span class="badge {{ a.status }}">{{ a.status|capitalize }}</span></td>'
new_status = """<td><span class="badge {{ a.status }}">
                            {% if a.status == 'pending' %}Pendiente{% endif %}
                            {% if a.status == 'confirmed' %}Confirmado{% endif %}
                            {% if a.status == 'cancelled' %}Cancelado{% endif %}
                        </span></td>"""
dash = dash.replace(old_status, new_status)

with open(dash_path, "w", encoding="utf-8") as f:
    f.write(dash)

# Update base.html to have lang="es"
base_path = os.path.join(base, "templates/base.html")
with open(base_path, "r", encoding="utf-8") as f:
    base_html = f.read()

base_html = base_html.replace('<html lang="en">', '<html lang="es">')
if '<html lang="es">' not in base_html and '<html' in base_html:
    base_html = base_html.replace('<html>', '<html lang="es">')

with open(base_path, "w", encoding="utf-8") as f:
    f.write(base_html)

