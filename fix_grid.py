import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"
css_path = os.path.join(base, "static/css/style.css")

with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# Replace the first .admin-layout in the media query
css = css.replace('.admin-layout {\n        flex-direction: column;\n    }', '.admin-layout {\n        display: block;\n    }')

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)

