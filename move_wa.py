import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"
index_path = os.path.join(base, "templates/cliente/index.html")

with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

# Extract the Whatsapp block
block_pattern = r'<div style="text-align: center; margin-top: 3rem;">\s*<p class="text-dim".*?Escribinos al WhatsApp\s*</a>\s*</p>\s*</div>'
match = re.search(block_pattern, content, flags=re.DOTALL)

if match:
    wa_block = match.group(0)
    # Remove from original position
    content = content.replace(wa_block, '')
    
    # Insert at the end of step 3
    step3_end = r'(<input type="tel" id="client-phone" required>\s*)</div>\s*(<div style="text-align: center; margin-top: 4rem; padding-bottom: 8rem;">|<div style="text-align: center; margin-top: 3rem;">|<div style="text-align: center;)'
    
    # Simple replacement: Find step 3 closing div
    content = re.sub(r'(<input type="tel" id="client-phone" required>\s*)</div>', r'\1\n' + wa_block + '\n</div>', content)
    
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)
else:
    print("Block not found")

