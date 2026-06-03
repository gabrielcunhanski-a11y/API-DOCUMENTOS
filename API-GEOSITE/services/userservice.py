from models.user import User
from config.database import db
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

class UserService:
    @staticmethod
    def create_user(username, email, password):
        password_hash = ph.hash(password)
        new_user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def verify_password(user, password):
        try:
            return ph.verify(user.password_hash, password)
        except VerifyMismatchError:
            return False
