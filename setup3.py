import os

base = r"c:\Users\usser\Documents\Alejo barber"

files = {
    r"static\css\style.css": '''
:root {
    --bg-color: #050505;
    --primary-gold: #D4AF37;
    --primary-gold-dim: rgba(212, 175, 55, 0.2);
    --text-light: #F5F5F5;
    --text-dim: #A0A0A0;
    --glass-bg: rgba(255, 255, 255, 0.03);
    --glass-border: rgba(255, 255, 255, 0.08);
    --glass-glow: rgba(212, 175, 55, 0.15);
    
    font-family: 'Inter', -apple-system, sans-serif;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    background-color: var(--bg-color);
    color: var(--text-light);
    min-height: 100vh;
    overflow-x: hidden;
    position: relative;
}

/* Custom Cursor Glow */
#cursor-glow {
    position: fixed;
    top: 0;
    left: 0;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, var(--primary-gold-dim) 0%, rgba(5,5,5,0) 70%);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    pointer-events: none;
    z-index: -1;
    transition: width 0.3s, height 0.3s;
}

/* Typography */
h1, h2, h3, h4 {
    font-weight: 300;
    letter-spacing: 1px;
}

.gold-text {
    color: var(--primary-gold);
}

/* Glassmorphism Classes */
.glass-panel {
    background: var(--glass-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
    padding: 2rem;
}

/* Buttons */
.btn-gold {
    background: transparent;
    color: var(--primary-gold);
    border: 1px solid var(--primary-gold);
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.btn-gold:hover {
    background: var(--primary-gold);
    color: var(--bg-color);
    box-shadow: 0 0 15px var(--glass-glow);
}

.btn-glass {
    background: var(--glass-bg);
    color: var(--text-light);
    border: 1px solid var(--glass-border);
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn-glass:hover {
    background: rgba(255, 255, 255, 0.1);
}

/* Layout */
.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
}

/* Stepper */
.step-container {
    display: none;
    animation: fadeUp 0.5s ease forwards;
}

.step-container.active {
    display: block;
}

/* Animations */
@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Cards */
.service-card {
    border: 1px solid var(--glass-border);
    padding: 1.5rem;
    border-radius: 12px;
    margin-bottom: 1rem;
    cursor: pointer;
    transition: all 0.3s;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.service-card:hover, .service-card.selected {
    border-color: var(--primary-gold);
    background: rgba(212, 175, 55, 0.05);
}

/* Forms */
input, select {
    width: 100%;
    background: rgba(255,255,255,0.05);
    border: 1px solid var(--glass-border);
    color: var(--text-light);
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    font-family: inherit;
}

input:focus {
    outline: none;
    border-color: var(--primary-gold);
}

/* Time slots */
.time-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 1rem;
}

.time-slot {
    padding: 0.75rem;
    text-align: center;
    border: 1px solid var(--glass-border);
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
}

.time-slot:hover, .time-slot.selected {
    border-color: var(--primary-gold);
    color: var(--primary-gold);
}

/* Admin Dashboard layout */
.admin-layout {
    display: grid;
    grid-template-columns: 250px 1fr;
    min-height: 100vh;
}

.sidebar {
    background: var(--glass-bg);
    border-right: 1px solid var(--glass-border);
    padding: 2rem;
}

.sidebar ul {
    list-style: none;
    margin-top: 2rem;
}

.sidebar li {
    margin-bottom: 1rem;
}

.sidebar a {
    color: var(--text-dim);
    text-decoration: none;
    transition: color 0.3s;
    display: flex;
    align-items: center;
    gap: 10px;
}

.sidebar a:hover, .sidebar a.active {
    color: var(--primary-gold);
}

.admin-content {
    padding: 2rem;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.stat-card {
    text-align: center;
}

.stat-card h3 {
    font-size: 2.5rem;
    color: var(--primary-gold);
    margin: 1rem 0;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
}

th, td {
    padding: 1rem;
    text-align: left;
    border-bottom: 1px solid var(--glass-border);
}

th {
    color: var(--text-dim);
    font-weight: normal;
}

.badge {
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.8rem;
}
.badge.pending { background: rgba(255, 193, 7, 0.2); color: #ffc107; }
.badge.confirmed { background: rgba(40, 167, 69, 0.2); color: #28a745; }
.badge.cancelled { background: rgba(220, 53, 69, 0.2); color: #dc3545; }

/* Utils */
.flex-between { display: flex; justify-content: space-between; align-items: center; }
.mt-2 { margin-top: 2rem; }
.mb-2 { margin-bottom: 2rem; }
.text-center { text-align: center; }
''',
    r"static\js\cursor.js": '''
document.addEventListener('DOMContentLoaded', () => {
    const glow = document.createElement('div');
    glow.id = 'cursor-glow';
    document.body.appendChild(glow);

    let mouseX = 0, mouseY = 0;
    let glowX = 0, glowY = 0;

    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    // Smooth follow effect
    function animate() {
        glowX += (mouseX - glowX) * 0.1;
        glowY += (mouseY - glowY) * 0.1;
        
        glow.style.left = glowX + 'px';
        glow.style.top = glowY + 'px';
        
        requestAnimationFrame(animate);
    }
    
    animate();

    // Enlarge on clickable elements
    const clickables = document.querySelectorAll('button, a, input, select, .service-card, .time-slot');
    clickables.forEach(el => {
        el.addEventListener('mouseenter', () => {
            glow.style.width = '400px';
            glow.style.height = '400px';
        });
        el.addEventListener('mouseleave', () => {
            glow.style.width = '300px';
            glow.style.height = '300px';
        });
    });
});
''',
    r"static\js\main.js": '''
// Stepper Logic
let currentStep = 1;
let bookingData = {
    service_id: null,
    service_name: null,
    service_price: null,
    date: null,
    time: null,
    name: null,
    phone: null
};

function nextStep(step) {
    document.getElementById(step).classList.remove('active');
    currentStep = step;
    document.getElementById(step).classList.add('active');
    updateSummary();
}

function prevStep(step) {
    document.getElementById(step).classList.remove('active');
    currentStep = step;
    document.getElementById(step).classList.add('active');
}

// Step 1: Services
document.querySelectorAll('.service-card').forEach(card => {
    card.addEventListener('click', function() {
        document.querySelectorAll('.service-card').forEach(c => c.classList.remove('selected'));
        this.classList.add('selected');
        
        bookingData.service_id = this.dataset.id;
        bookingData.service_name = this.dataset.name;
        bookingData.service_price = this.dataset.price;
        
        document.getElementById('btn-next-1').style.display = 'inline-block';
    });
});

// Step 2: Date & Time
const dateInput = document.getElementById('date-picker');
if(dateInput) {
    // Set min date to today
    const today = new Date().toISOString().split('T')[0];
    dateInput.min = today;
    
    dateInput.addEventListener('change', async function() {
        bookingData.date = this.value;
        const slotsContainer = document.getElementById('time-slots');
        slotsContainer.innerHTML = '<p>Cargando horarios...</p>';
        
        try {
            const res = await fetch(/api/availability?date=);
            const times = await res.json();
            
            slotsContainer.innerHTML = '';
            if(times.length === 0) {
                slotsContainer.innerHTML = '<p>No hay horarios disponibles para esta fecha.</p>';
                document.getElementById('btn-next-2').style.display = 'none';
                return;
            }
            
            times.forEach(time => {
                const div = document.createElement('div');
                div.className = 'time-slot';
                div.textContent = time;
                div.onclick = function() {
                    document.querySelectorAll('.time-slot').forEach(t => t.classList.remove('selected'));
                    this.classList.add('selected');
                    bookingData.time = time;
                    document.getElementById('btn-next-2').style.display = 'inline-block';
                };
                slotsContainer.appendChild(div);
            });
        } catch (e) {
            slotsContainer.innerHTML = '<p>Error al cargar horarios.</p>';
        }
    });
}

// Update Summary for Step 3
function updateSummary() {
    if(currentStep === 3) {
        document.getElementById('summary-service').textContent = bookingData.service_name;
        document.getElementById('summary-date').textContent = ${bookingData.date} a las ;
        document.getElementById('summary-price').textContent = $;
    }
}

// Confirm Booking
async function confirmBooking() {
    bookingData.name = document.getElementById('client-name').value;
    bookingData.phone = document.getElementById('client-phone').value;
    
    if(!bookingData.name || !bookingData.phone) {
        alert('Por favor completa tus datos.');
        return;
    }
    
    try {
        const res = await fetch('/api/book', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(bookingData)
        });
        const data = await res.json();
        
        if(data.success) {
            document.getElementById('step3').innerHTML = 
                <div class="text-center">
                    <i data-lucide="check-circle" class="gold-text mb-2" style="width:64px;height:64px;"></i>
                    <h2 class="mb-2">¡Turno Confirmado!</h2>
                    <p>Te esperamos el  a las .</p>
                    <button class="btn-gold mt-2" onclick="location.reload()">Nuevo Turno</button>
                </div>
            ;
            lucide.createIcons();
        } else {
            alert(data.message || 'Error al confirmar el turno.');
        }
    } catch (e) {
        alert('Error de conexión.');
    }
}
'''
}

for path, content in files.items():
    full_path = os.path.join(base, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
