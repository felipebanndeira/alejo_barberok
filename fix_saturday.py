import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "core/availability.py")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

import re

old_logic = """    if date_obj.weekday() >= 5:
        return [] # SAbados y domingos cerrados por defecto segAun el MVP
        
    start1 = settings.get('hours_mon_fri_start_1', '10:30')
    end1 = settings.get('hours_mon_fri_end_1', '13:00')
    start2 = settings.get('hours_mon_fri_start_2', '16:30')
    end2 = settings.get('hours_mon_fri_end_2', '21:00')
    
    # 2. Generate all possible slots (30 min increments)
    slots = []
    
    def generate_slots(start_str, end_str):
        if not start_str or not end_str: return
        current = datetime.strptime(f"{date_str} {start_str}", '%Y-%m-%d %H:%M')
        end_time = datetime.strptime(f"{date_str} {end_str}", '%Y-%m-%d %H:%M')
        
        while current + timedelta(minutes=30) <= end_time:
            slots.append(current.strftime('%H:%M'))
            current += timedelta(minutes=30)
            
    generate_slots(start1, end1)
    generate_slots(start2, end2)"""

new_logic = """    # Si es domingo (6), cerrado
    if date_obj.weekday() == 6:
        return []
        
    # 2. Generate all possible slots (30 min increments)
    slots = []
    
    def generate_slots(start_str, end_str):
        if not start_str or not end_str: return
        current = datetime.strptime(f"{date_str} {start_str}", '%Y-%m-%d %H:%M')
        end_time = datetime.strptime(f"{date_str} {end_str}", '%Y-%m-%d %H:%M')
        
        while current + timedelta(minutes=30) <= end_time:
            slots.append(current.strftime('%H:%M'))
            current += timedelta(minutes=30)

    # Si es sA!bado (5)
    if date_obj.weekday() == 5:
        sat_start = settings.get('hours_sat_start', '09:00')
        sat_end = settings.get('hours_sat_end', '13:00')
        generate_slots(sat_start, sat_end)
    else:
        # Lunes a viernes
        start1 = settings.get('hours_mon_fri_start_1', '10:30')
        end1 = settings.get('hours_mon_fri_end_1', '13:00')
        start2 = settings.get('hours_mon_fri_start_2', '16:30')
        end2 = settings.get('hours_mon_fri_end_2', '21:00')
        generate_slots(start1, end1)
        generate_slots(start2, end2)"""

# I need to use regex to replace it properly because of the special characters in the old comments
content = re.sub(r'    if date_obj\.weekday\(\) >= 5:.*?generate_slots\(start2, end2\)', new_logic, content, flags=re.DOTALL)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
