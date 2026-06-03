from flask import request, jsonify
from services.userservice import UserService

class UserController:
    @staticmethod
    def register():
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Bad Request", "message": "No JSON data provided"}), 400
            
        required_fields = ['username', 'email', 'password']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return jsonify({
                "error": "Missing required fields", 
                "missing": missing_fields
            }), 400
        
        try:
            user = UserService.create_user(data['username'], data['email'], data['password'])
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
            return jsonify({
                "message": "Login successful", 
                "user": user.to_dict()
            }), 200
        
        return jsonify({"error": "Invalid credentials"}), 401
