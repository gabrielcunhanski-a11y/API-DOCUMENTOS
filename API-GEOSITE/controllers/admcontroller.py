from flask import jsonify
from services.admservices import AdminService


class AdminController:
    @staticmethod
    def get_dashboard():
        stats = AdminService.get_dashboard_stats()
        return jsonify({"status": "success", "data": stats}), 200

    @staticmethod
    def promote_user(user_id):
        user, message = AdminService.promote_user_to_admin(user_id)
        if not user:
            return jsonify({"status": "error", "message": message}), 404

        return jsonify({
            "status": "success",
            "message": f"Usuário {user.username} promovido a Admin",
            "data": user.to_dict()
        }), 200