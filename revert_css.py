import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"
css_path = os.path.join(base, "static/css/style.css")

with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# Pattern to capture current ADMIN PANEL RESPONSIVE up to TABLES RESPONSIVE
old_pattern = r'/\* ADMIN PANEL RESPONSIVE \*/.*?/\* TABLES RESPONSIVE \*/'

reverted_css = """/* ADMIN PANEL RESPONSIVE */
    .admin-layout {
        flex-direction: column;
    }
    
    .sidebar {
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
    }
    
    .stats-grid {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
    
    .stats-grid .glass-panel {
        padding: 1.5rem;
    }
    
    canvas#incomeChart {
        max-height: none !important;
    }
    
    /* TABLES RESPONSIVE */"""

css = re.sub(old_pattern, reverted_css, css, flags=re.DOTALL)

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)

