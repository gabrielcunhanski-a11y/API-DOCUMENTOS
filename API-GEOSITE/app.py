import os
from flask import Flask
from config.database import db
from routes.userroutes import user_bp
from routes.citiesroutes import cities_bp
from routes.documentosrotas import documentos_bp
from routes.admroutes import admin_blueprint
from models.user import User
from models.citiesmodel import City
from models.documentosmodels import Documento

def create_app():
    app = Flask(__name__)
    
    # Configurações via variáveis de ambiente para o PostgreSQL da faculdade
    # Exemplo de URI: postgresql://usuario:senha@host:port/database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 
        'postgresql://postgres:postgres@localhost:5432/geocidades'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'sua_chave_secreta_super_segura')

    # Inicializa extensões
    db.init_app(app)

    # Registrar Middlewares
    from middlewares.error_handler import register_error_handlers
    from middlewares.logger import register_logger
    register_error_handlers(app)
    register_logger(app)

    # Registrar Blueprints
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(documentos_bp, url_prefix='/documentos')
    app.register_blueprint(cities_bp, url_prefix='/cities')
    app.register_blueprint(admin_blueprint, url_prefix='/api')

    # Nota: db.create_all() desativado conforme solicitado para não alterar o PostgreSQL remoto.

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
