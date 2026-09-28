import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "static/css/style.css")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# Remove .service-card > div and .service-header column overrides
content = re.sub(r'\s*\.service-card > div\s*\{[^}]+\}', '', content)
content = re.sub(r'\s*\.service-card > div > div:last-child\s*\{[^}]+\}', '', content)
content = re.sub(r'\s*\.service-header\s*\{[^}]+\}', '', content)
content = re.sub(r'\s*\.service-header > div:last-child\s*\{[^}]+\}', '', content)

# Adjust service card padding on mobile to make it more compact
mobile_padding = """
    .service-card { padding: 1rem; }
    .service-card h3 { font-size: 1.05rem; }
    .service-price { font-size: 1.1rem; }
"""

# Insert into max-width 768px block
if "/* CLIENT WIZARD RESPONSIVE */" in content:
    content = content.replace("/* CLIENT WIZARD RESPONSIVE */", "/* CLIENT WIZARD RESPONSIVE */\n" + mobile_padding)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
