import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"
css_path = os.path.join(base, "static/css/style.css")

with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# I will replace the ADMIN PANEL RESPONSIVE section with a hyper-compact version
old_admin_css_pattern = r'/\* ADMIN PANEL RESPONSIVE \*/.*?/\* TABLES RESPONSIVE \*/'

new_admin_css = """/* ADMIN PANEL RESPONSIVE */
    .admin-layout {
        flex-direction: column;
    }
    
    .sidebar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 65px;
        background: rgba(10, 10, 10, 0.95);
        backdrop-filter: blur(10px);
        border-top: 1px solid #222;
        border-right: none;
        padding: 0;
        z-index: 9999;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .sidebar-logo {
        display: none;
    }
    
    .sidebar ul {
        width: 100%;
        display: flex;
        justify-content: space-evenly;
        align-items: center;
        padding: 0;
        margin: 0;
    }
    
    .sidebar ul li {
        list-style: none;
    }
    
    .sidebar ul li a {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.5rem;
        font-size: 0.85rem;
        font-weight: 600;
        background: transparent !important;
        border-radius: 0;
        color: var(--text-dim);
    }
    
    .sidebar ul li a.active {
        color: var(--primary-gold) !important;
        background: transparent !important;
        border-bottom: 2px solid var(--primary-gold);
    }
    
    .sidebar-separator {
        display: none;
    }
    
    .admin-content {
        padding: 0.8rem;
        padding-bottom: 80px; /* Space for bottom nav */
    }
    
    .stats-grid {
        grid-template-columns: 1fr 1fr;
        gap: 0.5rem;
    }
    
    .stats-grid .glass-panel {
        padding: 0.8rem;
    }
    
    .stats-grid .glass-panel:nth-child(1) {
        grid-column: 1 / -1;
        display: flex;
        align-items: center;
    }
    
    .stats-grid .glass-panel h3 {
        font-size: 1.2rem !important;
    }
    
    .glass-panel.mb-2 {
        margin-bottom: 0.8rem !important;
        padding: 0.8rem !important;
    }
    
    canvas#incomeChart {
        max-height: 120px !important;
    }
    
    /* TABLES RESPONSIVE */"""

css = re.sub(old_admin_css_pattern, new_admin_css, css, flags=re.DOTALL)

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)

