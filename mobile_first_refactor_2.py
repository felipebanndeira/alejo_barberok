import os

base = r"c:\Users\usser\Documents\Alejo barber"
dash_path = os.path.join(base, "templates/admin/dashboard.html")
with open(dash_path, "r", encoding="utf-8") as f:
    dash = f.read()

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
                            
                            <a href="https://wa.me/{{a.client_phone|replace('+', '')}}?text=Hola {{a.client_name}}, te recuerdo tu turno de hoy a las {{a.time}} para el servicio de {{a.service_name}}. ¡Te espero!" target="_blank" class="btn-outline" style="flex:1; text-align:center; padding:0.8rem; border-color:rgba(255,204,0,0.3); color:var(--primary-gold); background:rgba(255,204,0,0.05);">
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

# Insert right after the closing </div> of the table-container
target = "{% endif %}\n        </div>"
if target in dash and "MOBILE CARDS VIEW" not in dash:
    dash = dash.replace(target, target + "\n" + mobile_cards, 1)
    with open(dash_path, "w", encoding="utf-8") as f:
        f.write(dash)
    print("Success")
else:
    print("Target not found or already inserted")

