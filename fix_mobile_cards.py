import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"
dash_path = os.path.join(base, "templates/admin/dashboard.html")

with open(dash_path, "r", encoding="utf-8") as f:
    dash = f.read()

# Extract the schedule block
match = re.search(r'(<!-- MOBILE CARDS VIEW -->.*?<div class="mobile-only mb-2">.*?{% if schedule %}.*?<div.*?align-items: stretch;">)(.*?)({% endfor %}\s*</div>\s*{% endif %}\s*</div>)', dash, flags=re.DOTALL)

if match:
    prefix = match.group(1)
    suffix = match.group(3)
    
    new_card_html = """
                      <style>
                      .premium-card { background: #18181b; border-radius: 0.75rem; border: 1px solid #27272a; padding: 1.25rem; width: 100%; }
                      .pc-top { display: flex; justify-content: space-between; align-items: flex-start; }
                      .pc-time { font-size: 1.25rem; font-weight: 700; color: #facc15; font-family: 'Plus Jakarta Sans', sans-serif; line-height: 1.2; }
                      .pc-service { font-size: 0.875rem; color: #a1a1aa; margin-top: 0.25rem; }
                      .pc-client { text-align: right; }
                      .pc-name { font-size: 1rem; font-weight: 600; color: #ffffff; cursor: pointer; text-decoration: underline; text-decoration-color: #52525b; }
                      .pc-phone { font-size: 0.875rem; color: #a1a1aa; margin-top: 0.25rem; display: flex; align-items: center; justify-content: flex-end; gap: 4px; }
                      .pc-middle { margin-top: 0.75rem; display: flex; justify-content: flex-start; }
                      .pc-badge { border-radius: 9999px; padding: 0.25rem 0.75rem; font-size: 0.75rem; font-weight: 500; }
                      .pc-badge.pending { background: rgba(234, 179, 8, 0.1); color: #facc15; border: 1px solid rgba(234, 179, 8, 0.2); }
                      .pc-badge.confirmed { background: rgba(34, 197, 94, 0.1); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.2); }
                      .pc-badge.cancelled { background: rgba(239, 68, 68, 0.1); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.2); }
                      .pc-actions { border-top: 1px solid #27272a; padding-top: 0.75rem; margin-top: 0.75rem; display: flex; justify-content: flex-end; gap: 0.75rem; }
                      .pc-btn { width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; background: transparent; border: 1px solid #27272a; cursor: pointer; transition: background 0.2s, border-color 0.2s; }
                      .pc-btn:hover { background: #27272a; border-color: #3f3f46; }
                      .pc-btn.confirm { color: #22c55e; }
                      .pc-btn.delay { color: #eab308; }
                      .pc-btn.wa { color: #10b981; }
                      .pc-btn.cancel { color: #ef4444; }
                      .pc-btn svg { width: 18px !important; height: 18px !important; }
                      </style>
                      {% for a in schedule %}
                      <div class="premium-card">
                          <div class="pc-top">
                              <div>
                                  <div class="pc-time">{{ a.time }}</div>
                                  <div class="pc-service">{{ a.service_name }}</div>
                              </div>
                              <div class="pc-client">
                                  <div class="pc-name" onclick="openClientModal('{{ a.client_phone }}', '{{ a.client_name }}')">{{ a.client_name }}</div>
                                  <div class="pc-phone">
                                      <i data-lucide="phone" style="width: 12px; height: 12px;"></i> {{ a.client_phone }}
                                  </div>
                              </div>
                          </div>
                          <div class="pc-middle">
                              <span class="pc-badge {{ a.status }}">
                                  {% if a.status == 'pending' %}Pendiente{% endif %}
                                  {% if a.status == 'confirmed' %}Confirmado{% endif %}
                                  {% if a.status == 'cancelled' %}Cancelado{% endif %}
                              </span>
                          </div>
                          <div class="pc-actions">
                              {% if a.status == 'pending' %}
                              <form method="POST" action="{{ url_for('admin.update_status', id=a.id) }}" style="margin:0;">
                                  <input type="hidden" name="status" value="confirmed">
                                  <button type="submit" class="pc-btn confirm" title="Confirmar"><i data-lucide="check"></i></button>
                              </form>
                              {% endif %}
                              
                              <a href="https://wa.me/{{a.client_phone|replace('+', '')}}?text=Hola {{a.client_name}}, estoy con una pequeña demora. ¿Podrías venir unos 15 minutitos más tarde de tu turno de las {{a.time}}? ¡Gracias y disculpá!" target="_blank" class="pc-btn delay" title="Avisar Demora 15m">
                                  <i data-lucide="clock"></i>
                              </a>
                              
                              <a href="https://wa.me/{{a.client_phone|replace('+', '')}}?text=Hola {{a.client_name}}, te recuerdo tu turno de hoy a las {{a.time}} para el servicio de {{a.service_name}}." target="_blank" class="pc-btn wa" title="Enviar WhatsApp">
                                  <i data-lucide="message-circle"></i>
                              </a>
                              
                              <form method="POST" action="{{ url_for('admin.update_status', id=a.id) }}" style="margin:0;">
                                  <input type="hidden" name="status" value="cancelled">
                                  <button type="submit" class="pc-btn cancel" title="Cancelar"><i data-lucide="x"></i></button>
                              </form>
                          </div>
                      </div>
                      """
    
    new_html = dash[:match.start()] + prefix + new_card_html + suffix + dash[match.end():]
    with open(dash_path, "w", encoding="utf-8") as f:
        f.write(new_html)
    print("Successfully replaced mobile cards")
else:
    print("Regex failed")

