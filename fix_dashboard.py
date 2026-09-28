import os

base = r"c:\Users\usser\Documents\Alejo barber"
dash_path = os.path.join(base, "templates/admin/dashboard.html")
finances_path = os.path.join(base, "templates/admin/finances.html")

with open(finances_path, "r", encoding="utf-8") as f:
    fin = f.read()

# Extract modals and scripts from finances
modals_part = "<!-- Modal Turno Manual -->" + fin.split("<!-- Modal Turno Manual -->")[1]

# But we don't need the chart logic in dashboard.html.
# So I will strip the chart logic from it.
import re
modals_part = re.sub(r'// Chart Logic.*?\}\);', '', modals_part, flags=re.DOTALL)

with open(dash_path, "r", encoding="utf-8") as f:
    dash = f.read()

# dashboard currently ends at </div>\n</div>
# but wait, the output of Get-Content showed the Sales table was STILL in dashboard.html!
# "No hay ventas registradas hoy."
# Let's clean up dashboard.html fully.

# The correct dashboard body should be:
# {% extends 'base.html' %} ... sidebar ... <div class="admin-content">
# <h2 class="mb-2 space-font">Agenda</h2>
# <div class="flex-between mb-2"> ... Agenda header & buttons ... </div>
# <div class="table-container desktop-only"> ... Table ... </div>
# <div class="mobile-only mb-2"> ... Mobile Cards ... </div>
# </div></div>
# Modals + endblock

# Let's extract the Agenda part from the current dashboard.html
agenda_start = dash.find('<div class="flex-between mb-2">\n            <h3 class="space-font">Agenda de Hoy</h3>')
if agenda_start == -1:
    agenda_start = dash.find('<div class="flex-between mb-2">')

agenda_end = dash.find('<!-- MOBILE CARDS VIEW -->')
if agenda_end != -1:
    # Find the end of the mobile cards view
    agenda_end_idx = dash.find('</div>\n        <div class="mt-2 flex-between mb-2">', agenda_end)
    if agenda_end_idx == -1:
        # If it doesn't have the Venta Rápida div after it, just find the last </div> before the Sales table
        # Let's just find where Venta Rápida starts
        venta_start = dash.find('<div class="mt-2 flex-between mb-2">')
        if venta_start != -1:
            dash_content = dash[:venta_start] + "    </div>\n</div>\n\n" + modals_part
        else:
            # If Sales is not found, just append modals_part
            dash_content = dash + "\n" + modals_part
else:
    # Just grab everything before Venta Rápida
    venta_start = dash.find('<div class="mt-2 flex-between mb-2">')
    if venta_start != -1:
        dash_content = dash[:venta_start] + "    </div>\n</div>\n\n" + modals_part
    else:
        dash_content = dash + "\n" + modals_part
        
# Fix the "Panel de Control" to "Agenda"
dash_content = dash_content.replace('<h2 class="mb-2 space-font">Panel de Control</h2>', '<h2 class="mb-2 space-font">Agenda</h2>')
# Fix <title>
dash_content = dash_content.replace('Dashboard - Admin', 'Agenda - Admin')

with open(dash_path, "w", encoding="utf-8") as f:
    f.write(dash_content)

