import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"
settings_path = os.path.join(base, "templates/admin/settings.html")

with open(settings_path, "r", encoding="utf-8") as f:
    content = f.read()

# Broad regex to remove deposit and bank details
remove_pattern = r'<label>Porcentaje de.*?<textarea name="bank_details".*?</textarea>'
content = re.sub(remove_pattern, '', content, flags=re.DOTALL)

with open(settings_path, "w", encoding="utf-8") as f:
    f.write(content)

