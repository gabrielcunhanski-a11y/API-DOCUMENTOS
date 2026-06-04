from flask import request, jsonify
from functools import wraps
from middlewares.auth import auth_required

def admin_required(f):
    """
    Middleware que exige que o usuário esteja autenticado E tenha role 'admin'.
    O @auth_required já decodifica o token e injeta request.user_role.
    """
    @auth_required
    @wraps(f)
    def decorated(*args, **kwargs):
        user_role = getattr(request, 'user_role', None)

        if user_role != 'admin':
            return jsonify({
                "error": "Forbidden", 
                "message": "Acesso restrito a administradores."
            }), 403
            
        return f(*args, **kwargs)
    return decorated