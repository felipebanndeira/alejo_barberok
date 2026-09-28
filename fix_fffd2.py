import os

base = r"c:\Users\usser\Documents\Alejo barber"

for template in ["index.html", "mis_turnos.html"]:
    path = os.path.join(base, "templates/cliente", template)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Brute force string replacement using slicing or exact string that I can see from terminal output
    # 'ConsultA tus turnos'
    content = content.replace("ConsultA\ufffd tus turnos", "Consultá tus turnos")
    content = content.replace("IngresA\ufffd tu", "Ingresá tu")
    content = content.replace("nA\ufffdmero", "número")
    content = content.replace("A\ufffdQuA\ufffd", "¿Qué")
    content = content.replace("necesitA\ufffds", "necesitás")
    content = content.replace("A\ufffdCuA\ufffdndo", "¿Cuándo")
    content = content.replace("querA\ufffds", "querés")
    content = content.replace("TelA\ufffdfono", "Teléfono")
    content = content.replace("A\ufffdTurno Confirmado!", "¡Turno Confirmado!")
    content = content.replace("conexiA\ufffdn", "conexión")
    content = content.replace("AtrA\ufffds", "Atrás")
    content = content.replace("APreferA\ufffds agendar por mensaje o tenA\ufffds dudas", "¿Preferís agendar por mensaje o tenés dudas")
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# And main.js
js_path = os.path.join(base, "static/js/main.js")
with open(js_path, "r", encoding="utf-8") as f:
    js = f.read()
    
js = js.replace("A\ufffdTurno Confirmado!", "¡Turno Confirmado!")
js = js.replace("conexiA\ufffdn", "conexión")
js = js.replace("AtrA\ufffds", "Atrás")

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js)
