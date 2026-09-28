import os

base = r"c:\Users\usser\Documents\Alejo barber"
js_path = os.path.join(base, "static/js/main.js")

with open(js_path, "r", encoding="utf-8") as f:
    js = f.read()

old_summary = """function updateSummary() {
    if(currentStep === 3) {
        document.getElementById('footer-next').textContent = "Confirmar";
        
        document.getElementById('footer-next').onclick = confirmBooking;
    } else {
        document.getElementById('footer-next').textContent = "Continuar";
        
        if(currentStep === 1 && !bookingData.service_id) {
            document.getElementById('footer-next').style.display = 'none';
        }
        if(currentStep === 2 && !bookingData.time) {
            document.getElementById('footer-next').style.display = 'none';
        }
    }
    
    if(currentStep > 1) {
        document.getElementById('footer-prev').style.display = 'inline-block';
        document.getElementById('footer-prev').onclick = () => prevStep(currentStep - 1);
    } else {
        document.getElementById('footer-prev').style.display = 'none';
    }
}"""

new_summary = """function updateSummary() {
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
}"""

if old_summary in js:
    js = js.replace(old_summary, new_summary)
else:
    print("Function not found!")

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js)
