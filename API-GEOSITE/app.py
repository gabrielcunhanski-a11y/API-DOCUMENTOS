from flask import Flask
from config.database import db
from routes.userroutes import user_bp
import os

def create_app():
    app = Flask(__name__)
    
    # Configuration
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'geosite.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'sua_chave_secreta_super_segura')

    # Initialize extensions
    db.init_app(app)

    # Register Middlewares
    from middlewares.error_handler import register_error_handlers
    from middlewares.logger import register_logger
    register_error_handlers(app)
    register_logger(app)

    # Register blueprints
    app.register_blueprint(user_bp, url_prefix='/users')

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
