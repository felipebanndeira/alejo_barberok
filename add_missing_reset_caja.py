import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "routes/admin_routes.py")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Make sure reset_caja isn't already there
if "def reset_caja():" not in content:
    reset_route = """
@admin_bp.route('/reset_caja', methods=['POST'])
@login_required
def reset_caja():
    db = get_db()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('last_reset_date', ?)", (now,))
    db.commit()
    return redirect(request.referrer or url_for('admin.finances'))
"""
    content += reset_route
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
        print("Route added.")
else:
    print("Route already exists.")
