import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "templates/admin/finances.html")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# We completely overwrite everything between <h2 class="mb-2 space-font">Caja y Estadísticas</h2> and <div class="mt-2 flex-between mb-2">
new_html = """        <div class="flex-between mb-2">
            <h2 class="space-font">Caja y Estadísticas</h2>
            <form method="POST" action="/admin/toggle_shift" style="margin:0;">
                {% if shift_active %}
                <button type="submit" class="btn-gold" style="padding: 0.5rem 1rem; font-size: 0.9rem; background: #ef4444; border-color: #ef4444; color: white;" onclick="return confirm('¿Cerrar la Jornada Actual? La caja volverá a $0 visualmente.');">
                    <i data-lucide="power" style="width:16px; margin-right:5px; vertical-align:text-bottom;"></i> Cerrar Jornada
                </button>
                {% else %}
                <button type="submit" class="btn-gold" style="padding: 0.5rem 1rem; font-size: 0.9rem;">
                    <i data-lucide="play" style="width:16px; margin-right:5px; vertical-align:text-bottom;"></i> Iniciar Jornada
                </button>
                {% endif %}
            </form>
        </div>
        
        <div class="stats-grid mb-2">
            <div class="glass-panel stat-card" style="display: flex; justify-content: space-between; border-top: 3px solid var(--primary-gold);">
                <div>
                    <p class="text-dim">Caja de Hoy (Manual)</p>
                    <h3 class="space-font" style="font-weight: 700;">${{ caja_hoy }}</h3>
                    <div style="font-size: 0.8rem; color: #a1a1aa; margin-top: 5px;">
                        Efectivo: <span style="color:#4ade80;">${{ "{:,.2f}".format(caja_efectivo).replace(",", ".") }}</span> | Transf: <span style="color:#60a5fa;">${{ "{:,.2f}".format(caja_transferencia).replace(",", ".") }}</span>
                    </div>
                </div>
                <button onclick="document.getElementById('modal-gasto').style.display='flex'" class="btn-outline" style="font-size:0.8rem; border:1px solid #333; border-radius:4px; padding:0.4rem 0.6rem; height: fit-content;">+ Cargar Gasto</button>
            </div>
            <div class="glass-panel stat-card">
                <p class="text-dim">Ganancia Neta (Manual)</p>
                <h3 class="space-font" style="font-weight: 700; color: var(--primary-gold);">${{ net_profit }}</h3>
            </div>
            <div class="glass-panel stat-card" style="border-top: 3px solid #6366f1;">
                <p class="text-dim">Caja Mensual (Automática)</p>
                <h3 class="space-font" style="font-weight: 700; color: #fff;">${{ caja_mes }}</h3>
            </div>
        </div>

        <div class="glass-panel mb-2" style="padding: 1.5rem;">
            <h3 class="space-font mb-2" style="font-size: 1.1rem;">Ingresos Últimos 7 días</h3>
            <div style="position: relative; height: 250px; width: 100%;"><canvas id="incomeChart"></canvas></div>
        </div>"""

content = re.sub(r'<h2 class="mb-2 space-font">Caja y Estad[íA]sticas</h2>.*?(?=<div class="mt-2 flex-between mb-2">)', new_html + "\n\n        ", content, flags=re.DOTALL)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
