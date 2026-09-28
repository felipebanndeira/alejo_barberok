import os

base = r"c:\Users\usser\Documents\Alejo barber"
css_path = os.path.join(base, "static/css/style.css")

with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

responsive_css = """

/* ==========================================================================
   RESPONSIVE DESIGN (MOBILE)
   ========================================================================== */
@media (max-width: 768px) {
    /* ADMIN PANEL RESPONSIVE */
    .admin-layout {
        flex-direction: column;
    }
    
    .sidebar {
        width: 100%;
        min-height: auto;
        padding: 1rem;
        border-right: none;
        border-bottom: 1px solid var(--glass-border);
    }
    
    .sidebar-logo {
        margin-bottom: 1rem;
    }
    
    .sidebar ul {
        display: flex;
        flex-direction: row;
        overflow-x: auto;
        white-space: nowrap;
        gap: 0.5rem;
        padding-bottom: 0.5rem;
    }
    
    .sidebar ul li a {
        padding: 0.6rem 1rem;
        border-radius: 20px;
        background: rgba(255,255,255,0.03);
    }
    
    .sidebar ul li a.active {
        background: rgba(255, 204, 0, 0.1);
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
    
    /* TABLES RESPONSIVE */
    table {
        display: block;
        overflow-x: auto;
        white-space: nowrap;
    }
    
    th, td {
        padding: 0.8rem;
    }
    
    /* MODALS RESPONSIVE */
    .glass-panel {
        width: 100% !important;
        max-width: 100% !important;
        padding: 1.25rem;
    }
    
    /* MIS TURNOS RESPONSIVE */
    form[action*="mis-turnos"] {
        flex-direction: column;
        align-items: stretch !important;
    }
    
    form[action*="mis-turnos"] button {
        width: 100%;
        margin-top: 1rem;
    }
    
    .service-card > div {
        flex-direction: column;
        align-items: flex-start !important;
        gap: 1rem;
    }
    
    .service-card > div > div:last-child {
        align-items: flex-start !important;
        width: 100%;
    }
    
    .badge {
        margin-bottom: 0.5rem !important;
    }
    
    /* CLIENT WIZARD RESPONSIVE */
    .top-header {
        padding: 1rem;
    }
    
    .container {
        padding: 1rem;
        padding-bottom: 6rem;
    }
    
    .stepper-wrapper {
        padding: 1rem;
    }
    
    .service-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 1rem;
    }
    
    .service-header > div:last-child {
        width: 100%;
        justify-content: space-between;
    }
    
    .sticky-footer .footer-content {
        flex-direction: column;
        gap: 1rem;
    }
    
    .sticky-footer button {
        width: 100% !important;
    }
}
"""

if "RESPONSIVE DESIGN" not in css:
    with open(css_path, "a", encoding="utf-8") as f:
        f.write(responsive_css)

# Also fix the inline styles in mis_turnos.html that might override CSS
mis_path = os.path.join(base, "templates/cliente/mis_turnos.html")
with open(mis_path, "r", encoding="utf-8") as f:
    mis_content = f.read()

mis_content = mis_content.replace('style="display: flex; gap: 1rem; align-items: flex-end;"', 'class="mis-turnos-form" style="display: flex; gap: 1rem; align-items: flex-end;"')

with open(mis_path, "w", encoding="utf-8") as f:
    f.write(mis_content)

