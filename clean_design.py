import os

base = r"c:\Users\usser\Documents\Alejo barber"

# 1. Update base.html to add fonts
base_path = os.path.join(base, "templates/base.html")
with open(base_path, "r", encoding="utf-8") as f:
    html = f.read()

# Replace fonts
import re
html = re.sub(r'<link href="https://fonts.googleapis.com/css2[^>]+>', '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600&family=Space+Grotesk:wght@400;500;600&display=swap" rel="stylesheet">', html)

with open(base_path, "w", encoding="utf-8") as f:
    f.write(html)

# 2. Update style.css for ultra-clean minimalist futuristic design
css_path = os.path.join(base, "static/css/style.css")
new_css = ''':root {
    --bg-color: #030303; 
    --card-bg: #0a0a0a; 
    --primary-gold: #e2c073;
    --primary-gold-dim: rgba(226, 192, 115, 0.08);
    --text-light: #ffffff;
    --text-dim: #7a7a7a; 
    --border-color: #1a1a1a; 
    
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    background-color: var(--bg-color);
    color: var(--text-light);
    min-height: 100vh;
    padding-bottom: 100px;
    -webkit-font-smoothing: antialiased;
}

h1, h2, h3, h4 { font-weight: 500; letter-spacing: -0.02em; }
.gold-text { color: var(--primary-gold); }
.text-dim { color: var(--text-dim); }

/* Monospace / Tech numbers */
.num-font {
    font-family: 'Space Grotesk', monospace;
    letter-spacing: -0.03em;
}

/* Header */
.top-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 2rem;
    border-bottom: 1px solid var(--border-color);
}
.header-logo {
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 500;
    font-size: 1.1rem;
    letter-spacing: -0.01em;
}
.header-logo img { height: 24px; }
.header-nav a {
    color: var(--text-dim);
    text-decoration: none;
    margin-left: 1.5rem;
    font-size: 0.9rem;
    font-weight: 500;
    transition: color 0.2s;
}
.header-nav a:hover, .header-nav a.active { color: var(--text-light); }

/* Stepper UI */
.stepper-wrapper {
    max-width: 500px;
    margin: 3rem auto 2rem;
    padding: 0 1.5rem;
}
.stepper-lines {
    display: flex;
    gap: 6px;
    margin-bottom: 1.5rem;
}
.step-line {
    height: 2px;
    background: var(--border-color);
    flex: 1;
    transition: background 0.4s ease;
}
.step-line.active { background: var(--primary-gold); }
.step-label {
    text-align: center;
    color: var(--text-dim);
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.container { max-width: 500px; margin: 0 auto; padding: 0 1.5rem; }

.step-container { display: none; animation: fadeUp 0.4s cubic-bezier(0.16, 1, 0.3, 1); }
.step-container.active { display: block; }
@keyframes fadeUp { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }

/* Services */
.service-card {
    background: transparent;
    border: 1px solid var(--border-color);
    padding: 1.25rem 1.5rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    cursor: pointer;
    transition: all 0.25s ease;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.service-card:hover { border-color: #333; }
.service-card.selected {
    border-color: var(--primary-gold);
    background: var(--primary-gold-dim);
}
.service-card h3 { font-size: 1.1rem; margin-bottom: 0.2rem; }
.service-price { font-size: 1.15rem; font-weight: 500; }

.check-icon { display: none; color: var(--primary-gold); }

/* Forms */
input, select, textarea {
    width: 100%;
    background: transparent;
    border: 1px solid var(--border-color);
    color: var(--text-light);
    padding: 1rem 1.25rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    font-family: inherit;
    font-size: 1rem;
    transition: border-color 0.2s;
}
input:focus, select:focus, textarea:focus { outline: none; border-color: var(--primary-gold); }
input::placeholder { color: #444; }
input[type="date"]::-webkit-calendar-picker-indicator { filter: invert(0.6); cursor: pointer; }

/* Time Slots */
.time-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(85px, 1fr));
    gap: 0.75rem;
}
.time-slot {
    padding: 0.8rem 0;
    text-align: center;
    background: transparent;
    border: 1px solid var(--border-color);
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 0.95rem;
}
.time-slot:hover { border-color: #444; }
.time-slot.selected {
    background: var(--primary-gold);
    color: var(--bg-color);
    border-color: var(--primary-gold);
    font-weight: 600;
}

/* Sticky Footer */
.sticky-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background: rgba(3, 3, 3, 0.85);
    backdrop-filter: blur(12px);
    border-top: 1px solid var(--border-color);
    padding: 1rem 1.5rem;
    display: flex;
    justify-content: center;
    z-index: 100;
}
.footer-content {
    max-width: 500px;
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.footer-total p { font-size: 0.75rem; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.05em;}
.footer-total h3 { font-size: 1.4rem; margin: 0; color: var(--text-light); }

.btn-white {
    background: var(--text-light);
    color: var(--bg-color);
    border: none;
    padding: 0.8rem 1.8rem;
    border-radius: 6px;
    font-weight: 600;
    font-size: 0.95rem;
    cursor: pointer;
    transition: transform 0.2s;
}
.btn-white:active { transform: scale(0.97); }
.btn-outline {
    background: transparent;
    color: var(--text-dim);
    border: none;
    padding: 0.8rem 0;
    font-weight: 500;
    cursor: pointer;
    transition: color 0.2s;
}
.btn-outline:hover { color: var(--text-light); }

.btn-gold {
    background: var(--primary-gold);
    color: var(--bg-color);
    border: none;
    padding: 1rem 1.5rem;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1rem;
    font-weight: 600;
    transition: opacity 0.2s;
    width: 100%;
}
.btn-gold:hover { opacity: 0.9; }

/* Admin */
.admin-layout { display: grid; grid-template-columns: 240px 1fr; min-height: 100vh; }
.sidebar { background: var(--bg-color); border-right: 1px solid var(--border-color); padding: 2rem 1.5rem; }
.sidebar ul { list-style: none; margin-top: 2rem; }
.sidebar li { margin-bottom: 0.3rem; }
.sidebar a {
    color: var(--text-dim);
    text-decoration: none;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0.75rem 1rem;
    border-radius: 6px;
    font-size: 0.95rem;
}
.sidebar a:hover, .sidebar a.active { color: var(--text-light); background: var(--card-bg); }
.admin-content { padding: 3rem; background: var(--bg-color); }

.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0 1rem;
}
.sidebar-logo img { height: 24px; }
.sidebar-logo h2 { font-size: 1.1rem; font-weight: 500; margin: 0; color: var(--text-light); letter-spacing: -0.01em;}

.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.25rem; margin-bottom: 2.5rem; }
.stat-card { padding: 1.5rem; border-radius: 8px; background: transparent; border: 1px solid var(--border-color);}
.stat-card h3 { font-size: 2rem; margin: 0.5rem 0 0; font-weight: 500; color: var(--text-light); }

.table-container { background: transparent; border: 1px solid var(--border-color); border-radius: 8px; overflow: hidden; }
table { width: 100%; border-collapse: collapse; }
th, td { padding: 1rem 1.5rem; text-align: left; border-bottom: 1px solid var(--border-color); }
th { color: var(--text-dim); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 500; }
tr:last-child td { border-bottom: none; }

.badge { padding: 0.3rem 0.6rem; border-radius: 4px; font-size: 0.8rem; font-weight: 500; }
.badge.pending { background: rgba(255, 193, 7, 0.1); color: #ffc107; border: 1px solid rgba(255, 193, 7, 0.2); }
.badge.confirmed { background: rgba(40, 167, 69, 0.1); color: #28a745; border: 1px solid rgba(40, 167, 69, 0.2); }
.badge.cancelled { background: rgba(220, 53, 69, 0.1); color: #dc3545; border: 1px solid rgba(220, 53, 69, 0.2); }

.flex-between { display: flex; justify-content: space-between; align-items: center; }
.mt-2 { margin-top: 2rem; }
.mb-2 { margin-bottom: 1.5rem; }
.text-center { text-align: center; }
.w-100 { width: 100%; }

.actions-cell { display: flex; gap: 8px; }
.btn-icon {
    background: transparent;
    border: 1px solid var(--border-color);
    color: var(--text-light);
    padding: 0.4rem;
    border-radius: 4px;
    cursor: pointer;
    display: inline-flex;
    transition: all 0.2s;
}
.btn-icon:hover { background: var(--card-bg); border-color: #444; }
.btn-icon.delete:hover { background: rgba(220, 53, 69, 0.1); color: #dc3545; border-color: rgba(220, 53, 69, 0.3); }

/* Form layout inside settings */
.glass-panel { background: transparent; padding: 2rem; border-radius: 8px; border: 1px solid var(--border-color); }
label { display: block; margin-bottom: 0.5rem; font-size: 0.9rem; color: var(--text-dim); }
'''
with open(css_path, "w", encoding="utf-8") as f:
    f.write(new_css)

# 3. Apply .num-font to index.html and admin templates
index_path = os.path.join(base, "templates/cliente/index.html")
with open(index_path, "r", encoding="utf-8") as f:
    index = f.read()

index = index.replace('class="service-price gold-text"', 'class="service-price gold-text num-font"')
index = index.replace('id="footer-total"', 'id="footer-total" class="num-font"')
index = index.replace('class="time-slot"', 'class="time-slot num-font"')

with open(index_path, "w", encoding="utf-8") as f:
    f.write(index)

dashboard_path = os.path.join(base, "templates/admin/dashboard.html")
with open(dashboard_path, "r", encoding="utf-8") as f:
    dashboard = f.read()

dashboard = dashboard.replace('<h3>${{ caja_hoy }}</h3>', '<h3 class="num-font">${{ caja_hoy }}</h3>')
dashboard = dashboard.replace('<h3>{{ appointments_today }}</h3>', '<h3 class="num-font">{{ appointments_today }}</h3>')
dashboard = dashboard.replace('<h3>{{ total_clients }}</h3>', '<h3 class="num-font">{{ total_clients }}</h3>')
dashboard = dashboard.replace('{{ a.time }}</td>', '{{ a.time }}</td>').replace('<td style="font-size: 1.1rem; font-weight: 600; color: var(--primary-gold);">', '<td class="num-font" style="font-size: 1.05rem; font-weight: 500; color: var(--primary-gold);">')

# Admin sidebar logo was requested to be exactly like the client one (small). 
# It already uses `<img src="..." alt="Logo">` with `height: 24px;` in the new CSS.
# In the client, header-logo img is also 24px. So they will be identical in size.

with open(dashboard_path, "w", encoding="utf-8") as f:
    f.write(dashboard)

