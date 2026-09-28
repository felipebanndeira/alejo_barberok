import os

base = r"c:\Users\usser\Documents\Alejo barber"
css_path = os.path.join(base, "static/css/style.css")

with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# Replace the previous block with the new one
old_block = """    .sidebar ul li:nth-child(3),
    .sidebar ul li:nth-child(5),
    .sidebar ul li:nth-child(6),
    .sidebar ul li:nth-child(7) {
        display: none !important;
    }"""

new_block = """    .sidebar ul li:nth-child(5),
    .sidebar ul li:nth-child(6),
    .sidebar ul li:nth-child(7) {
        display: none !important;
    }"""

if old_block in css:
    css = css.replace(old_block, new_block)
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(css)
    print("Restored Horarios.")
else:
    print("Old block not found.")

