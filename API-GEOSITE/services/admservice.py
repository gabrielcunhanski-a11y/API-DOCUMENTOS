from config.database import db
from models.citymodel import City
from models.documentomodel import Documento
from models.usermodel import User

class AdminService:
    @staticmethod
    def get_dashboard_stats():
        return {
            "total_users": User.query.count(),
            "total_documents": Documento.query.count(),
            "total_cities": City.query.count()
        }

    @staticmethod
    def promote_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return None
        
        user.role = 'admin'
        db.session.commit()
        return user
