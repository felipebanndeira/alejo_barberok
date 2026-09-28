import os

base = r"c:\Users\usser\Documents\Alejo barber"
login_path = os.path.join(base, "templates/admin/login.html")
mis_turnos_path = os.path.join(base, "templates/cliente/mis_turnos.html")

with open(login_path, "r", encoding="utf-8") as f:
    login = f.read()

# Add a back button to login if it's not there
if "Volver al inicio" not in login:
    btn = '<a href="{{ url_for(\'cliente.index\') }}" class="btn-outline w-100" style="display:block; width:100%; text-align:center; margin-top: 1rem; text-decoration: none;">Volver al inicio</a>'
    login = login.replace('</form>', f'</form>\n        {btn}')
    with open(login_path, "w", encoding="utf-8") as f:
        f.write(login)

with open(mis_turnos_path, "r", encoding="utf-8") as f:
    mis_turnos = f.read()

# Add a back button to mis_turnos at the bottom
if "Volver a Nuevo Turno" not in mis_turnos:
    btn = '<div class="text-center" style="margin-top: 2rem;"><a href="{{ url_for(\'cliente.index\') }}" class="btn-outline" style="display:inline-block; text-decoration: none;"><i data-lucide="arrow-left" style="width:16px; margin-right:5px; vertical-align:middle;"></i> Volver a Nuevo Turno</a></div>'
    mis_turnos = mis_turnos.replace('<!-- Developer Footer -->', f'{btn}\n\n<!-- Developer Footer -->')
    # Fix encoding
    mis_turnos = mis_turnos.replace("ConsultA tus turnos", "Consultá tus turnos")
    mis_turnos = mis_turnos.replace("text-cenAmero de celular.", "text-center mb-2\">Ingresa tu número de celular ")
    mis_turnos = mis_turnos.replace("NAmero", "Número")
    with open(mis_turnos_path, "w", encoding="utf-8") as f:
        f.write(mis_turnos)

