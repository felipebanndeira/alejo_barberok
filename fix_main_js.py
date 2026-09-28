import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "static/js/main.js")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

import re

old_js = """            times.forEach(time => {
                const div = document.createElement('div');
                div.className = 'time-slot';
                div.textContent = time;
                div.onclick = function() {
                    document.querySelectorAll('.time-slot').forEach(t => t.classList.remove('selected'));
                    this.classList.add('selected');
                    bookingData.time = time;
                    document.getElementById('footer-next').style.display = 'inline-block';
                    document.getElementById('footer-next').onclick = () => nextStep(3);
                };
                slotsContainer.appendChild(div);
            });"""

new_js = """            times.forEach(slot => {
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
            });"""

content = content.replace(old_js, new_js)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
