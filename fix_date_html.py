import os

base = r"c:\Users\usser\Documents\Alejo barber"
index_path = os.path.join(base, "templates/cliente/index.html")

with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

old_date = '<input type="date" id="date-picker">'
new_date = """<div style="position: relative; width: 100%;">
                <div class="btn-gold" style="width: 100%; padding: 1.2rem; font-size: 1.1rem; display: flex; justify-content: center; gap: 10px; align-items: center; cursor: pointer; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">
                    <i data-lucide="calendar" style="width: 22px;"></i>
                    <span id="date-display">Elegir Fecha</span>
                </div>
                <input type="date" id="date-picker" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0; cursor: pointer;">
            </div>"""

if old_date in html:
    html = html.replace(old_date, new_date)
else:
    print("Exact old_date not found.")

# Also remove the small text "Fecha" above it because the button says "Elegir Fecha"
old_text = '<p class="text-dim mb-2" style="font-size: 0.9rem;"><i data-lucide="calendar" style="width: 14px; \ndisplay:inline-block; vertical-align:middle;"></i> Fecha</p>'
# Use regex to be safe
import re
html = re.sub(r'<p class="text-dim mb-2".*?>.*?Fecha</p>', '', html, flags=re.DOTALL)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(html)

