import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "templates/cliente/index.html")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# Remove ALL flatpickr scripts blocks
content = re.sub(r'<script src="https://cdn\.jsdelivr\.net/npm/flatpickr"></script>\s*<script src="https://npmcdn\.com/flatpickr/dist/l10n/es\.js"></script>\s*<script>.*?flatpickr\("#date-picker".*?</script>\s*', '', content, flags=re.DOTALL)

# Add it exactly once inside {% block scripts %}
content = content.replace('{% block scripts %}\n<script src="{{ url_for(\'static\', filename=\'js/main.js\') }}"></script>', '{% block scripts %}\n<script src="{{ url_for(\'static\', filename=\'js/main.js\') }}"></script>\n<script src="https://cdn.jsdelivr.net/npm/flatpickr"></script>\n<script src="https://npmcdn.com/flatpickr/dist/l10n/es.js"></script>\n<script>\n    flatpickr("#date-picker", {\n        locale: "es",\n        minDate: "today",\n        dateFormat: "Y-m-d",\n        altInput: true,\n        altFormat: "d/m/Y",\n        disableMobile: true,\n        onChange: function(selectedDates, dateStr, instance) {\n            const event = new Event(\'change\');\n            document.getElementById(\'date-picker\').dispatchEvent(event);\n        }\n    });\n</script>')

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
