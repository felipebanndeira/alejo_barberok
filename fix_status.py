import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "routes/admin_routes.py")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_status = """def update_status(id):
    status = request.form['status']
    db = get_db()
    db.execute("UPDATE appointments SET status = ? WHERE id = ?", (status, id))"""

new_status = """def update_status(id):
    status = request.form['status']
    payment_method = request.form.get('payment_method', 'efectivo')
    db = get_db()
    db.execute("UPDATE appointments SET status = ?, payment_method = ? WHERE id = ?", (status, payment_method, id))"""

content = content.replace(old_status, new_status)
with open(path, "w", encoding="utf-8") as f:
    f.write(content)
