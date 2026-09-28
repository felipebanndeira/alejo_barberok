from datetime import datetime, timedelta
from core.db import get_db

def get_available_times(date_str):
    db = get_db()
    
    # 1. Get Settings for hours
    settings = dict(db.execute('SELECT key, value FROM settings').fetchall())
    
    # Check if weekend (Mon=0, Sun=6)
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    # Si es domingo (6), cerrado
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

    # Si es sábado (5)
    if date_obj.weekday() == 5:
        sat_start = settings.get('hours_sat_start', '09:00')
        sat_end = settings.get('hours_sat_end', '13:30')
        generate_slots(sat_start, sat_end)
    else:
        # Lunes a viernes
        start1 = settings.get('hours_mon_fri_start_1', '10:30')
        end1 = settings.get('hours_mon_fri_end_1', '13:30')
        start2 = settings.get('hours_mon_fri_start_2', '16:30')
        end2 = settings.get('hours_mon_fri_end_2', '21:30')
        generate_slots(start1, end1)
        generate_slots(start2, end2)
    
    # 3. Filter past times if it's today
    now = datetime.now()
    if date_obj.date() == now.date():
        current_time_str = now.strftime('%H:%M')
        slots = [s for s in slots if s > current_time_str]
        
    # 4. Remove blocks (Specific date or recurring day_of_week)
    blocks = db.execute(
        "SELECT start_time, end_time FROM blocks WHERE (type='date' AND date=%s) OR (type='recurring' AND day_of_week=%s)",
        (date_str, date_obj.weekday())
    ).fetchall()
    
    for b in blocks:
        bs_time = b['start_time']
        be_time = b['end_time']
        # Remove any slot that falls inside the block
        slots = [s for s in slots if not (bs_time <= s < be_time)]
        
    # 5. Remove already booked appointments
    appointments = db.execute(
        "SELECT time FROM appointments WHERE date=%s AND status != 'cancelled'",
        (date_str,)
    ).fetchall()
    
    booked_times = [a['time'] for a in appointments]
    
    # Return objects instead of strings
    result = []
    for s in slots:
        if s in booked_times:
            result.append({"time": s, "available": False})
        else:
            result.append({"time": s, "available": True})
            
    return result
