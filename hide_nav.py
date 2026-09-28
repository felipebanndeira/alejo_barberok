import os

base = r"c:\Users\usser\Documents\Alejo barber"
css_path = os.path.join(base, "static/css/style.css")

with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

hide_css = """
    .sidebar ul li:nth-child(3),
    .sidebar ul li:nth-child(5),
    .sidebar ul li:nth-child(6),
    .sidebar ul li:nth-child(7) {
        display: none !important;
    }
"""

if hide_css not in css:
    # Insert it inside @media (max-width: 768px)
    media_query_start = css.find("@media (max-width: 768px) {")
    if media_query_start != -1:
        insert_pos = css.find(".sidebar {", media_query_start)
        if insert_pos != -1:
            css = css[:insert_pos] + hide_css + css[insert_pos:]
            with open(css_path, "w", encoding="utf-8") as f:
                f.write(css)
            print("CSS updated.")
        else:
            print("Could not find .sidebar { inside media query")
    else:
        print("Could not find media query")
