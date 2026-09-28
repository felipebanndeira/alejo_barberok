import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"
css_path = os.path.join(base, "static/css/style.css")

with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# 1. Update step-line and stepper
css = css.replace(
'''.step-line {
    height: 2px;
    background: var(--border-color);
    flex: 1;
    transition: background 0.4s ease;
}
.step-line.active { background: var(--primary-gold); }''',
'''.step-line {
    height: 5px;
    background: #1f1f1f;
    border-radius: 4px;
    flex: 1;
    transition: all 0.4s ease;
}
.step-line.active {
    background: linear-gradient(90deg, var(--primary-gold), var(--light-gold));
    box-shadow: 0 0 12px rgba(201, 163, 78, 0.3);
}'''
)

# 2. Service cards
css = css.replace(
'''.service-card:hover { border-color: #333; }
.service-card.selected {
    border-color: var(--primary-gold);
    background: var(--primary-gold-dim);
}''',
'''.service-card:hover { 
    border-color: rgba(201, 163, 78, 0.3); 
    transform: scale(1.01);
    box-shadow: 0 8px 24px rgba(201, 163, 78, 0.08);
}
.service-card.selected {
    border-color: var(--primary-gold);
    background: var(--primary-gold-dim);
    transform: scale(1.01);
    box-shadow: 0 8px 24px rgba(201, 163, 78, 0.15);
}'''
)

# 3. Footer background and total
css = css.replace(
'''background: rgba(3, 3, 3, 0.85);
    backdrop-filter: blur(12px);''',
'''background: linear-gradient(to bottom, rgba(5,5,5,0.8), #030303 30%);
    backdrop-filter: blur(16px);'''
)
css = css.replace(
'''.btn-gold {
    background: var(--primary-gold);
    color: var(--bg-color);''',
'''.btn-gold {
    background: var(--primary-gold);
    color: #000;'''
)
css = css.replace(".footer-total h3 { font-size: 1.4rem; margin: 0; color: var(--text-light); }", ".footer-total h3 { font-size: 1.5rem; margin: 0; color: var(--text-light); font-weight: 700; letter-spacing: -0.02em; }")


with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)


# 4. Update index.html
index_path = os.path.join(base, "templates/cliente/index.html")
with open(index_path, "r", encoding="utf-8") as f:
    index = f.read()

# Make titles Space Grotesk
index = index.replace('<h2 class="mb-2">', '<h2 class="mb-2 space-font">')
index = index.replace('<h3 id="footer-total" class="num-font">', '<h3 id="footer-total" class="space-font">')
index = index.replace('class="service-price gold-text num-font"', 'class="service-price gold-text space-font"')
index = index.replace('<h3>{{ s.name }}</h3>', '<h3 class="space-font">{{ s.name }}</h3>')

# Format initial jinja prices
index = re.sub(
    r'\$\{\{ s\.price \}\}',
    r'${{ "{:,}".format(s.price).replace(",", ".") }}',
    index
)

# Add icons to service card
card_pattern = r'(<div class="service-header">\s*<div>\s*<h3)'
replacement = '''<div class="service-header">
                    <div style="display: flex; align-items: center; gap: 15px;">
                        {% set icon_name = 'scissors' %}
                        {% if 'barba' in s.name|lower and 'corte' in s.name|lower %}
                            {% set icon_name = 'sparkles' %}
                        {% elif 'barba' in s.name|lower %}
                            {% set icon_name = 'brush' %}
                        {% endif %}
                        <i data-lucide="{{ icon_name }}" style="color: var(--primary-gold); opacity: 0.8; width: 20px;"></i>
                        <div>
                            <h3'''
index = re.sub(card_pattern, replacement, index, count=1) # Note: this regex targets the first div wrapping h3 and replaces it, wait...
# Let's do it safer.
# Reload file
with open(index_path, "r", encoding="utf-8") as f:
    index = f.read()

index = index.replace('<h2 class="mb-2">', '<h2 class="mb-2 space-font">')
index = index.replace('<h3 id="footer-total" class="num-font">', '<h3 id="footer-total" class="space-font">')
index = index.replace('class="service-price gold-text num-font"', 'class="service-price gold-text space-font"')
index = index.replace('<h3>{{ s.name }}</h3>', '<h3 class="space-font">{{ s.name }}</h3>')
index = re.sub(r'\$\{\{ s\.price \}\}', r'${{ "{:,}".format(s.price).replace(",", ".") }}', index)

# Inject icon before h3
icon_code = '''
                        <div style="display:flex; gap: 12px; align-items: center;">
                            {% set icon_name = 'scissors' %}
                            {% if 'barba' in s.name|lower and 'corte' in s.name|lower %}
                                {% set icon_name = 'sparkles' %}
                            {% elif 'barba' in s.name|lower %}
                                {% set icon_name = 'brush' %}
                            {% endif %}
                            <i data-lucide="{{ icon_name }}" style="color: var(--primary-gold); width: 22px;"></i>
                            <div>
                                <h3 class="space-font">{{ s.name }}</h3>
                                <p class="text-dim" style="font-size: 0.85rem;">30 minutos</p>
                            </div>
                        </div>'''

old_title_div = '''<div>
                        <h3 class="space-font">{{ s.name }}</h3>
                        <p class="text-dim" style="font-size: 0.85rem;">30 minutos</p>
                    </div>'''

index = index.replace(old_title_div, icon_code)

# Add "Continuar" button to footer-next (update in JS later, but in HTML keep it as is, we will change it in JS)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(index)


# 5. Update main.js for number formatting and footer button
js_path = os.path.join(base, "static/js/main.js")
with open(js_path, "r", encoding="utf-8") as f:
    js = f.read()

js = js.replace(
'''document.getElementById('footer-total').textContent = `$${bookingData.service_price}`;''',
'''const formattedPrice = bookingData.service_price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
        document.getElementById('footer-total').textContent = `$${formattedPrice}`;'''
)
js = js.replace(
'''document.getElementById('footer-next').textContent = "Confirmar";''',
'''document.getElementById('footer-next').textContent = "Confirmar";
        document.getElementById('footer-next').className = "btn-gold";'''
)
js = js.replace(
'''document.getElementById('footer-next').textContent = "Siguiente >";''',
'''document.getElementById('footer-next').textContent = "Continuar";
        document.getElementById('footer-next').className = "btn-gold";'''
)
# Ensure btn-gold style is applied correctly by resetting className on click if necessary. Actually the prompt asks for it to be a solid gold button.
# Previously it was `btn-white` which was styled as a primary button, but maybe `btn-gold` is better.
# Let's change the HTML button class directly to btn-gold
js = js.replace("document.getElementById('footer-next').className = \"btn-gold\";", "") # clean up first

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js)

# Update index.html button class
with open(index_path, "r", encoding="utf-8") as f:
    index = f.read()
index = index.replace('class="btn-white" id="footer-next"', 'class="btn-gold" id="footer-next" style="display: none; width: auto;"')
with open(index_path, "w", encoding="utf-8") as f:
    f.write(index)

