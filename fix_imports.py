import os

base = r"c:\Users\usser\Documents\Alejo barber"
path = os.path.join(base, "routes/cliente_routes.py")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("from flask import Blueprint, render_template, request, jsonify", "from flask import Blueprint, render_template, request, jsonify, redirect, url_for")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
