import os, re

base = r"c:\Users\usser\Documents\Alejo barber"
files = ["templates/admin/finances.html", "templates/admin/blocks.html", "templates/admin/users.html", "templates/admin/settings.html", "templates/admin/dashboard.html"]

for rel in files:
    path = os.path.join(base, rel)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Remove ANY li containing admin.settings or admin.logout
    content = re.sub(r'^\s*<li[^>]*><a[^>]*href="\{\{\s*url_for\(\'admin\.settings\'\)\s*\}\}"[^>]*>.*?</a></li>\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*<li[^>]*><a[^>]*href="\{\{\s*url_for\(\'admin\.logout\'\)\s*\}\}"[^>]*>.*?</a></li>\n', '', content, flags=re.MULTILINE)
    
    # Just in case, clean up any stray separators
    content = re.sub(r'^\s*<li class="sidebar-separator"></li>\n', '', content, flags=re.MULTILINE)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Cleaned {rel}")
