import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"

# Update routes
with open(os.path.join(base, "routes/admin_routes.py"), "r", encoding="utf-8") as f:
    routes_content = f.read()

new_routes = '''

@admin_bp.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    db = get_db()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        from werkzeug.security import generate_password_hash
        try:
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                       (email, generate_password_hash(password)))
            db.commit()
            flash('Usuario agregado correctamente')
        except:
            flash('Error: El usuario/correo ya existe')
        return redirect(url_for('admin.users'))
        
    users_list = db.execute("SELECT id, username FROM users").fetchall()
    return render_template('admin/users.html', users=users_list)

@admin_bp.route('/users/<int:id>/delete', methods=['POST'])
@login_required
def delete_user(id):
    if id == session.get('user_id'):
        flash('No puedes borrar tu propia cuenta')
        return redirect(url_for('admin.users'))
        
    db = get_db()
    db.execute("DELETE FROM users WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for('admin.users'))
'''

if "/users" not in routes_content:
    with open(os.path.join(base, "routes/admin_routes.py"), "a", encoding="utf-8") as f:
        f.write(new_routes)

# Update templates sidebar
templates_to_update = ["dashboard.html", "settings.html", "blocks.html"]
sidebar_link = '''            <li><a href="{{ url_for('admin.users') }}" {% if request.endpoint == 'admin.users' %}class="active"{% endif %}><i data-lucide="users"></i> Accesos</a></li>'''

for t in templates_to_update:
    path = os.path.join(base, f"templates/admin/{t}")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "admin.users" not in content:
        content = content.replace(
            '''<li><a href="{{ url_for('admin.blocks') }}"''',
            sidebar_link + '''\n            <li><a href="{{ url_for('admin.blocks') }}"'''
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

# Change login placeholder
login_path = os.path.join(base, "templates/admin/login.html")
with open(login_path, "r", encoding="utf-8") as f:
    login_content = f.read()
login_content = login_content.replace('placeholder="Usuario"', 'placeholder="Correo Electrónico"')
with open(login_path, "w", encoding="utf-8") as f:
    f.write(login_content)

# Create users.html
users_html = '''{% extends 'base.html' %}
{% block title %}Accesos - Admin{% endblock %}

{% block content %}
<div class="admin-layout">
    <div class="sidebar">
        <h2 class="gold-text"><i data-lucide="scissors"></i> Alejo Barber</h2>
        <ul>
            <li><a href="{{ url_for('admin.dashboard') }}"><i data-lucide="layout-dashboard"></i> Dashboard</a></li>
            <li><a href="{{ url_for('admin.settings') }}"><i data-lucide="settings"></i> Configuración</a></li>
            <li><a href="{{ url_for('admin.users') }}" class="active"><i data-lucide="users"></i> Accesos</a></li>
            <li><a href="{{ url_for('admin.blocks') }}"><i data-lucide="calendar-off"></i> Bloqueos</a></li>
            <li class="mt-2"><a href="{{ url_for('admin.logout') }}"><i data-lucide="log-out"></i> Salir</a></li>
        </ul>
    </div>
    <div class="admin-content">
        <h2 class="mb-2">Correos Autorizados (Admins)</h2>
        
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                <div style="color: #primary-gold; margin-bottom: 1rem;">{{ messages[0] }}</div>
            {% endif %}
        {% endwith %}

        <div class="stats-grid">
            <div class="glass-panel">
                <h3 class="mb-2">Agregar Acceso</h3>
                <form method="POST">
                    <label>Correo Electrónico</label>
                    <input type="email" name="email" required>
                    
                    <label>Contraseña</label>
                    <input type="password" name="password" required>
                    
                    <button type="submit" class="btn-gold mt-2 w-100">Autorizar Correo</button>
                </form>
            </div>
            
            <div class="glass-panel">
                <h3 class="mb-2">Usuarios Actuales</h3>
                {% if users %}
                <table>
                    <thead>
                        <tr>
                            <th>Correo / Usuario</th>
                            <th>Acción</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for u in users %}
                        <tr>
                            <td>{{ u.username }}</td>
                            <td>
                                <form method="POST" action="{{ url_for('admin.delete_user', id=u.id) }}">
                                    <button type="submit" class="btn-glass" style="padding:0.25rem 0.5rem;"><i data-lucide="trash-2" style="width:16px;"></i></button>
                                </form>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <p class="text-dim">No hay usuarios.</p>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''
with open(os.path.join(base, "templates/admin/users.html"), "w", encoding="utf-8") as f:
    f.write(users_html)

