import os

base = r"c:\Users\usser\Documents\Alejo barber"
dash_path = os.path.join(base, "templates/admin/dashboard.html")

with open(dash_path, "r", encoding="utf-8") as f:
    dash = f.read()

# Let's count how many times mobile-only mb-2 appears
print("mobile-only count:", dash.count('<div class="mobile-only mb-2">'))

# Let's count how many times endfor appears
print("endfor count:", dash.count('{% endfor %}'))

# Let's count how many times for appears
print("for count:", dash.count('{% for '))

