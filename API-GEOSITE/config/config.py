import os
from urllib.parse import quote_plus

class Config:
    # Configurações de Banco de Dados
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = quote_plus(os.environ.get('DB_PASSWORD', 'sua_senha_com_ç'))
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '5432')
    DB_NAME = os.environ.get('DB_NAME', 'geocidades')

    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    SECRET_KEY = os.environ.get('SECRET_KEY', 'sua_chave_secreta_super_segura')
