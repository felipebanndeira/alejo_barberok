import os

base = r"c:\Users\usser\Documents\Alejo barber"
finances = os.path.join(base, "templates/admin/finances.html")
dash = os.path.join(base, "templates/admin/dashboard.html")

# Modify finances
with open(finances, "r", encoding="utf-8") as f:
    fc = f.read()

fc = fc.replace("<h3>Caja Hoy</h3>", "<h3>Caja Actual</h3>")
fc = fc.replace("<h3>Gastos Hoy</h3>", "<h3>Gastos Actuales</h3>")
fc = fc.replace("<h3>Ingreso Neto Hoy</h3>", "<h3>Ingreso Neto</h3>")
fc = fc.replace("Estadísticas de Hoy", "Estadísticas Actuales")

# Add the reset button to finances
btn_html = """
        <div class="flex-between" style="margin-bottom: 1rem;">
            <h2>Estadísticas Actuales</h2>
            <form method="POST" action="/admin/reset_caja" onsubmit="return confirm('¿Seguro que querés Reiniciar la Caja a $0? Esto no borrará el historial mensual.');" style="margin:0;">
                <button type="submit" class="btn-gold" style="padding: 0.5rem 1rem; font-size: 0.9rem; background: #ef4444; border-color: #ef4444; color: white;">
                    <i data-lucide="refresh-cw" style="width:16px; margin-right:5px; vertical-align:text-bottom;"></i> Reiniciar Caja
                </button>
            </form>
        </div>
"""
fc = fc.replace('<h2 style="margin-bottom: 1rem;">Estadísticas Actuales</h2>', btn_html)

with open(finances, "w", encoding="utf-8") as f:
    f.write(fc)

# Modify dash
with open(dash, "r", encoding="utf-8") as f:
    dc = f.read()

dc = dc.replace("<h3>Caja Hoy</h3>", "<h3>Caja Actual</h3>")
dc = dc.replace("<h3>Gastos Hoy</h3>", "<h3>Gastos Actuales</h3>")
dc = dc.replace("<h3>Ingreso Neto Hoy</h3>", "<h3>Ingreso Neto</h3>")

# Add the reset button to dash top
dash_btn_html = """
        <div class="flex-between mb-2">
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
        </form>
"""
dc = dc.replace('<h2 class="space-font mb-2">Resumen Financiero</h2>', dash_btn_html)

with open(dash, "w", encoding="utf-8") as f:
    f.write(dc)
