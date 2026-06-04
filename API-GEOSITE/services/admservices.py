from config.database import db
from models.citiesmodel import City
from models.documentosmodels import Documento
from models.user import User


class AdminService:
    @staticmethod
    def get_dashboard_stats():
        total_cities = City.query.count()
        total_documents = Documento.query.count()
        total_users = User.query.count()

        return {
            "total_cities": total_cities,
            "total_documents": total_documents,
            "total_users": total_users
        }

    @staticmethod
    def promote_user_to_admin(target_user_id):
        user = User.query.get(target_user_id)
        if not user:
            return None, "User not found"

        user.role = 'admin'
        db.session.commit()
        return user, "User promoted to admin successfully"