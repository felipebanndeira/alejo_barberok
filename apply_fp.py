import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "templates/cliente/index.html")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Add flatpickr css to the top block
fp_css = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css">\n<link rel="stylesheet" type="text/css" href="https://npmcdn.com/flatpickr/dist/themes/dark.css">'
if fp_css not in content:
    content = content.replace('{% block content %}', '{% block content %}\n' + fp_css)

# Change the date picker HTML back to a normal input but styled, and remove the overlay hack
old_html = """            <div style="width: 100%; text-align: center; position: relative; overflow: hidden; border-radius: 8px;">
                <div class="btn-gold" style="width: 100%; padding: 1.2rem; font-size: 1.1rem; display: flex; justify-content: center; gap: 10px; align-items: center; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; pointer-events: none;">
                    <i data-lucide="calendar" style="width: 22px;"></i>
                    <span id="date-display">Elegir Fecha</span>
                </div>
                <input type="date" id="date-picker" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0.01; cursor: pointer; z-index: 50;">
            </div>"""

new_html = """            <div style="width: 100%; text-align: center;">
                <input type="text" id="date-picker" class="btn-gold" placeholder="ELEGIR FECHA" readonly="readonly" style="width: 100%; padding: 1.2rem; font-size: 1.1rem; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; text-align: center; cursor: pointer; border: none; font-family: inherit;">
            </div>"""

content = content.replace(old_html, new_html)

# Add flatpickr js to the bottom block
fp_js = """<script src="https://cdn.jsdelivr.net/npm/flatpickr"></script>
<script src="https://npmcdn.com/flatpickr/dist/l10n/es.js"></script>
<script>
    flatpickr("#date-picker", {
        locale: "es",
        minDate: "today",
        disableMobile: "true",
        onChange: function(selectedDates, dateStr, instance) {
            // Trigger the change event manually so main.js picks it up
            const event = new Event('change');
            document.getElementById('date-picker').dispatchEvent(event);
        }
    });
</script>"""

if 'flatpickr("#date-picker"' not in content:
    content = content.replace('{% endblock %}', fp_js + '\n{% endblock %}')

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
