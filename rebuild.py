import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"
finances_path = os.path.join(base, "templates/admin/finances.html")
dash_path = os.path.join(base, "templates/admin/dashboard.html")

with open(finances_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove stats grid
content = re.sub(r'<div class="stats-grid">.*?</div>\s*<div class="glass-panel mb-2"', '<div class="glass-panel mb-2"', content, flags=re.DOTALL)

# 2. Remove chart
content = re.sub(r'<div class="glass-panel mb-2".*?<canvas id="incomeChart".*?</canvas>\s*</div>', '', content, flags=re.DOTALL)

# 3. Remove sales form & table
content = re.sub(r'<div class="mt-2 flex-between mb-2">\s*<h3 class="space-font">Venta de Mostrador rApida</h3>.*?</div>\s*</div>', '</div>\n</div>', content, flags=re.DOTALL)
# (Since the encoding might vary, let's use a safer regex)
content = re.sub(r'<div class="mt-2 flex-between mb-2">.*?<!-- Modal Turno Manual -->', '<!-- Modal Turno Manual -->', content, flags=re.DOTALL)

# But wait, we NEED the Agenda inside dashboard.html. finances.html doesn't have the Agenda!
