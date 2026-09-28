import os, re

base = r"c:\Users\usser\Documents\Alejo barber"
css_path = os.path.join(base, "static/css/style.css")

with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# The 768px block uses a horizontal scrolling tab bar for sidebar
# We need to replace ONLY the sidebar rules inside the first 768px block  
# with a simple hide-icons rule, and let 480px handle the bottom nav

old_768_sidebar = """.sidebar {
        position: static;
        width: 100%;
        height: auto;
        min-height: auto;
        padding: 1rem;
        background: transparent;
        border-right: none;
        border-bottom: 1px solid var(--glass-border);
        display: block;
    }
    
    .sidebar-logo {
        display: block;
        margin-bottom: 1rem;
    }
    
    .sidebar ul {
        width: auto;
        display: flex;
        flex-direction: row;
        overflow-x: auto;
        white-space: nowrap;
        gap: 0.5rem;
        padding-bottom: 0.5rem;
        justify-content: flex-start;
    }
    
    .sidebar ul li {
        list-style: none;
    }
    
    .sidebar ul li a {
        padding: 0.6rem 1rem;
        border-radius: 20px;
        background: rgba(255,255,255,0.03) !important;
        color: var(--text-light);
        font-size: 1rem;
        font-weight: 500;
        display: inline-block;
        border: none;
    }
    
    .sidebar ul li a.active {
        background: rgba(255, 204, 0, 0.1) !important;
        color: var(--primary-gold) !important;
        border: none;
    }
    
    .sidebar-separator {
        display: none;
    }
    
    .admin-content {
        padding: 1rem;
    }"""

new_768_sidebar = """.sidebar ul li a svg,
    .sidebar ul li a i { display: none !important; }
    .sidebar-separator { display: none; }
    .admin-content { padding: 1rem; }"""

if old_768_sidebar in css:
    css = css.replace(old_768_sidebar, new_768_sidebar)
    print("768px sidebar block replaced.")
else:
    print("Old 768px sidebar block not found exactly.")

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)
