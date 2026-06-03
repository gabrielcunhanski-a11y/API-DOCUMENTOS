from flask import Blueprint
from controllers.usercontroller import UserController
from middlewares.auth import auth_required

user_bp = Blueprint('user_bp', __name__)

user_bp.route('/register', methods=['POST'])(UserController.register)
user_bp.route('/login', methods=['POST'])(UserController.login)

# Rotas do próprio usuário
user_bp.route('/me', methods=['GET'])(auth_required(UserController.get_me))
user_bp.route('/me', methods=['PUT'])(auth_required(UserController.update_me))

# Rotas de gerenciamento de usuários
user_bp.route('/', methods=['GET'])(auth_required(UserController.get_all_users))
user_bp.route('/<int:user_id>', methods=['GET'])(auth_required(UserController.get_user_by_id))
user_bp.route('/<int:user_id>', methods=['PUT'])(auth_required(UserController.update_user))
user_bp.route('/<int:user_id>/deactivate', methods=['PATCH'])(auth_required(UserController.deactivate_user))
user_bp.route('/<int:user_id>/activate', methods=['PATCH'])(auth_required(UserController.activate_user))
