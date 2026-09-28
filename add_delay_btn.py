import os

base = r"c:\Users\usser\Documents\Alejo barber"
dash_path = os.path.join(base, "templates/admin/dashboard.html")

with open(dash_path, "r", encoding="utf-8") as f:
    dash = f.read()

# Desktop injection
desktop_target = """<a href="https://wa.me/{{a.client_phone|replace('+', '')}}?text=Hola {{a.client_name}}, te recuerdo tu turno de hoy a las {{a.time}} para el servicio de {{a.service_name}}." target="_blank" class="btn-icon" title="Enviar Recordatorio">
                                <i data-lucide="message-circle"></i>
                            </a>"""

desktop_delay_btn = """<a href="https://wa.me/{{a.client_phone|replace('+', '')}}?text=Hola {{a.client_name}}, estoy con una pequeña demora. ¿Podrías venir unos 15 minutitos más tarde de tu turno de las {{a.time}}? ¡Gracias y disculpá!" target="_blank" class="btn-icon" title="Avisar Demora 15m" style="color: #ffc107;">
                                <i data-lucide="clock"></i>
                            </a>"""

if desktop_target in dash:
    dash = dash.replace(desktop_target, desktop_delay_btn + "\n                            " + desktop_target)
else:
    print("Desktop target not found")


# Mobile injection
mobile_target = """<a href="https://wa.me/{{a.client_phone|replace('+', '')}}?text=Hola {{a.client_name}}, te recuerdo tu turno de hoy a las {{a.time}} para el servicio de {{a.service_name}}." target="_blank" class="btn-outline" style="flex:1; text-align:center; padding:0.8rem; border-color:rgba(255,204,0,0.3); color:var(--primary-gold); background:rgba(255,204,0,0.05);">
                                <i data-lucide="message-circle" style="width:20px; display:inline-block; vertical-align:middle;"></i>
                            </a>"""

mobile_delay_btn = """<a href="https://wa.me/{{a.client_phone|replace('+', '')}}?text=Hola {{a.client_name}}, estoy con una pequeña demora. ¿Podrías venir unos 15 minutitos más tarde de tu turno de las {{a.time}}? ¡Gracias y disculpá!" target="_blank" class="btn-outline" style="flex:1; text-align:center; padding:0.8rem; border-color:rgba(255,193,7,0.3); color:#ffc107; background:rgba(255,193,7,0.05);" title="Avisar Demora 15m">
                                <i data-lucide="clock" style="width:20px; display:inline-block; vertical-align:middle;"></i>
                            </a>"""

if mobile_target in dash:
    dash = dash.replace(mobile_target, mobile_delay_btn + "\n                            " + mobile_target)
else:
    print("Mobile target not found")

with open(dash_path, "w", encoding="utf-8") as f:
    f.write(dash)
    
print("Added Delay buttons")

