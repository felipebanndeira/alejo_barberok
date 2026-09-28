import os, re

base = r"c:\Users\usser\Documents\Alejo barber"
css_path = os.path.join(base, "static/css/style.css")

with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# Remove old nth-child hide rules
old_hide = """    .sidebar ul li:nth-child(5),
    .sidebar ul li:nth-child(6),
    .sidebar ul li:nth-child(7) {
        display: none !important;
    }"""
css = css.replace(old_hide, "")

# Find the bottom nav block (480px media query) and replace all sidebar ul styles inside
old_bottom = re.search(r'(@media \(max-width: 480px\) \{.*?)(\}[\s]*?(?=@media|\Z))', css, re.DOTALL)
if old_bottom:
    old_block = old_bottom.group(0)
    new_block = """@media (max-width: 480px) {
    .sidebar {
        position: fixed;
        bottom: 0; left: 0; right: 0;
        width: 100%;
        height: auto;
        padding: 0;
        background: #0f0f0f;
        border-top: 1px solid #1f1f1f;
        z-index: 100;
    }
    .sidebar-logo { display: none; }
    .sidebar ul {
        width: 100%;
        display: flex;
        justify-content: space-around;
        align-items: stretch;
        padding: 0; margin: 0;
        list-style: none;
    }
    .sidebar ul li { flex: 1; }
    .sidebar ul li a {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 0.85rem 0.5rem;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.01em;
        background: transparent !important;
        border-radius: 0 !important;
        color: #71717a;
        border: none !important;
        border-top: 2px solid transparent;
        transition: color 0.15s, border-color 0.15s;
        text-decoration: none;
        white-space: nowrap;
    }
    .sidebar ul li a.active {
        color: #facc15 !important;
        border-top: 2px solid #facc15 !important;
        background: transparent !important;
    }
    .sidebar ul li a:hover:not(.active) { color: #a1a1aa; }
    .sidebar ul li a svg,
    .sidebar ul li a i { display: none !important; }
    .sidebar-separator { display: none !important; }
    .admin-content { padding: 1rem; padding-bottom: 80px; }
}
"""
    css = css.replace(old_block, new_block)
    print("Bottom nav replaced.")
else:
    print("480px media query not found, appending...")
    css += "\n" + """@media (max-width: 480px) {
    .sidebar {
        position: fixed;
        bottom: 0; left: 0; right: 0;
        width: 100%;
        height: auto;
        padding: 0;
        background: #0f0f0f;
        border-top: 1px solid #1f1f1f;
        z-index: 100;
    }
    .sidebar-logo { display: none; }
    .sidebar ul {
        width: 100%;
        display: flex;
        justify-content: space-around;
        align-items: stretch;
        padding: 0; margin: 0;
        list-style: none;
    }
    .sidebar ul li { flex: 1; }
    .sidebar ul li a {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 0.85rem 0.5rem;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.01em;
        background: transparent !important;
        border-radius: 0 !important;
        color: #71717a;
        border: none !important;
        border-top: 2px solid transparent;
        transition: color 0.15s, border-color 0.15s;
        text-decoration: none;
        white-space: nowrap;
    }
    .sidebar ul li a.active {
        color: #facc15 !important;
        border-top: 2px solid #facc15 !important;
        background: transparent !important;
    }
    .sidebar ul li a:hover:not(.active) { color: #a1a1aa; }
    .sidebar ul li a svg,
    .sidebar ul li a i { display: none !important; }
    .sidebar-separator { display: none !important; }
    .admin-content { padding: 1rem; padding-bottom: 80px; }
}"""
    print("Bottom nav appended.")

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)
