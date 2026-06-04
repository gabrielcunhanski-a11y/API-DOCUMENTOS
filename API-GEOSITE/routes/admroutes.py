from flask import Blueprint
from controllers.admcontroller import AdminController
from middlewares.admmiddleware import admin_required

admin_blueprint = Blueprint('admin_blueprint', __name__)


admin_blueprint.route('/admin/dashboard', methods=['GET'])(admin_required(AdminController.get_dashboard))


admin_blueprint.route('/admin/promote/<int:user_id>', methods=['PATCH'])(admin_required(AdminController.promote_user))