import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-alejo-barber'
    DATABASE = os.path.join(os.path.dirname(__file__), 'barber.db')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'img')
