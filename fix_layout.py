import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"
file_path = os.path.join(base, "templates/cliente/mis_turnos.html")

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = """<div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <h3 class="space-font mb-2">{{ t.service_name }}</h3>
                            <p class="text-dim" style="font-size: 0.95rem; margin-bottom: 0.3rem;"><i data-lucide="calendar" style="width: 14px; vertical-align: middle;"></i> {{ t.date.split('-')[2] }}/{{ t.date.split('-')[1] }}/{{ t.date.split('-')[0] }}</p>
                            <p class="text-dim" style="font-size: 0.95rem;"><i data-lucide="clock" style="width: 14px; vertical-align: middle;"></i> {{ t.time }}</p>
                        </div>
                        <div style="text-align: right;">
                            <span class="badge {{ t.status }} space-font" style="
                                display: inline-block; 
                                margin-bottom: 1rem;
                                padding: 0.4rem 0.8rem;
                                border-radius: 4px;
                                {% if t.status == 'pending' %}background: rgba(255,193,7,0.1); color:#ffc107; border: 1px solid rgba(255,193,7,0.2);{% endif %}
                                {% if t.status == 'confirmed' %}background: rgba(40,167,69,0.1); color:#28a745; border: 1px solid rgba(40,167,69,0.2);{% endif %}
                                {% if t.status == 'cancelled' %}background: rgba(220,53,69,0.1); color:#dc3545; border: 1px solid rgba(220,53,69,0.2);{% endif %}
                            ">
                                {% if t.status == 'pending' %}Pendiente{% endif %}
                                {% if t.status == 'confirmed' %}Confirmado{% endif %}
                                {% if t.status == 'cancelled' %}Cancelado{% endif %}
                            </span>
                            <br>
                            <span class="gold-text space-font" style="font-size: 1.2rem; font-weight: 600;">${{ "{:,}".format(t.price|int).replace(",", ".") }}</span>
                        </div>
                    </div>"""

new_block = """<div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h3 class="space-font mb-2">{{ t.service_name }}</h3>
                            <div style="display: flex; gap: 15px;">
                                <p class="text-dim" style="font-size: 0.95rem; margin-bottom: 0;"><i data-lucide="calendar" style="width: 14px; vertical-align: text-bottom;"></i> {{ t.date.split('-')[2] }}/{{ t.date.split('-')[1] }}/{{ t.date.split('-')[0] }}</p>
                                <p class="text-dim" style="font-size: 0.95rem; margin-bottom: 0;"><i data-lucide="clock" style="width: 14px; vertical-align: text-bottom;"></i> {{ t.time }}</p>
                            </div>
                        </div>
                        <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 8px;">
                            <span class="badge {{ t.status }} space-font" style="
                                display: inline-block; 
                                padding: 0.4rem 0.8rem;
                                border-radius: 4px;
                                {% if t.status == 'pending' %}background: rgba(255,193,7,0.1); color:#ffc107; border: 1px solid rgba(255,193,7,0.2);{% endif %}
                                {% if t.status == 'confirmed' %}background: rgba(40,167,69,0.1); color:#28a745; border: 1px solid rgba(40,167,69,0.2);{% endif %}
                                {% if t.status == 'cancelled' %}background: rgba(220,53,69,0.1); color:#dc3545; border: 1px solid rgba(220,53,69,0.2);{% endif %}
                            ">
                                {% if t.status == 'pending' %}Pendiente{% endif %}
                                {% if t.status == 'confirmed' %}Confirmado{% endif %}
                                {% if t.status == 'cancelled' %}Cancelado{% endif %}
                            </span>
                            <span class="gold-text space-font" style="font-size: 1.2rem; font-weight: 600;">${{ "{:,}".format(t.price|int).replace(",", ".") }}</span>
                        </div>
                    </div>"""

if old_block in content:
    content = content.replace(old_block, new_block)
else:
    print("Block not found!")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

