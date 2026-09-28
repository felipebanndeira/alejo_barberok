import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "templates/admin/finances.html")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_html = """        <div class="flex-between mb-2">
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
        </div>"""

new_html = """        <div class="flex-between mb-2">
            <h2 class="space-font">Caja y Estadísticas</h2>
            <form method="POST" action="/admin/reset_caja" onsubmit="return confirm('¿Seguro que querés Reiniciar la Caja Actual a $0?');" style="margin:0;">
                <button type="submit" class="btn-gold" style="padding: 0.5rem 1rem; font-size: 0.9rem; background: #ef4444; border-color: #ef4444; color: white;">
                    <i data-lucide="refresh-cw" style="width:16px; margin-right:5px; vertical-align:text-bottom;"></i> Reiniciar Caja
                </button>
            </form>
        </div>"""

content = content.replace(old_html, new_html)
with open(path, "w", encoding="utf-8") as f:
    f.write(content)
