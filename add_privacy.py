import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"
base_html = os.path.join(base, "templates/base.html")

with open(base_html, "r", encoding="utf-8") as f:
    content = f.read()

modal_html = """
    <!-- Modal de Privacidad -->
    <div id="privacy-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); backdrop-filter: blur(5px); z-index: 9999; justify-content: center; align-items: center; padding: 20px;">
        <div style="background: #0a0a0a; border: 1px solid #333; border-radius: 12px; padding: 25px; max-width: 500px; width: 100%; max-height: 80vh; overflow-y: auto; color: #e5e5e5; font-family: 'Inter', sans-serif;">
            <h2 style="color: #FFCC00; margin-bottom: 20px; font-family: 'Space Grotesk', sans-serif; font-size: 1.5rem;">Políticas de Privacidad</h2>
            
            <h3 style="color: #fff; font-size: 1.1rem; margin-bottom: 10px;">1. Uso de los datos personales</h3>
            <p style="font-size: 0.9rem; color: #a1a1aa; line-height: 1.5; margin-bottom: 20px;">En este sitio recolectamos únicamente los datos estrictamente necesarios (nombre y número de teléfono) con el único fin de gestionar la reserva de tu turno y poder contactarte en caso de modificaciones en el servicio.</p>
            
            <h3 style="color: #fff; font-size: 1.1rem; margin-bottom: 10px;">2. Privacidad y seguridad</h3>
            <p style="font-size: 0.9rem; color: #a1a1aa; line-height: 1.5; margin-bottom: 20px;">Tu información personal es completamente confidencial y se almacena de forma segura. Tus datos no serán vendidos, cedidos ni compartidos con terceros bajo ninguna circunstancia. Únicamente el personal de la barbería tiene acceso a esta información para la correcta atención en el local.</p>
            
            <h3 style="color: #fff; font-size: 1.1rem; margin-bottom: 10px;">3. Uso de cookies</h3>
            <p style="font-size: 0.9rem; color: #a1a1aa; line-height: 1.5; margin-bottom: 20px;">Esta plataforma utiliza exclusivamente cookies técnicas esenciales. Estas son necesarias para garantizar el correcto funcionamiento del sistema y mantener activa tu sesión mientras gestionás tu turno. No utilizamos cookies de rastreo con fines publicitarios.</p>
            
            <button onclick="document.getElementById('privacy-modal').style.display='none'" style="width: 100%; padding: 12px; background: #FFCC00; color: #000; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; margin-top: 10px;">Entendido</button>
        </div>
    </div>
</body>"""

if "privacy-modal" not in content:
    content = content.replace("</body>", modal_html)
    with open(base_html, "w", encoding="utf-8") as f:
        f.write(content)

# Update index.html
index_html = os.path.join(base, "templates/cliente/index.html")
with open(index_html, "r", encoding="utf-8") as f:
    idx = f.read()

privacy_link = """</a><br><br><a href="#" onclick="document.getElementById('privacy-modal').style.display='flex'; return false;" style="color: #666; text-decoration: none; border-bottom: 1px solid #444; padding-bottom: 1px; transition: color 0.3s;" onmouseover="this.style.color='#FFCC00'" onmouseout="this.style.color='#666'">Políticas de Privacidad</a>"""
idx = re.sub(r'Felipe Bandeira</a>', 'Felipe Bandeira' + privacy_link, idx)
with open(index_html, "w", encoding="utf-8") as f:
    f.write(idx)

# Update mis_turnos.html
mis_turnos_html = os.path.join(base, "templates/cliente/mis_turnos.html")
with open(mis_turnos_html, "r", encoding="utf-8") as f:
    mt = f.read()

mt = re.sub(r'Felipe Bandeira</a>', 'Felipe Bandeira' + privacy_link, mt)
with open(mis_turnos_html, "w", encoding="utf-8") as f:
    f.write(mt)
