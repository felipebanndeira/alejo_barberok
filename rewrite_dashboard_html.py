import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "templates/admin/dashboard.html")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

new_html = """        <div class="flex-between mb-2">
            <h2 class="space-font">Resumen Financiero</h2>
            <form method="POST" action="/admin/toggle_shift" style="margin:0;">
                {% if shift_active %}
                <button type="submit" class="btn-gold d-none-mobile" style="padding: 0.5rem 1rem; font-size: 0.9rem; background: #ef4444; border-color: #ef4444; color: white;" onclick="return confirm('¿Cerrar la Jornada Actual? La caja volverá a $0 visualmente.');">
                    <i data-lucide="power" style="width:16px; margin-right:5px; vertical-align:text-bottom;"></i> Cerrar Jornada
                </button>
                {% else %}
                <button type="submit" class="btn-gold d-none-mobile" style="padding: 0.5rem 1rem; font-size: 0.9rem;">
                    <i data-lucide="play" style="width:16px; margin-right:5px; vertical-align:text-bottom;"></i> Iniciar Jornada
                </button>
                {% endif %}
            </form>
        </div>
        <form method="POST" action="/admin/toggle_shift" class="d-none-desktop mb-2">
            {% if shift_active %}
            <button type="submit" class="btn-gold w-full" style="padding: 1rem; font-size: 1rem; background: #ef4444; border-color: #ef4444; color: white;" onclick="return confirm('¿Cerrar la Jornada Actual?');">
                <i data-lucide="power" style="width:18px; margin-right:5px; vertical-align:text-bottom;"></i> Cerrar Jornada
            </button>
            {% else %}
            <button type="submit" class="btn-gold w-full" style="padding: 1rem; font-size: 1rem;">
                <i data-lucide="play" style="width:18px; margin-right:5px; vertical-align:text-bottom;"></i> Iniciar Jornada
            </button>
            {% endif %}
        </form>

        <div class="stats-grid mb-2">
            <div class="glass-panel stat-card" style="border-top: 3px solid var(--primary-gold);">
                <p class="text-dim">Caja de Hoy (Manual)</p>
                <h3 class="space-font" style="font-weight: 700;">${{ caja_hoy }}</h3>
            </div>
            <div class="glass-panel stat-card">
                <p class="text-dim">Ganancia Neta</p>
                <h3 class="space-font" style="font-weight: 700; color: var(--primary-gold);">${{ net_profit }}</h3>
            </div>
            <div class="glass-panel stat-card">
                <p class="text-dim">Turnos Hoy</p>
                <h3 class="space-font" style="font-weight: 700;">{{ appointments_today }}</h3>
            </div>
        </div>"""

content = re.sub(r'<h2 class="space-font mb-2">Resumen Financiero</h2>.*?(?=<div class="flex-between mb-2" style="margin-top: 2rem;">|<div class="flex-between mb-2">)', new_html + "\n\n        ", content, flags=re.DOTALL)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
