from flask import Blueprint
from controllers.authcontroller import PasswordResetController

auth_bp = Blueprint('auth_bp', __name__)

# 1. Rota onde o usuário digita o e-mail na tela de esqueci a senha
auth_bp.route('/forgot-password', methods=['POST'])(PasswordResetController.request_reset)

# 2. Rota onde o front-end envia o Token da URL + a Nova Senha digitada
auth_bp.route('/reset-password', methods=['POST'])(PasswordResetController.execute_reset)
