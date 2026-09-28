import os

base = r"c:\Users\usser\Documents\Alejo barber"
css_path = os.path.join(base, "static/css/style.css")

with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# Update Gold
css = css.replace("--primary-gold: #e2c073;", "--primary-gold: #D4AF37;")
css = css.replace("--primary-gold-dim: rgba(226, 192, 115, 0.08);", "--primary-gold-dim: rgba(212, 175, 55, 0.1);")

# Add Vinotinto Cursor Glow
cursor_glow_css = """

/* Custom Cursor Glow (Vinotinto) */
#cursor-glow {
    position: fixed;
    top: 0;
    left: 0;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(128, 0, 32, 0.25) 0%, rgba(128, 0, 32, 0) 70%);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    pointer-events: none;
    z-index: 0;
    transition: width 0.3s, height 0.3s;
}

"""

if "#cursor-glow" not in css:
    css += cursor_glow_css

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)
