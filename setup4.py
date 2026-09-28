import os

base = r"c:\Users\usser\Documents\Alejo barber"

files = {
    r"templates\base.html": '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Alejo Barber{% endblock %}</title>
    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <!-- CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
</head>
<body>
    {% block content %}{% endblock %}

    <!-- Cursor Script -->
    <script src="{{ url_for('static', filename='js/cursor.js') }}"></script>
    {% block scripts %}{% endblock %}
    
    <script>
        lucide.createIcons();
    </script>
</body>
</html>
''',
    r"templates\cliente\index.html": '''{% extends 'base.html' %}

{% block content %}
<div class="container mt-2">
    <div class="text-center mb-2">
        {% if settings.get('logo_path') %}
            <img src="{{ url_for('static', filename='img/' + settings.get('logo_path')) }}" alt="Logo" style="max-height: 100px;">
        {% else %}
            <h1 class="gold-text">{{ settings.get('barber_name', 'Alejo Barber') }}</h1>
        {% endif %}
        <p class="text-dim">Reserva tu turno en 3 simples pasos</p>
    </div>

    <div class="glass-panel">
        <!-- Step 1 -->
        <div id="step1" class="step-container active">
            <h2 class="mb-2"><i data-lucide="scissors" class="gold-text"></i> Paso 1: Elegir Servicio</h2>
            <div class="services-list">
                {% for s in services %}
                <div class="service-card" data-id="{{ s.id }}" data-name="{{ s.name }}" data-price="{{ s.price }}">
                    <div>
                        <h3>{{ s.name }}</h3>
                        <p class="text-dim">30 min</p>
                    </div>
                    <div class="gold-text">${{ s.price }}</div>
                </div>
                {% endfor %}
            </div>
            <div class="text-center mt-2">
                <button class="btn-gold" id="btn-next-1" style="display:none;" onclick="nextStep(2)">Siguiente <i data-lucide="arrow-right"></i></button>
            </div>
        </div>

        <!-- Step 2 -->
        <div id="step2" class="step-container">
            <h2 class="mb-2"><i data-lucide="calendar" class="gold-text"></i> Paso 2: Elegir Fecha y Hora</h2>
            <input type="date" id="date-picker">
            <div id="time-slots" class="time-grid mt-2"></div>
            
            <div class="flex-between mt-2">
                <button class="btn-glass" onclick="prevStep(1)">Atrás</button>
                <button class="btn-gold" id="btn-next-2" style="display:none;" onclick="nextStep(3)">Siguiente <i data-lucide="arrow-right"></i></button>
            </div>
        </div>

        <!-- Step 3 -->
        <div id="step3" class="step-container">
            <h2 class="mb-2"><i data-lucide="check" class="gold-text"></i> Paso 3: Confirmar</h2>
            <div class="mb-2">
                <p><strong>Servicio:</strong> <span id="summary-service"></span></p>
                <p><strong>Fecha y Hora:</strong> <span id="summary-date"></span></p>
                <p><strong>Total:</strong> $<span id="summary-price" class="gold-text"></span></p>
                <p class="text-dim mt-2" style="font-size:0.9rem;">
                    Seña requerida: {{ settings.get('deposit_percentage', 0) }}% <br>
                    Transferir a:<br>
                    {{ settings.get('bank_details', '') | replace('\n', '<br>') | safe }}
                </p>
            </div>
            
            <input type="text" id="client-name" placeholder="Tu Nombre" required>
            <input type="tel" id="client-phone" placeholder="Tu WhatsApp" required>
            
            <div class="flex-between mt-2">
                <button class="btn-glass" onclick="prevStep(2)">Atrás</button>
                <button class="btn-gold" onclick="confirmBooking()">Confirmar Reserva</button>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script src="{{ url_for('static', filename='js/main.js') }}"></script>
{% endblock %}
''',
    r"templates\admin\login.html": '''{% extends 'base.html' %}
{% block title %}Login - Admin{% endblock %}

{% block content %}
<div class="container" style="max-width: 400px; margin-top: 10vh;">
    <div class="glass-panel text-center">
        <h2 class="gold-text mb-2"><i data-lucide="lock"></i> Acceso Admin</h2>
        
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                <div style="color: #dc3545; margin-bottom: 1rem;">{{ messages[0] }}</div>
            {% endif %}
        {% endwith %}
        
        <form method="POST">
            <input type="text" name="username" placeholder="Usuario" required>
            <input type="password" name="password" placeholder="Contraseña" required>
            <button type="submit" class="btn-gold w-100 mt-2" style="width: 100%;">Ingresar</button>
        </form>
    </div>
</div>
{% endblock %}
'''
}

for path, content in files.items():
    full_path = os.path.join(base, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
