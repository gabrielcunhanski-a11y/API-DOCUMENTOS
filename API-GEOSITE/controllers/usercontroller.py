from flask import request, jsonify
from services.userservice import UserService

class UserController:
    @staticmethod
    def register():
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Bad Request", "message": "No JSON data provided"}), 400
            
        required_fields = ['username', 'email', 'password', 'course', 'role']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return jsonify({
                "error": "Missing required fields", 
                "missing": missing_fields
            }), 400
        
        if data['role'] not in ['aluno', 'professor']:
            return jsonify({"error": "Invalid role", "message": "Role must be 'aluno' or 'professor'"}), 400

        try:
            user = UserService.create_user(
                data['username'], 
                data['email'], 
                data['password'],
                data['course'],
                data['role']
            )
            return jsonify({
                "message": "User created successfully", 
                "user": user.to_dict()
            }), 201
        except Exception as e:
            # Captura erros como email já existente (Unique constraint)
            error_msg = str(e)
            if "UNIQUE constraint failed" in error_msg:
                return jsonify({"error": "Conflict", "message": "Username or Email already exists"}), 409
            return jsonify({"error": "Internal Error", "message": error_msg}), 400

    @staticmethod
    def login():
        data = request.get_json()
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({"error": "Missing email or password"}), 400

        user = UserService.get_user_by_email(data['email'])
        if user and UserService.verify_password(user, data['password']):
            token = UserService.generate_token(user)
            return jsonify({
                "message": "Login successful", 
                "token": token,
                "user": user.to_dict()
            }), 200
        
        return jsonify({"error": "Invalid credentials"}), 401

    @staticmethod
    def get_me():
        user_id = getattr(request, 'user_id', None)
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401
            
        user = UserService.get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        return jsonify(user.to_dict()), 200

    @staticmethod
    def update_me():
        user_id = getattr(request, 'user_id', None)
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401
            
        data = request.get_json()
        try:
            user = UserService.update_user(user_id, data)
            if not user:
                return jsonify({"error": "User not found"}), 404
                
            return jsonify({
                "message": "User updated successfully",
                "user": user.to_dict()
            }), 200
        except Exception as e:
            error_msg = str(e)
            if "UNIQUE constraint failed" in error_msg:
                return jsonify({"error": "Conflict", "message": "Username or Email already exists"}), 409
            return jsonify({"error": "Internal Error", "message": error_msg}), 400

    @staticmethod
    def get_all_users():
        users = UserService.get_all_users()
        return jsonify([user.to_dict() for user in users]), 200

    @staticmethod
    def get_user_by_id(user_id):
        user = UserService.get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user.to_dict()), 200

    @staticmethod
    def update_user(user_id):
        data = request.get_json()
        try:
            user = UserService.update_user(user_id, data)
            if not user:
                return jsonify({"error": "User not found"}), 404
            return jsonify({
                "message": "User updated successfully",
                "user": user.to_dict()
            }), 200
        except Exception as e:
            error_msg = str(e)
            if "UNIQUE constraint failed" in error_msg:
                return jsonify({"error": "Conflict", "message": "Username or Email already exists"}), 409
            return jsonify({"error": "Internal Error", "message": error_msg}), 400

    @staticmethod
    def deactivate_user(user_id):
        user = UserService.set_user_active_status(user_id, False)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify({
            "message": "User deactivated successfully",
            "user": user.to_dict()
        }), 200

    @staticmethod
    def activate_user(user_id):
        user = UserService.set_user_active_status(user_id, True)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify({
            "message": "User activated successfully",
            "user": user.to_dict()
        }), 200
