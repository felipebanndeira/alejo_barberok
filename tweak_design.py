import os

base = r"c:\Users\usser\Documents\Alejo barber"

# 1. Update style.css
css_path = os.path.join(base, "static/css/style.css")
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# Make the Siguiente button gold
css = css.replace(
'''.btn-white {
    background: var(--text-light);
    color: var(--bg-color);''',
'''.btn-white {
    background: var(--primary-gold);
    color: var(--bg-color);'''
)

# Remove Space Grotesk from num-font and make cards look better
new_css_updates = {
    # Remove Space Grotesk
    "font-family: 'Space Grotesk', monospace;": "font-family: inherit;",
    
    # Improve cards
    "background: transparent;\n    border: 1px solid var(--border-color);\n    padding: 1.25rem 1.5rem;\n    border-radius: 8px;": "background: #0f0f0f;\n    border: 1px solid #1a1a1a;\n    padding: 1.25rem 1.5rem;\n    border-radius: 12px;",
    
    # Hover on service card
    ".service-card:hover { border-color: #333; }": ".service-card:hover { border-color: #333; background: #141414; }",
    
    # Selected service card
    ".service-card.selected {\n    border-color: var(--primary-gold);\n    background: var(--primary-gold-dim);\n}": ".service-card.selected {\n    border-color: var(--primary-gold);\n    background: var(--primary-gold-dim);\n    box-shadow: 0 4px 12px rgba(226, 192, 115, 0.05);\n}",
    
    # Time slots
    "background: transparent;\n    border: 1px solid var(--border-color);\n    border-radius: 6px;": "background: #0f0f0f;\n    border: 1px solid #1a1a1a;\n    border-radius: 10px;",
    
    # Glass panels / Admin cards
    "background: transparent; padding: 2rem; border-radius: 8px; border: 1px solid var(--border-color);": "background: #0f0f0f; padding: 2rem; border-radius: 12px; border: 1px solid #1a1a1a;",
    
    # Stat cards
    "padding: 1.5rem; border-radius: 8px; background: transparent; border: 1px solid var(--border-color);": "padding: 1.5rem; border-radius: 12px; background: #0f0f0f; border: 1px solid #1a1a1a;",
    
    # Table container
    "background: transparent; border: 1px solid var(--border-color); border-radius: 8px;": "background: #0f0f0f; border: 1px solid #1a1a1a; border-radius: 12px;",
}

for old, new in new_css_updates.items():
    css = css.replace(old, new)

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)

# 2. Update base.html to remove Space Grotesk
base_path = os.path.join(base, "templates/base.html")
with open(base_path, "r", encoding="utf-8") as f:
    html = f.read()

import re
html = re.sub(r'<link href="https://fonts.googleapis.com/css2[^>]+>', '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">', html)

with open(base_path, "w", encoding="utf-8") as f:
    f.write(html)

