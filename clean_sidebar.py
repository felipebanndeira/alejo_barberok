import os

base = r"c:\Users\usser\Documents\Alejo barber"
files = ["templates/admin/finances.html", "templates/admin/blocks.html", "templates/admin/users.html", "templates/admin/settings.html"]

for rel in files:
    path = os.path.join(base, rel)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Remove separator and logout
    content = content.replace('<div class="sidebar-separator"></div>', '')
    content = content.replace('<li><a href="{{ url_for(\'admin.logout\') }}">Salir</a></li>', '')
    content = content.replace('<li><a href="{{ url_for(\'admin.logout\') }}"><i data-lucide="log-out"></i> Salir</a></li>', '')
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Cleaned {rel}")
