import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "templates/cliente/index.html")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# Remove the duplicated script before {% endblock %} of content block
bad_script = """<script src="https://cdn.jsdelivr.net/npm/flatpickr"></script>
<script src="https://npmcdn.com/flatpickr/dist/l10n/es.js"></script>
<script>
    flatpickr("#date-picker", {
        locale: "es",
        minDate: "today",
        dateFormat: "Y-m-d",
        altInput: true,
        altFormat: "d/m/Y",
        disableMobile: "true",
        onChange: function(selectedDates, dateStr, instance) {
            // Trigger the change event manually so main.js picks it up
            const event = new Event('change');
            document.getElementById('date-picker').dispatchEvent(event);
        }
    });
</script>"""

# We'll just carefully replace the disableMobile: "true" with disableMobile: true
content = content.replace('disableMobile: "true",', 'disableMobile: true,')

# And remove one of the duplicates if it exists twice
content = content.replace(bad_script, "")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
