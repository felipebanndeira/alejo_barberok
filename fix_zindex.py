import os

base = r"c:\Users\usser\Documents\Alejo barber"
css_path = os.path.join(base, "static/css/style.css")

with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

css = css.replace("z-index: 0;", "z-index: -1;")

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)
