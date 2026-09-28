import os

base = r"c:\Users\usser\Documents\Alejo barber"
files = ["templates/admin/finances.html", "templates/admin/blocks.html", "templates/admin/users.html", "templates/admin/settings.html", "templates/admin/dashboard.html"]

sidebar_html = """    <aside class="sidebar">
        <div class="sidebar-logo mb-2">
            {% if settings.get('logo_path') %}
                <img src="{{ url_for('static', filename='img/' + settings.get('logo_path')) }}" alt="Logo">
            {% endif %}
            <h2 class="space-font">{{ settings.get('barber_name', 'Alejo Barber') }}</h2>
        </div>
        <ul>
            <li><a href="{{ url_for('admin.dashboard') }}" {% if request.endpoint == 'admin.dashboard' %}class="active"{% endif %}>Agenda</a></li>
            <li><a href="{{ url_for('admin.finances') }}" {% if request.endpoint == 'admin.finances' %}class="active"{% endif %}>Caja</a></li>
            <li><a href="{{ url_for('admin.blocks') }}" {% if request.endpoint == 'admin.blocks' %}class="active"{% endif %}>Bloqueos</a></li>
            <li><a href="{{ url_for('admin.users') }}" {% if request.endpoint == 'admin.users' %}class="active"{% endif %}>Accesos</a></li>
        </ul>
    </aside>"""

import re
for rel in files:
    path = os.path.join(base, rel)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace anything from <div class="sidebar"> or <aside class="sidebar"> up to </ul>\n    </div> or </ul>\n    </aside>
    new_content = re.sub(r'<(div|aside) class="sidebar">.*?</ul>\n\s*</\1>', sidebar_html, content, flags=re.DOTALL)
    
    # Some hardcoded active states in dashboard.html might conflict if we rely on request.endpoint, but request.endpoint is better.
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"Unified sidebar in {rel}")
