import os

base = r"c:\Users\usser\Documents\Alejo barber"

for template in ["index.html", "mis_turnos.html"]:
    path = os.path.join(base, "templates/cliente", template)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace the replacement character  with the correct ones
    content = content.replace("Consult", "Consultá")
    content = content.replace("Ingres", "Ingresá")
    content = content.replace("nmero", "número")
    content = content.replace("Atrs", "Atrás")
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

