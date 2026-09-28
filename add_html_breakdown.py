import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "templates/admin/finances.html")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Modify the Caja Hoy card
search = """            <div class="stat-card">
                <h3>Caja Hoy</h3>
                <p class="stat-value space-font">${{ "{:,.2f}".format(caja_hoy).replace(",", ".") }}</p>
            </div>"""

replace = """            <div class="stat-card">
                <h3>Caja Hoy</h3>
                <p class="stat-value space-font">${{ "{:,.2f}".format(caja_hoy).replace(",", ".") }}</p>
                <div style="font-size: 0.8rem; color: #a1a1aa; margin-top: 5px;">
                    Efectivo: <span style="color:#4ade80;">${{ "{:,.2f}".format(caja_efectivo).replace(",", ".") }}</span> | Transf: <span style="color:#60a5fa;">${{ "{:,.2f}".format(caja_transferencia).replace(",", ".") }}</span>
                </div>
            </div>"""

content = content.replace(search, replace)
with open(path, "w", encoding="utf-8") as f:
    f.write(content)
