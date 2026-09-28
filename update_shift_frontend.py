import os

base = r"c:\Users\usser\Documents\Alejo barber"
fin = os.path.join(base, "templates/admin/finances.html")
dash = os.path.join(base, "templates/admin/dashboard.html")

with open(fin, "r", encoding="utf-8") as f:
    fc = f.read()

# Replace the old form with the new dynamic button
old_btn = """        <div class="flex-between" style="margin-bottom: 1rem;">
            <h2>Estadísticas Actuales</h2>
            <form method="POST" action="/admin/reset_caja" onsubmit="return confirm('¿Seguro que querés Reiniciar la Caja a $0? Esto no borrará el historial mensual.');" style="margin:0;">
                <button type="submit" class="btn-gold" style="padding: 0.5rem 1rem; font-size: 0.9rem; background: #ef4444; border-color: #ef4444; color: white;">
                    <i data-lucide="refresh-cw" style="width:16px; margin-right:5px; vertical-align:text-bottom;"></i> Reiniciar Caja
                </button>
            </form>
        </div>"""

new_btn = """        <div class="flex-between" style="margin-bottom: 1rem;">
            <h2>Estadísticas Actuales</h2>
            <form method="POST" action="/admin/toggle_shift" style="margin:0;">
                {% if shift_active %}
                <button type="submit" class="btn-gold" style="padding: 0.5rem 1rem; font-size: 0.9rem; background: #ef4444; border-color: #ef4444; color: white;" onclick="return confirm('¿Seguro que querés Cerrar la Jornada? Los contadores volverán a $0.');">
                    <i data-lucide="power" style="width:16px; margin-right:5px; vertical-align:text-bottom;"></i> Cerrar Jornada
                </button>
                {% else %}
                <button type="submit" class="btn-gold" style="padding: 0.5rem 1rem; font-size: 0.9rem;">
                    <i data-lucide="play" style="width:16px; margin-right:5px; vertical-align:text-bottom;"></i> Iniciar Jornada
                </button>
                {% endif %}
            </form>
        </div>"""

fc = fc.replace(old_btn, new_btn)
with open(fin, "w", encoding="utf-8") as f:
    f.write(fc)

# Now dashboard
with open(dash, "r", encoding="utf-8") as f:
    dc = f.read()

old_dash_btn = """        <div class="flex-between mb-2">
            <h2 class="space-font">Resumen Financiero</h2>
            <form method="POST" action="/admin/reset_caja" onsubmit="return confirm('¿Seguro que querés Reiniciar la Caja a $0?');" style="margin:0;">
                <button type="submit" class="btn-gold d-none-mobile" style="padding: 0.5rem 1rem; font-size: 0.9rem; background: #ef4444; border-color: #ef4444; color: white;">
                    <i data-lucide="refresh-cw" style="width:16px; margin-right:5px; vertical-align:text-bottom;"></i> Reiniciar Caja
                </button>
            </form>
        </div>
        <form method="POST" action="/admin/reset_caja" onsubmit="return confirm('¿Seguro que querés Reiniciar la Caja a $0?');" class="d-none-desktop mb-2">
            <button type="submit" class="btn-gold w-full" style="padding: 1rem; font-size: 1rem; background: #ef4444; border-color: #ef4444; color: white;">
                <i data-lucide="refresh-cw" style="width:18px; margin-right:5px; vertical-align:text-bottom;"></i> Reiniciar Caja
            </button>
        </form>"""

new_dash_btn = """        <div class="flex-between mb-2">
            <h2 class="space-font">Resumen Financiero</h2>
            <form method="POST" action="/admin/toggle_shift" style="margin:0;">
                {% if shift_active %}
                <button type="submit" class="btn-gold d-none-mobile" style="padding: 0.5rem 1rem; font-size: 0.9rem; background: #ef4444; border-color: #ef4444; color: white;" onclick="return confirm('¿Seguro que querés Cerrar la Jornada? Los contadores volverán a $0.');">
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
            <button type="submit" class="btn-gold w-full" style="padding: 1rem; font-size: 1rem; background: #ef4444; border-color: #ef4444; color: white;" onclick="return confirm('¿Seguro que querés Cerrar la Jornada?');">
                <i data-lucide="power" style="width:18px; margin-right:5px; vertical-align:text-bottom;"></i> Cerrar Jornada
            </button>
            {% else %}
            <button type="submit" class="btn-gold w-full" style="padding: 1rem; font-size: 1rem;">
                <i data-lucide="play" style="width:18px; margin-right:5px; vertical-align:text-bottom;"></i> Iniciar Jornada
            </button>
            {% endif %}
        </form>"""

dc = dc.replace(old_dash_btn, new_dash_btn)
with open(dash, "w", encoding="utf-8") as f:
    f.write(dc)
