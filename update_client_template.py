import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "templates/cliente/mis_turnos.html")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Add a message at the top of the history
msg = '<p class="text-dim" style="font-size:0.85rem; text-align:center; margin-bottom:1.5rem;"><i data-lucide="info" style="width:14px;height:14px;vertical-align:middle;"></i> Los turnos solo se pueden cancelar desde acá con más de 2 hs de anticipación.</p>'
content = content.replace('<h3 class="mb-2 space-font text-center" style="margin-top: 3rem;">Historial de Turnos</h3>', '<h3 class="mb-2 space-font text-center" style="margin-top: 3rem;">Tus Turnos</h3>\n            ' + msg)


# Update the footer of the card to include the cancel button if can_cancel
old_footer = """                <div class="mt-footer">
                    <span class="mt-pill {{ t.status }}">
                        {% if t.status == 'pending' %}Pendiente{% endif %}
                        {% if t.status == 'confirmed' %}Confirmado{% endif %}
                        {% if t.status == 'cancelled' %}Cancelado{% endif %}
                    </span>
                </div>"""

new_footer = """                <div class="mt-footer" style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="mt-pill {{ t.status }}">
                        {% if t.status == 'pending' %}Pendiente{% endif %}
                        {% if t.status == 'confirmed' %}Confirmado{% endif %}
                        {% if t.status == 'cancelled' %}Cancelado{% endif %}
                    </span>
                    {% if t.can_cancel %}
                    <form method="POST" action="{{ url_for('cliente.cancelar_turno_cliente', id=t.id) }}" style="margin:0;" onsubmit="return confirm('¿Seguro que querés cancelar este turno?');">
                        <input type="hidden" name="phone" value="{{ request.form.get('phone', '') }}">
                        <button type="submit" style="background:transparent; border:1px solid #3f3f46; color:#ef4444; border-radius:6px; padding:0.35rem 0.75rem; font-size:0.75rem; font-weight:600; cursor:pointer;">Cancelar Turno</button>
                    </form>
                    {% elif t.status != 'cancelled' %}
                    <a href="https://wa.me/{{ settings.get('barber_phone', '') }}?text=Hola {{ settings.get('barber_name', 'Alejo') }}, te quería avisar que no voy a poder ir a mi turno de las {{t.time}}." target="_blank" style="font-size:0.75rem; color:#a1a1aa; text-decoration:underline;">Avisar tardanza/ausencia</a>
                    {% endif %}
                </div>"""

content = content.replace(old_footer, new_footer)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
