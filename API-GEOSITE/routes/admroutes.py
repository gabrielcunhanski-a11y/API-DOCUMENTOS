from flask import Blueprint
from controllers.admcontroller import AdminController
from middlewares.admmiddleware import admin_required

admin_bp = Blueprint('admin_bp', __name__)

admin_bp.route('/dashboard', methods=['GET'])(admin_required(AdminController.get_dashboard))
admin_bp.route('/promote/<int:user_id>', methods=['PATCH'])(admin_required(AdminController.promote_user))
