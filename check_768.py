import os, re

base = r"c:\Users\usser\Documents\Alejo barber"
css_path = os.path.join(base, "static/css/style.css")

with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# Find the 768px admin panel media query and check what sidebar rules it has
idx = css.find("@media (max-width: 768px) {\n    /* ADMIN PANEL RESPONSIVE */")
if idx != -1:
    snippet = css[idx:idx+2000]
    print(snippet[:2000])
else:
    print("Not found")
    # Try generic search
    for m in re.finditer(r"@media \(max-width: 768px\)", css):
        print("Found at pos:", m.start())
        print(css[m.start():m.start()+300])
        print("---")
