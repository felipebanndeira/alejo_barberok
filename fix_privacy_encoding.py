import os

base = r"c:\Users\usser\Documents\Alejo barber"

def fix_encoding(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    content = content.replace("PolAticas", "Políticas")
    content = content.replace("tAccnicas", "técnicas")
    content = content.replace("sesiA3n", "sesión")
    content = content.replace("gestionA\u00b4s", "gestionás")
    content = content.replace("gestionAs", "gestionás")
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

fix_encoding(os.path.join(base, "templates/base.html"))
fix_encoding(os.path.join(base, "templates/cliente/index.html"))
fix_encoding(os.path.join(base, "templates/cliente/mis_turnos.html"))
