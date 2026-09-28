import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "templates/admin/dashboard.html")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the specific forms that cancel appointments
old_form = '<form method="POST" action="{{ url_for(\'admin.update_status\', id=a.id) }}" style="margin:0;">\n                            <input type="hidden" name="status" value="cancelled">'
new_form = '<form method="POST" action="{{ url_for(\'admin.update_status\', id=a.id) }}" style="margin:0;" onsubmit="return confirm(\'¿Seguro que querés cancelar este turno?\');">\n                            <input type="hidden" name="status" value="cancelled">'

content = content.replace(old_form, new_form)

# Desktop form might have different indentation
old_form_desktop = '<form method="POST" action="{{ url_for(\'admin.update_status\', id=a.id) }}" style="margin:0;">\n                                <input type="hidden" name="status" value="cancelled">'
new_form_desktop = '<form method="POST" action="{{ url_for(\'admin.update_status\', id=a.id) }}" style="margin:0;" onsubmit="return confirm(\'¿Seguro que querés cancelar este turno?\');">\n                                <input type="hidden" name="status" value="cancelled">'
content = content.replace(old_form_desktop, new_form_desktop)


with open(path, "w", encoding="utf-8") as f:
    f.write(content)
