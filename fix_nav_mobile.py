import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"
css_path = os.path.join(base, "static/css/style.css")

with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

nav_css = """
    .top-header {
        padding: 1rem;
        flex-wrap: wrap;
    }
    .header-nav {
        display: flex;
        align-items: center;
    }
    .header-nav a {
        margin-left: 1rem;
        white-space: nowrap;
    }
"""

# Replace the existing top-header mobile rule
css = re.sub(r'\.top-header\s*\{\s*padding:\s*1rem;\s*\}', nav_css, css)

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)

