import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "static/css/style.css")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# Add color-scheme to inputs
old_input = """input, select, textarea {
    width: 100%;
    background: #0a0a0a;"""

new_input = """input, select, textarea {
    width: 100%;
    background: #0a0a0a;
    color-scheme: dark;"""

content = content.replace(old_input, new_input)

# Force option colors
if "option {" not in content:
    content += "\noption { background: #0a0a0a; color: white; }\n"

# Check time picker indicator
if "input[type=\"time\"]" not in content:
    content += "\ninput[type=\"time\"]::-webkit-calendar-picker-indicator { filter: invert(0.6); cursor: pointer; }\n"

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
