import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "templates/admin/dashboard.html")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# For the desktop table
old_td = '<td class="space-font" style="font-size: 1.05rem; font-weight: 500; color: var(--primary-gold);">{{ a.time }}</td>'
new_td = '<td class="space-font" style="font-size: 1.05rem; font-weight: 500; color: var(--primary-gold);">{{ a.date.split(\'-\')[2] }}/{{ a.date.split(\'-\')[1] }} {{ a.time }}</td>'
content = content.replace(old_td, new_td)

# For the mobile cards
old_span = '<span class="appt-time">{{ a.time }}</span>'
new_span = '<span class="appt-time" style="font-size: 1.1rem;">{{ a.date.split(\'-\')[2] }}/{{ a.date.split(\'-\')[1] }} {{ a.time }}</span>'
content = content.replace(old_span, new_span)

# Also there's a heading "Agenda de Hoy" which should say "Próximos Turnos"
content = content.replace('<h3 class="space-font">Agenda de Hoy</h3>', '<h3 class="space-font">Próximos Turnos</h3>')
content = content.replace('<p class="text-dim">No hay turnos agendados para hoy.</p>', '<p class="text-dim">No hay próximos turnos agendados.</p>')

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
