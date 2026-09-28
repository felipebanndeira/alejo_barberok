import os

base = r"c:\Users\usser\Documents\Alejo barber"
css_path = os.path.join(base, "static/css/style.css")

with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

autofill_css = """
/* Fix for Chrome/Edge Autofill background in dark mode */
input:-webkit-autofill,
input:-webkit-autofill:hover, 
input:-webkit-autofill:focus, 
input:-webkit-autofill:active {
    -webkit-box-shadow: 0 0 0 30px #0a0a0a inset !important;
    -webkit-text-fill-color: var(--text-light) !important;
    transition: background-color 5000s ease-in-out 0s;
    border: 1px solid var(--primary-gold) !important;
}

input, select, textarea {
    width: 100%;
    background: #0a0a0a;
"""

css = css.replace("input, select, textarea {\n    width: 100%;\n    background: transparent;", autofill_css)

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)

