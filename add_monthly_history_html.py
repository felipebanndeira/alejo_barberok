import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "templates/admin/finances.html")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

history_html = """
        <h2 style="margin-top: 3rem; margin-bottom: 1rem;">Historial Mes a Mes</h2>
        <div class="card" style="margin-bottom: 2rem;">
            <table class="table">
                <thead>
                    <tr>
                        <th>Mes</th>
                        <th>Caja Total</th>
                        <th>Gastos</th>
                        <th>Ganancia Neta</th>
                    </tr>
                </thead>
                <tbody>
                    {% for h in monthly_history %}
                    <tr>
                        <td style="font-weight: bold; color: #fff;">{{ h.month }}</td>
                        <td class="gold-text space-font">${{ h.caja }}</td>
                        <td class="space-font" style="color: #ef4444;">${{ h.gastos }}</td>
                        <td class="space-font" style="color: #4ade80;">${{ h.neto }}</td>
                    </tr>
                    {% endfor %}
                    {% if not monthly_history %}
                    <tr>
                        <td colspan="4" class="text-center text-dim">No hay historial registrado aún.</td>
                    </tr>
                    {% endif %}
                </tbody>
            </table>
        </div>
"""

# Insert it before the Grafico de Ingresos section
content = content.replace('<h2 style="margin-bottom: 1rem;">Gráfico de Ingresos (Últimos 7 días)</h2>', history_html + '\n        <h2 style="margin-bottom: 1rem;">Gráfico de Ingresos (Últimos 7 días)</h2>')

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
