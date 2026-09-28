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

function updateStepperUI() {
    // Update progress lines
    document.querySelectorAll('.step-line').forEach((line, index) => {
        if(index < currentStep) {
            line.classList.add('active');
        } else {
            line.classList.remove('active');
        }
    });
    
    // Update step label
    const labels = ["Servicios", "Fecha y Hora", "Información del Cliente"];
    const stepLabel = document.getElementById('step-label');
    if(stepLabel) {
        stepLabel.textContent = `Paso ${currentStep} de 3 — ${labels[currentStep-1]}`;
    }
}

function nextStep(step) {
    document.getElementById(`step${currentStep}`).classList.remove('active');
    currentStep = step;
    document.getElementById(`step${currentStep}`).classList.add('active');
    updateSummary();
    updateStepperUI();
}

function prevStep(step) {
    document.getElementById(`step${currentStep}`).classList.remove('active');
    currentStep = step;
    document.getElementById(`step${currentStep}`).classList.add('active');
    updateSummary();
    updateStepperUI();
}

// Step 1: Services
document.querySelectorAll('.service-card').forEach(card => {
    card.addEventListener('click', function() {
        document.querySelectorAll('.service-card').forEach(c => {
            c.classList.remove('selected');
            c.querySelector('.check-icon').style.display = 'none';
        });
        this.classList.add('selected');
        this.querySelector('.check-icon').style.display = 'block';
        
        bookingData.service_id = this.dataset.id;
        bookingData.service_name = this.dataset.name;
        bookingData.service_price = this.dataset.price;
        
        // Update sticky footer total
        const formattedPrice = bookingData.service_price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
        document.getElementById('footer-total').textContent = `$${formattedPrice}`;
        document.getElementById('footer-next').style.display = 'inline-block';
        document.getElementById('footer-next').onclick = () => nextStep(2);
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
        const dateDisplay = document.getElementById('date-display');
        if (dateDisplay) {
            if (this.value) {
                const [year, month, day] = this.value.split('-');
                dateDisplay.textContent = `${day}/${month}/${year}`;
            } else {
                dateDisplay.textContent = 'Elegir Fecha';
            }
        }
        const slotsContainer = document.getElementById('time-slots');
        slotsContainer.innerHTML = '<p class="text-dim text-center" style="grid-column: 1/-1;">Cargando horarios...</p>';
        document.getElementById('footer-next').style.display = 'none';
        
        try {
            const res = await fetch(`/api/availability?date=${this.value}`);
            const times = await res.json();
            
            slotsContainer.innerHTML = '';
            if(times.length === 0) {
                slotsContainer.innerHTML = '<p class="text-dim text-center" style="grid-column: 1/-1;">No hay horarios disponibles.</p>';
                return;
            }
            
            times.forEach(slot => {
                const div = document.createElement('div');
                div.className = 'time-slot';
                
                if (slot.available) {
                    div.textContent = slot.time;
                    div.onclick = function() {
                        document.querySelectorAll('.time-slot').forEach(t => t.classList.remove('selected'));
                        this.classList.add('selected');
                        bookingData.time = slot.time;
                        document.getElementById('footer-next').style.display = 'inline-block';
                        document.getElementById('footer-next').onclick = () => nextStep(3);
                    };
                } else {
                    div.innerHTML = `<span style="text-decoration: line-through; opacity: 0.5;">${slot.time}</span><br><span style="font-size: 0.75rem; color: #ef4444; font-weight: 700;">Ocupado</span>`;
                    div.style.pointerEvents = 'none';
                    div.style.background = 'rgba(255, 0, 0, 0.05)';
                    div.style.borderColor = 'rgba(255, 0, 0, 0.1)';
                    div.style.display = 'flex';
                    div.style.flexDirection = 'column';
                    div.style.justifyContent = 'center';
                }
                
                slotsContainer.appendChild(div);
            });
        } catch (e) {
            slotsContainer.innerHTML = '<p class="text-dim text-center" style="grid-column: 1/-1;">Error al cargar horarios.</p>';
        }
    });
}

// Update Summary for Step 3
function updateSummary() {
    if(currentStep === 3) {
        document.getElementById('footer-next').textContent = "Confirmar";
        document.getElementById('footer-next').onclick = confirmBooking;
    } else if(currentStep === 2) {
        document.getElementById('footer-next').textContent = "Continuar";
        document.getElementById('footer-next').onclick = () => nextStep(3);
        if(!bookingData.time) {
            document.getElementById('footer-next').style.display = 'none';
        } else {
            document.getElementById('footer-next').style.display = 'inline-block';
        }
    } else if(currentStep === 1) {
        document.getElementById('footer-next').textContent = "Continuar";
        document.getElementById('footer-next').onclick = () => nextStep(2);
        if(!bookingData.service_id) {
            document.getElementById('footer-next').style.display = 'none';
        } else {
            document.getElementById('footer-next').style.display = 'inline-block';
        }
    }
    
    if(currentStep > 1) {
        document.getElementById('footer-prev').style.display = 'inline-block';
        document.getElementById('footer-prev').onclick = () => prevStep(currentStep - 1);
    } else {
        document.getElementById('footer-prev').style.display = 'none';
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
            document.getElementById('step3').innerHTML = `
                <div class="text-center" style="margin-top: 2rem;">
                    <i data-lucide="check-circle" class="gold-text mb-2 neon-icon" style="width:80px;height:80px;"></i>
                    <h2 class="mb-2">¡Turno Confirmado!</h2>
                    <p class="text-dim">Te esperamos el ${bookingData.date.split('-')[2]}/${bookingData.date.split('-')[1]}/${bookingData.date.split('-')[0]} a las ${bookingData.time}.</p>
                    <button class="btn-gold mt-2 w-100" onclick="location.reload()">Nuevo Turno</button>
                </div>
            `;
            document.querySelector('.sticky-footer').style.display = 'none';
            document.querySelector('.stepper-wrapper').style.display = 'none';
            lucide.createIcons();
        } else {
            alert(data.message || 'Error al confirmar el turno.');
        }
    } catch (e) {
        alert('Error de conexión.');
    }
}

// Init
updateStepperUI();
