from flask import Flask, g
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
