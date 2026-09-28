import os

base = r"c:\Users\usser\Documents\Alejo barber"

# 1. Update base.html to include Plus Jakarta Sans instead of Space Grotesk
base_html_path = os.path.join(base, "templates/base.html")
with open(base_html_path, "r", encoding="utf-8") as f:
    base_html = f.read()

base_html = base_html.replace("Space+Grotesk:wght@400;500;600;700", "Plus+Jakarta+Sans:wght@400;500;600;700")

with open(base_html_path, "w", encoding="utf-8") as f:
    f.write(base_html)

# 2. Update style.css to use Plus Jakarta Sans
css_path = os.path.join(base, "static/css/style.css")
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

css = css.replace("'Space Grotesk', sans-serif;", "'Plus Jakarta Sans', sans-serif;")
# Also adjust letter spacing slightly as Plus Jakarta is already well proportioned
css = css.replace("letter-spacing: -0.02em;", "letter-spacing: -0.01em;")

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)

