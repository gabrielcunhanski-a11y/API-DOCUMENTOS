from functools import wraps
from flask import request, jsonify, current_app
import jwt

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({"error": "Unauthorized", "message": "Missing Authorization header"}), 401
        
        try:
            # Espera formato "Bearer <token>"
            token = auth_header.split(" ")[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            # Você pode injetar o user_id no request se precisar
            request.user_id = data['user_id']
            request.user_role = data['role']
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Unauthorized", "message": "Token has expired"}), 401
        except (jwt.InvalidTokenError, IndexError):
            return jsonify({"error": "Unauthorized", "message": "Invalid token"}), 401
            
        return f(*args, **kwargs)
    return decorated
