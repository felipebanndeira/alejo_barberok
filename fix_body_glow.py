import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "static/css/style.css")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace body styles
old_body = """body {
    background-color: var(--bg-color);
    color: var(--text-light);
    font-family: var(--font-family);
    min-height: 100vh;
    padding-bottom: 100px;
    -webkit-font-smoothing: antialiased;
}"""

if "background-color: var(--bg-color);" in content:
    # We'll just replace the background part
    import re
    content = re.sub(
        r'body\s*\{[^}]*\}', 
        """body {
    background-color: var(--bg-color);
    background-image: 
        radial-gradient(circle at 10% 20%, rgba(255, 204, 0, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 90% 15%, rgba(255, 204, 0, 0.06) 0%, transparent 40%),
        radial-gradient(circle at 50% 85%, rgba(255, 204, 0, 0.07) 0%, transparent 50%);
    background-attachment: fixed;
    color: var(--text-light);
    min-height: 100vh;
    padding-bottom: 100px;
    -webkit-font-smoothing: antialiased;
}""", 
        content
    )

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
