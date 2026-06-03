from models.user import User
from config.database import db
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import jwt
import datetime
from flask import current_app

ph = PasswordHasher()

class UserService:
    @staticmethod
    def create_user(username, email, password, course, role):
        password_hash = ph.hash(password)
        new_user = User(
            username=username, 
            email=email, 
            password_hash=password_hash,
            course=course,
            role=role
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def generate_token(user):
        payload = {
            'user_id': user.id,
            'role': user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def update_user(user_id, data):
        user = User.query.get(user_id)
        if not user:
            return None
        
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'course' in data:
            user.course = data['course']
        if 'role' in data:
            user.role = data['role']
        if 'password' in data:
            user.password_hash = ph.hash(data['password'])
            
        db.session.commit()
        return user

    @staticmethod
    def set_user_active_status(user_id, status):
        user = User.query.get(user_id)
        if not user:
            return None
        
        user.is_active = status
        db.session.commit()
        return user

    @staticmethod
    def verify_password(user, password):
        try:
            return ph.verify(user.password_hash, password)
        except VerifyMismatchError:
            return False
