import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"

# Add footer to index.html
index_path = os.path.join(base, "templates/cliente/index.html")
with open(index_path, "r", encoding="utf-8") as f:
    index = f.read()

footer_html = """
<!-- Developer Footer -->
<div style="text-align: center; margin-top: 4rem; padding-bottom: 8rem;">
    <p style="color: #444; font-size: 0.8rem; font-family: 'Inter', sans-serif;">
        Desarrollado por <a href="#" style="color: #666; text-decoration: none; border-bottom: 1px solid #444; padding-bottom: 1px;">[Tu Nombre / Agencia]</a>
    </p>
</div>
"""
if "Desarrollado por" not in index:
    index = index.replace('<!-- Sticky Footer -->', footer_html + '\n<!-- Sticky Footer -->')
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index)


# Add footer to mis_turnos.html
mis_turnos_path = os.path.join(base, "templates/cliente/mis_turnos.html")
with open(mis_turnos_path, "r", encoding="utf-8") as f:
    mis = f.read()

footer_html_mis = """
<!-- Developer Footer -->
<div style="text-align: center; margin-top: 4rem; padding-bottom: 2rem;">
    <p style="color: #444; font-size: 0.8rem; font-family: 'Inter', sans-serif;">
        Desarrollado por <a href="#" style="color: #666; text-decoration: none; border-bottom: 1px solid #444; padding-bottom: 1px;">[Tu Nombre / Agencia]</a>
    </p>
</div>
"""
if "Desarrollado por" not in mis:
    mis = mis.replace('{% endblock %}', footer_html_mis + '\n{% endblock %}')
    with open(mis_turnos_path, "w", encoding="utf-8") as f:
        f.write(mis)

