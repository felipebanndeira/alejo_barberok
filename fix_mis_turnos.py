import os

base = r"c:\Users\usser\Documents\Alejo barber"
mis_turnos_path = os.path.join(base, "templates/cliente/mis_turnos.html")

with open(mis_turnos_path, "r", encoding="utf-8") as f:
    html = f.read()

start_marker = '<div class="services-list">'
end_marker = '{% else %}'

start_idx = html.find(start_marker)
end_idx = html.find(end_marker, start_idx)

if start_idx != -1 and end_idx != -1:
    prefix = html[:start_idx]
    suffix = html[end_idx:]
    
    new_list_html = """<div class="services-list">
                <style>
                .premium-card { background: #18181b; border-radius: 0.75rem; border: 1px solid #27272a; padding: 1.25rem; width: 100%; box-sizing: border-box; margin-bottom: 1rem; }
                .pc-top { display: flex; justify-content: space-between; align-items: flex-start; }
                .pc-time { font-size: 1.25rem; font-weight: 700; color: #facc15; font-family: 'Plus Jakarta Sans', sans-serif; line-height: 1.2; }
                .pc-service { font-size: 1rem; font-weight: 600; color: #ffffff; margin-top: 0.25rem; }
                .pc-price { font-size: 1.2rem; font-weight: 700; color: #facc15; text-align: right; }
                .pc-date { font-size: 0.875rem; color: #a1a1aa; margin-top: 0.25rem; display: flex; align-items: center; justify-content: flex-end; gap: 4px; }
                .pc-middle { margin-top: 1rem; display: flex; justify-content: flex-end; border-top: 1px solid #27272a; padding-top: 1rem; }
                .pc-badge { border-radius: 9999px; padding: 0.3rem 0.8rem; font-size: 0.75rem; font-weight: 500; }
                .pc-badge.pending { background: rgba(234, 179, 8, 0.1); color: #facc15; border: 1px solid rgba(234, 179, 8, 0.2); }
                .pc-badge.confirmed { background: rgba(34, 197, 94, 0.1); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.2); }
                .pc-badge.cancelled { background: rgba(239, 68, 68, 0.1); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.2); }
                </style>
                {% for t in turnos %}
                <div class="premium-card">
                    <div class="pc-top">
                        <div>
                            <div class="pc-time">{{ t.time }}</div>
                            <div class="pc-service">{{ t.service_name }}</div>
                        </div>
                        <div>
                            <div class="pc-price">${{ "{:,}".format(t.price|int).replace(",", ".") }}</div>
                            <div class="pc-date">
                                <i data-lucide="calendar" style="width: 14px; height: 14px;"></i> {{ t.date.split('-')[2] }}/{{ t.date.split('-')[1] }}/{{ t.date.split('-')[0] }}
                            </div>
                        </div>
                    </div>
                    <div class="pc-middle">
                        <span class="pc-badge {{ t.status }}">
                            {% if t.status == 'pending' %}Pendiente{% endif %}
                            {% if t.status == 'confirmed' %}Confirmado{% endif %}
                            {% if t.status == 'cancelled' %}Cancelado{% endif %}
                        </span>
                    </div>
                </div>
                {% endfor %}
            </div>
        """
    
    new_html = prefix + new_list_html + "    " + suffix
    with open(mis_turnos_path, "w", encoding="utf-8") as f:
        f.write(new_html)
    print("Replaced mis_turnos cards.")
else:
    print("Could not find boundaries in mis_turnos")

