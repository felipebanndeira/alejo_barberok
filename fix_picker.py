import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "templates/cliente/index.html")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_picker = """            <div style="width: 100%; text-align: center;">
                <button type="button" class="btn-gold" onclick="try { document.getElementById('date-picker').showPicker(); } catch(e) { document.getElementById('date-picker').focus(); }" style="width: 100%; padding: 1.2rem; font-size: 1.1rem; display: flex; justify-content: center; gap: 10px; align-items: center; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">
                    <i data-lucide="calendar" style="width: 22px;"></i>
                    <span id="date-display">Elegir Fecha</span>
                </button>
                <input type="date" id="date-picker" style="position: absolute; top: 50%; left: 50%; width: 1px; height: 1px; opacity: 0; z-index: -1;">
            </div>"""

new_picker = """            <div style="width: 100%; text-align: center; position: relative;">
                <div class="btn-gold" style="width: 100%; padding: 1.2rem; font-size: 1.1rem; display: flex; justify-content: center; gap: 10px; align-items: center; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; pointer-events: none;">
                    <i data-lucide="calendar" style="width: 22px;"></i>
                    <span id="date-display">Elegir Fecha</span>
                </div>
                <input type="date" id="date-picker" style="position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; cursor: pointer; -webkit-appearance: none;">
            </div>"""

content = content.replace(old_picker, new_picker)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
