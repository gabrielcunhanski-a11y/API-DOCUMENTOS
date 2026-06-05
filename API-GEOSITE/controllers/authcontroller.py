from flask import request, jsonify
from services.authservice import PasswordResetService

class PasswordResetController:
    @staticmethod
    def request_reset():
        data = request.get_json()
        if not data or not data.get('email'):
            return jsonify({"error": "Bad Request", "message": "Email is required"}), 400
        
        token = PasswordResetService.generate_reset_token(data['email'])
        
        # Em um sistema real, aqui enviaríamos um e-mail. 
        # Como é uma API de exemplo/estudo, retornaremos o token no JSON.
        if token:
            return jsonify({
                "message": "Reset token generated successfully",
                "token": token
            }), 200
        
        # Mesmo que o e-mail não exista, por segurança, costuma-se retornar 200 ou 202.
        # Mas aqui retornaremos 404 para facilitar o debug do usuário.
        return jsonify({"error": "Not Found", "message": "User not found"}), 404

    @staticmethod
    def execute_reset():
        data = request.get_json()
        if not data or not data.get('token') or not data.get('new_password'):
            return jsonify({"error": "Bad Request", "message": "Token and new_password are required"}), 400
        
        try:
            PasswordResetService.reset_password(data['token'], data['new_password'])
            return jsonify({"message": "Password reset successfully"}), 200
        except ValueError as e:
            return jsonify({"error": "Unprocessable Entity", "message": str(e)}), 422
        except Exception as e:
            return jsonify({"error": "Internal Error", "message": str(e)}), 500
