import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"
js_path = os.path.join(base, "static/js/main.js")

with open(js_path, "r", encoding="utf-8") as f:
    js = f.read()

old_js = """dateInput.addEventListener('change', async function() {
        bookingData.date = this.value;
        const [year, month, day] = this.value.split('-');
        const dateDisplay = document.getElementById('date-display');
        if (dateDisplay) {
            dateDisplay.textContent = `${day}/${month}/${year}`;
        }"""

new_js = """dateInput.addEventListener('change', async function() {
        bookingData.date = this.value;
        const dateDisplay = document.getElementById('date-display');
        if (dateDisplay) {
            if (this.value) {
                const [year, month, day] = this.value.split('-');
                dateDisplay.textContent = `${day}/${month}/${year}`;
            } else {
                dateDisplay.textContent = 'Elegir Fecha';
            }
        }"""

js = js.replace(old_js, new_js)

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js)

