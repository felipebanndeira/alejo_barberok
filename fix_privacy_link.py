import os

base = r"c:\Users\usser\Documents\Alejo barber"

def fix_link(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    content = content.replace('href="#" onclick="document.getElementById(\'privacy-modal\').style.display=\'flex\'; return false;"', 'href="javascript:void(0)" onclick="document.getElementById(\'privacy-modal\').style.display=\'flex\'"')
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

fix_link(os.path.join(base, "templates/cliente/index.html"))
fix_link(os.path.join(base, "templates/cliente/mis_turnos.html"))
