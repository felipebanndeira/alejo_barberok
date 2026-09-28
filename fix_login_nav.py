import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"

# 1. Update login.html
login_path = os.path.join(base, "templates/admin/login.html")
with open(login_path, "r", encoding="utf-8") as f:
    login = f.read()

# Replace password input with a wrapper that has the eye icon
old_pass = '<input type="password" name="password" placeholder="ContraseAa" required>'
# Since the encoding might be messed up in the file, let's use regex
pass_regex = r'<input type="password" name="password" placeholder=".*?" required>'

new_pass = """
            <div style="position: relative;">
                <input type="password" name="password" id="login-password" placeholder="Contraseña" required style="width: 100%; padding-right: 40px;">
                <button type="button" onclick="togglePassword()" style="position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background: none; border: none; color: var(--text-dim); cursor: pointer; padding: 0;">
                    <i data-lucide="eye" id="eye-icon" style="width: 20px; height: 20px;"></i>
                </button>
            </div>
            
            <script>
            function togglePassword() {
                const input = document.getElementById('login-password');
                const icon = document.getElementById('eye-icon');
                if (input.type === 'password') {
                    input.type = 'text';
                    icon.setAttribute('data-lucide', 'eye-off');
                } else {
                    input.type = 'password';
                    icon.setAttribute('data-lucide', 'eye');
                }
                if (window.lucide) {
                    lucide.createIcons();
                }
            }
            </script>
"""

login = re.sub(pass_regex, new_pass, login)

# Also fix the weird encoding in 'Correo ElectrA3nico'
login = login.replace("Correo ElectrA3nico", "Correo Electrónico")

with open(login_path, "w", encoding="utf-8") as f:
    f.write(login)


# 2. Update style.css for responsive header
css_path = os.path.join(base, "static/css/style.css")
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

old_nav_css = """    .top-header {
        padding: 1rem;
        flex-wrap: wrap;
    }
    .header-nav {
        display: flex;
        align-items: center;
    }
    .header-nav a {
        margin-left: 1rem;
        white-space: nowrap;
    }"""

new_nav_css = """    .top-header {
        flex-direction: column;
        justify-content: center;
        gap: 1rem;
        padding: 1.5rem 1rem;
    }
    .header-logo {
        font-size: 1.25rem;
    }
    .header-nav {
        display: flex;
        width: 100%;
        justify-content: center;
    }
    .header-nav a {
        margin: 0 0.8rem;
        font-size: 1.05rem;
        white-space: nowrap;
    }"""

if old_nav_css in css:
    css = css.replace(old_nav_css, new_nav_css)
else:
    print("Could not find exact CSS match. Using regex.")
    # Fallback if whitespace differs
    css = re.sub(r'\.top-header\s*\{\s*padding:\s*1rem;\s*flex-wrap:\s*wrap;\s*\}.*?white-space:\s*nowrap;\s*\}', new_nav_css, css, flags=re.DOTALL)

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)

print("Done")
