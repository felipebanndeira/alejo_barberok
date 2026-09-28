import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"
dash_path = os.path.join(base, "templates/admin/dashboard.html")
finances_path = os.path.join(base, "templates/admin/finances.html")

with open(dash_path, "r", encoding="utf-8") as f:
    dash = f.read()

# Let's completely clean up dashboard.html
# It should contain:
# {% extends 'base.html' %}
# {% block title %}...{% endblock %}
# {% block content %}
# <div class="admin-layout"> ... sidebar ... <div class="admin-content">
# <h2>Agenda</h2>
# <div class="flex-between mb-2"> ... Agenda buttons ... </div>
# <div class="table-container desktop-only"> ... Table ... </div>
# <div class="mobile-only mb-2"> ... Mobile Cards ... </div>
# </div></div>
# {% endblock %}
# {% block scripts %} ... Modals ... {% endblock %}

# Wait, the modals are in `finances.html` under `{% block scripts %}` or just floating?
with open(finances_path, "r", encoding="utf-8") as f:
    fin = f.read()

# Modals start with <!-- Modal Turno Manual --> and go to {% endblock %}
modals_and_end = "<!-- Modal Turno Manual -->" + fin.split("<!-- Modal Turno Manual -->")[1]

# In dashboard.html, let's chop off everything from <div class="stats-grid"> up to <div class="flex-between mb-2">\n            <h3 class="space-font">Agenda de Hoy</h3>
dash = re.sub(r'<div class="stats-grid">.*?<div class="flex-between mb-2">\s*<h3 class="space-font">Agenda de Hoy</h3>', '<div class="flex-between mb-2">\n            <h3 class="space-font">Agenda de Hoy</h3>', dash, flags=re.DOTALL)

# Chop off everything after <!-- MOBILE CARDS VIEW --> 's closing div
mobile_cards_end = dash.find('<!-- MOBILE CARDS VIEW -->')
# We need to find the </div> that closes .mobile-only
# In the previous python script, we appended it.
# Let's find "No hay ventas registradas hoy." and remove the whole sales block.
dash = re.sub(r'<div class="mt-2 flex-between mb-2">\s*<h3 class="space-font">Venta de Mostrador.*?</div>\s*</div>', '</div>\n</div>', dash, flags=re.DOTALL)

# Find the end of the admin-content div, which should be two </div></div>
dash = dash.split('<!-- Modal Turno Manual -->')[0]
# Append the modals and script block
dash = dash + "\n" + modals_and_end

# Also remove the chart script from the appended modals
dash = re.sub(r'// Chart Logic.*?\}\);', '', dash, flags=re.DOTALL)
dash = dash.replace('Panel de Control', 'Agenda')

with open(dash_path, "w", encoding="utf-8") as f:
    f.write(dash)

