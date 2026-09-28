import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "routes/admin_routes.py")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Update update_status
old_status = """def update_status(id):
    status = request.form['status']
    payment_method = request.form.get('payment_method', 'efectivo')
    db = get_db()
    db.execute("UPDATE appointments SET status = ?, payment_method = ? WHERE id = ?", (status, payment_method, id))"""

new_status = """def update_status(id):
    status = request.form['status']
    payment_method = request.form.get('payment_method', 'efectivo')
    db = get_db()
    if status == 'confirmed':
        db.execute("UPDATE appointments SET status = ?, payment_method = ?, confirmed_at = CURRENT_TIMESTAMP WHERE id = ?", (status, payment_method, id))
    else:
        db.execute("UPDATE appointments SET status = ?, payment_method = ? WHERE id = ?", (status, payment_method, id))"""
content = content.replace(old_status, new_status)

# Now we replace the a.date || a.time logic across the board.
# Search pattern: WHERE (a.date || ' ' || a.time || ':00') >= ? AND (a.date || ' ' || a.time || ':00') <= ?
# We can replace all of it! Let's just use simple text replacement for the ones we added earlier.
content = content.replace("(a.date || ' ' || a.time || ':00') >= ? AND (a.date || ' ' || a.time || ':00') <= ?", "datetime(a.confirmed_at, 'localtime') >= ? AND datetime(a.confirmed_at, 'localtime') <= ?")

# Also the ones in the charts and monthly box that didn't have the <= today bound
content = content.replace("(a.date || ' ' || a.time || ':00') >= ?", "datetime(a.confirmed_at, 'localtime') >= ?")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
