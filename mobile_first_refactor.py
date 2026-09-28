import os

base = r"c:\Users\usser\Documents\Alejo barber"

# 1. Update style.css with the exact responsive classes needed
css_path = os.path.join(base, "static/css/style.css")
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

responsive_tail = """
/* ==========================================================================
   MOBILE FIRST RESPONSIVE (Tailwind logic)
   ========================================================================== */
.desktop-only { display: block; }
.mobile-only { display: none; }
.d-none-mobile { display: inline-block; }
.d-none-desktop { display: none; }
.w-full { width: 100%; }

@media (max-width: 768px) {
    .desktop-only { display: none !important; }
    .mobile-only { display: block !important; }
    .d-none-mobile { display: none !important; }
    .d-none-desktop { display: inline-block !important; }
    
    /* 1. Layout Principal y Navegacion (Bottom Bar) */
    .admin-layout {
        flex-direction: column;
    }
    .sidebar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 65px;
        background: rgba(10, 10, 10, 0.95);
        backdrop-filter: blur(10px);
        border-top: 1px solid #222;
        border-right: none;
        padding: 0;
        z-index: 9999;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .sidebar-logo { display: none; }
    .sidebar ul {
        width: 100%;
        display: flex;
        justify-content: space-evenly;
        align-items: center;
        padding: 0; margin: 0;
    }
    .sidebar ul li { list-style: none; }
    .sidebar ul li a {
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        padding: 0.5rem; font-size: 0.85rem; font-weight: 600;
        background: transparent !important; border-radius: 0; color: var(--text-dim); border: none !important;
    }
    .sidebar ul li a.active {
        color: var(--primary-gold) !important; background: transparent !important; border-bottom: 2px solid var(--primary-gold) !important;
    }
    .sidebar-separator { display: none; }
    .admin-content { padding: 1rem; padding-bottom: 80px; }
    
    /* 2. Tarjetas Resumen (Stack vertical w-full) */
    .stats-grid {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
    .stats-grid .glass-panel { width: 100%; padding: 1.25rem; }
    
    /* 3. Grafico Ingresos */
    .glass-panel:has(#incomeChart) { width: 100%; overflow: hidden; }
    canvas#incomeChart { width: 100% !important; max-height: 150px; }
    
    /* 5. Venta Rapida (Stack inputs vertical) */
    form[action*="sales/add"] {
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 0.8rem !important;
    }
    form[action*="sales/add"] > div { flex: none !important; width: 100% !important; }
    form[action*="sales/add"] button { width: 100% !important; margin-top: 0.5rem !important; }
    
    /* Modales */
    .glass-panel { max-width: 100% !important; }
}
"""
if "MOBILE FIRST RESPONSIVE" not in css:
    with open(css_path, "a", encoding="utf-8") as f:
        f.write(responsive_tail)


# 2. Update dashboard.html to add the Card view and swap classes
dash_path = os.path.join(base, "templates/admin/dashboard.html")
with open(dash_path, "r", encoding="utf-8") as f:
    dash = f.read()

# Replace the "Agenda de Hoy" header to include the responsive buttons
old_agenda_header = """<div class="flex-between mb-2">
            <h3 class="space-font">Agenda de Hoy</h3>
            <button onclick="document.getElementById('modal-turno').style.display='flex'" class="btn-gold" style="padding: 0.5rem 1rem; font-size: 0.9rem;"><i data-lucide="plus" style="width:16px; margin-right:5px; vertical-align:text-bottom;"></i> Agendar Manual</button>
        </div>"""
new_agenda_header = """<div class="flex-between mb-2">
            <h3 class="space-font">Agenda de Hoy</h3>
            <button onclick="document.getElementById('modal-turno').style.display='flex'" class="btn-gold d-none-mobile" style="padding: 0.5rem 1rem; font-size: 0.9rem;"><i data-lucide="plus" style="width:16px; margin-right:5px; vertical-align:text-bottom;"></i> Agendar Manual</button>
        </div>
        <button onclick="document.getElementById('modal-turno').style.display='flex'" class="btn-gold d-none-desktop w-full mb-2" style="padding: 1rem; font-size: 1rem;"><i data-lucide="plus" style="width:18px; margin-right:5px; vertical-align:text-bottom;"></i> Agendar Manual</button>"""
dash = dash.replace(old_agenda_header, new_agenda_header)

# Hide table on mobile
dash = dash.replace('<div class="table-container">', '<div class="table-container desktop-only">', 1)

# Generate Mobile Cards
mobile_cards = """
        <!-- MOBILE CARDS VIEW -->
        <div class="mobile-only mb-2">
            {% if schedule %}
                <div style="display: flex; flex-direction: column; gap: 1rem;">
                {% for a in schedule %}
                    <div class="glass-panel" style="padding: 1rem; border-color: {% if a.status == 'cancelled' %}#dc3545{% elif a.status == 'confirmed' %}var(--primary-gold){% else %}#222{% endif %};">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                            <div class="space-font gold-text" style="font-size: 1.3rem; font-weight: 700;">{{ a.time }}</div>
                            <div style="text-align: right;">
                                <div style="font-weight: 600; font-size: 1.1rem; color: var(--text-light);" onclick="openClientModal('{{ a.client_phone }}', '{{ a.client_name }}')">{{ a.client_name }}</div>
                                <div class="text-dim" style="font-size: 0.9rem;">{{ a.client_phone }}</div>
                            </div>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding-bottom: 0.8rem; border-bottom: 1px solid rgba(255,255,255,0.05);">
                            <div class="text-dim" style="font-size: 1.05rem;">{{ a.service_name }}</div>
                            <span class="badge {{ a.status }}" style="margin:0;">
                                {% if a.status == 'pending' %}Pendiente{% endif %}
                                {% if a.status == 'confirmed' %}Confirmado{% endif %}
                                {% if a.status == 'cancelled' %}Cancelado{% endif %}
                            </span>
                        </div>
                        <div style="display: flex; justify-content: space-between; gap: 0.5rem;">
                            {% if a.status == 'pending' %}
                            <form method="POST" action="{{ url_for('admin.update_status', id=a.id) }}" style="margin:0; flex:1;">
                                <input type="hidden" name="status" value="confirmed">
                                <button type="submit" class="btn-outline" style="width:100%; border-color:rgba(40,167,69,0.3); color:#28a745; padding:0.8rem; background:rgba(40,167,69,0.05);"><i data-lucide="check" style="width:20px;"></i></button>
                            </form>
                            {% endif %}
                            
                            <a href="https://wa.me/{{a.client_phone|replace('+', '')}}?text=Hola {{a.client_name}}, te recuerdo tu turno de hoy a las {{a.time}} para el servicio de {{a.service_name}}. ATe espero!" target="_blank" class="btn-outline" style="flex:1; text-align:center; padding:0.8rem; border-color:rgba(255,204,0,0.3); color:var(--primary-gold); background:rgba(255,204,0,0.05);">
                                <i data-lucide="message-circle" style="width:20px; display:inline-block; vertical-align:middle;"></i>
                            </a>
                            
                            <form method="POST" action="{{ url_for('admin.update_status', id=a.id) }}" style="margin:0; flex:1;">
                                <input type="hidden" name="status" value="cancelled">
                                <button type="submit" class="btn-outline delete" style="width:100%; padding:0.8rem; border-color:rgba(220,53,69,0.3); color:#dc3545; background:rgba(220,53,69,0.05);"><i data-lucide="x" style="width:20px;"></i></button>
                            </form>
                        </div>
                    </div>
                {% endfor %}
                </div>
            {% else %}
                <div style="padding: 2rem; text-align: center; border: 1px dashed #333; border-radius: 8px;">
                    <p class="text-dim">No hay turnos agendados para hoy.</p>
                </div>
            {% endif %}
        </div>
"""
if "MOBILE CARDS VIEW" not in dash:
    dash = dash.replace("</div>\n\n        <div class=\"mt-2 flex-between mb-2\">\n            <h3 class=\"space-font\">Venta de Mostrador rApida</h3>", "</div>\n" + mobile_cards + "\n        <div class=\"mt-2 flex-between mb-2\">\n            <h3 class=\"space-font\">Venta de Mostrador rApida</h3>")

with open(dash_path, "w", encoding="utf-8") as f:
    f.write(dash)

