import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "static/css/style.css")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Add body padding-bottom to the mobile media query
mobile_padding_body = """
    body { padding-bottom: 220px !important; }
"""

if "/* CLIENT WIZARD RESPONSIVE */" in content:
    content = content.replace("/* CLIENT WIZARD RESPONSIVE */", "/* CLIENT WIZARD RESPONSIVE */\n" + mobile_padding_body)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
