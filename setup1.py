import os

base = r"c:\Users\usser\Documents\Alejo barber"

files = {
    "config.py": '''import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-alejo-barber'
    DATABASE = os.path.join(os.path.dirname(__file__), 'barber.db')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'img')
''',
    "app.py": '''from flask import Flask, g
from config import Config
from core.db import init_db, close_db
from routes.cliente_routes import cliente_bp
from routes.admin_routes import admin_bp

app = Flask(__name__)
app.config.from_object(Config)

@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)

with app.app_context():
    init_db()

app.register_blueprint(cliente_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')

if __name__ == '__main__':
    app.run(debug=True)
''',
    r"core\db.py": '''import sqlite3
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    
    db.execute(\'\'\'
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    \'\'\')
    
    db.execute(\'\'\'
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            duration INTEGER NOT NULL
        )
    \'\'\')
    
    db.execute(\'\'\'
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            client_phone TEXT NOT NULL,
            service_id INTEGER,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY (service_id) REFERENCES services (id)
        )
    \'\'\')

    db.execute(\'\'\'
        CREATE TABLE IF NOT EXISTS blocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            date TEXT,
            day_of_week INTEGER,
            start_time TEXT,
            end_time TEXT
        )
    \'\'\')
    
    db.execute(\'\'\'
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    \'\'\')
    
    if db.execute('SELECT COUNT(*) FROM services').fetchone()[0] == 0:
        db.execute("INSERT INTO services (name, price, duration) VALUES ('Corte', 10000, 30)")
        db.execute("INSERT INTO services (name, price, duration) VALUES ('Barba', 4000, 30)")
        db.execute("INSERT INTO services (name, price, duration) VALUES ('Corte y barba', 12000, 30)")
        
    if db.execute('SELECT COUNT(*) FROM settings').fetchone()[0] == 0:
        settings = [
            ('barber_name', 'Alejo Barber'),
            ('whatsapp', '123456789'),
            ('deposit_percentage', '50'),
            ('bank_details', 'CBU: 0000000000000000000000\\nAlias: alejo.barber'),
            ('hours_mon_fri_start_1', '10:30'),
            ('hours_mon_fri_end_1', '13:00'),
            ('hours_mon_fri_start_2', '16:30'),
            ('hours_mon_fri_end_2', '21:00')
        ]
        db.executemany("INSERT INTO settings (key, value) VALUES (?, ?)", settings)

    from werkzeug.security import generate_password_hash
    if db.execute('SELECT COUNT(*) FROM users').fetchone()[0] == 0:
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                   ('admin', generate_password_hash('admin')))

    db.commit()
''',
    r"core\auth.py": '''from functools import wraps
from flask import session, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function
''',
    r"routes\__init__.py": '''# Routes package
'''
}

for path, content in files.items():
    full_path = os.path.join(base, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
