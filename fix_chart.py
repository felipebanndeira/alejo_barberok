import os
import re

base = r"c:\Users\usser\Documents\Alejo barber"
fin_path = os.path.join(base, "templates/admin/finances.html")

with open(fin_path, "r", encoding="utf-8") as f:
    fin = f.read()

# Fix chart HTML wrapper
old_chart = '<canvas id="incomeChart" height="250"></canvas>'
new_chart = '<div style="position: relative; height: 250px; width: 100%;"><canvas id="incomeChart"></canvas></div>'
fin = fin.replace(old_chart, new_chart)

# Fix JS to add maintainAspectRatio: false
old_js = "plugins: { legend: { display: false } },"
new_js = "maintainAspectRatio: false, responsive: true, plugins: { legend: { display: false } },"
fin = fin.replace(old_js, new_js)

with open(fin_path, "w", encoding="utf-8") as f:
    f.write(fin)
    
print("Chart fixed.")
