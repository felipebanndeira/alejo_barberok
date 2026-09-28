import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "core/availability.py")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# We will rewrite the end of get_available_times
old_logic = """    booked_times = [a['time'] for a in appointments]
    slots = [s for s in slots if s not in booked_times]
    
    return slots"""

new_logic = """    booked_times = [a['time'] for a in appointments]
    
    # Return objects instead of strings
    result = []
    for s in slots:
        if s in booked_times:
            result.append({"time": s, "available": False})
        else:
            result.append({"time": s, "available": True})
            
    return result"""

content = content.replace(old_logic, new_logic)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
