import os
from flask import Flask, send_from_directory
from config.database import db
from config.config import Config
from routes.userroutes import user_bp
from routes.citiesroutes import cities_bp
from routes.documentosroutes import documentos_bp
from routes.admroutes import admin_bp
from routes.authroutes import auth_bp
from models.usermodel import User
from models.citymodel import City
from models.documentomodel import Documento

def create_app():
    app = Flask(__name__)
    
    # Aplicar configurações do arquivo config.py
    app.config.from_object(Config)
    
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
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Rota para servir arquivos estáticos (uploads)
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
