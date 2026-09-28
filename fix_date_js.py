import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"
js_path = os.path.join(base, "static/js/main.js")

with open(js_path, "r", encoding="utf-8") as f:
    js = f.read()

# Add display update in dateInput event listener
old_js = """dateInput.addEventListener('change', async function() {
        bookingData.date = this.value;"""
        
new_js = """dateInput.addEventListener('change', async function() {
        bookingData.date = this.value;
        const [year, month, day] = this.value.split('-');
        const dateDisplay = document.getElementById('date-display');
        if (dateDisplay) {
            dateDisplay.textContent = `${day}/${month}/${year}`;
        }"""

js = js.replace(old_js, new_js)

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js)

