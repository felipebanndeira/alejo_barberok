import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "templates/admin/finances.html")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# The stats grid currently shows three boxes: Caja Hoy, Gastos Hoy, Ingreso Neto Hoy
# We'll change the grid to have 6 boxes, or maybe two sections: Hoy and Mes

stats_grid = """        <div class="stats-grid">
            <div class="stat-card">
                <h3>Caja Hoy</h3>
                <p class="stat-value space-font">${{ "{:,.2f}".format(caja_hoy).replace(",", ".") }}</p>
            </div>
            <div class="stat-card">
                <h3>Gastos Hoy</h3>
                <p class="stat-value space-font">${{ gastos_hoy }}</p>
            </div>
            <div class="stat-card">
                <h3>Ingreso Neto Hoy</h3>
                <p class="stat-value space-font gold-text">${{ net_profit }}</p>
            </div>
        </div>"""

new_stats_grid = """        
        <h2 style="margin-bottom: 1rem;">Estadísticas de Hoy</h2>
        <div class="stats-grid" style="margin-bottom: 2rem;">
            <div class="stat-card">
                <h3>Caja Hoy</h3>
                <p class="stat-value space-font">${{ "{:,.2f}".format(caja_hoy).replace(",", ".") }}</p>
            </div>
            <div class="stat-card">
                <h3>Gastos Hoy</h3>
                <p class="stat-value space-font">${{ gastos_hoy }}</p>
            </div>
            <div class="stat-card">
                <h3>Ingreso Neto Hoy</h3>
                <p class="stat-value space-font gold-text">${{ net_profit }}</p>
            </div>
        </div>
        
        <h2 style="margin-bottom: 1rem;">Estadísticas del Mes</h2>
        <div class="stats-grid" style="margin-bottom: 2rem;">
            <div class="stat-card" style="border-top: 3px solid #6366f1;">
                <h3>Caja del Mes</h3>
                <p class="stat-value space-font">${{ caja_mes }}</p>
            </div>
            <div class="stat-card" style="border-top: 3px solid #ef4444;">
                <h3>Gastos del Mes</h3>
                <p class="stat-value space-font">${{ gastos_mes }}</p>
            </div>
            <div class="stat-card" style="border-top: 3px solid #22c55e;">
                <h3>Neto del Mes</h3>
                <p class="stat-value space-font" style="color: #4ade80;">${{ net_mes }}</p>
            </div>
        </div>"""

content = content.replace(stats_grid, new_stats_grid)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
