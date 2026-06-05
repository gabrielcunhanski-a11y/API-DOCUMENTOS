import datetime
import jwt
from flask import current_app
from config.database import db
from argon2 import PasswordHasher
from models.usermodel import User

ph = PasswordHasher()

class PasswordResetService:
    @staticmethod
    def generate_reset_token(email):
        """Gera um token JWT seguro para recuperação de senha com validade de 15 minutos."""
        user = User.query.filter_by(email=email).first()
        if not user:
            return None

        payload = {
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=15),
            'iat': datetime.datetime.now(datetime.timezone.utc),
            'user_id': user.id,
            'type': 'password_reset'
        }

        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_token(token):
        """
        Valida o token recebido e retorna o usuário correspondente.
        Levanta erros específicos caso o token seja inválido ou tenha expirado.
        """
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])

            if payload.get('type') != 'password_reset':
                raise ValueError('Este token não é válido para recuperação de senha.')

            user_id = payload.get('user_id')
            user = User.query.get(user_id)
            if not user:
                raise ValueError('Usuário associado a este token não foi encontrado.')

            return user

        except jwt.ExpiredSignatureError:
            raise ValueError('O link de recuperação expirou! Solicite um novo link.')
        except jwt.InvalidTokenError:
            raise ValueError('O link de recuperação é inválido ou está corrompido.')

    @staticmethod
    def reset_password(token, new_password):
        user = PasswordResetService.verify_reset_token(token)
        user.password_hash = ph.hash(new_password)
        db.session.commit()
        return user
