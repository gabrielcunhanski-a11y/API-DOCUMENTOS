from flask import Blueprint
from controllers.usercontroller import UserController

user_bp = Blueprint('user_bp', __name__)

user_bp.route('/register', methods=['POST'])(UserController.register)
user_bp.route('/login', methods=['POST'])(UserController.login)
