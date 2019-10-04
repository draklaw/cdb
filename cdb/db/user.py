from werkzeug.security import generate_password_hash, check_password_hash

from .db import db


class Rights:
    def __init__(self, admin = False):
        self.admin = False


class User(db.Model):
    id       = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique=True, index=True, nullable=False)
    email    = db.Column(db.String, unique=True, index=True, nullable=False)
    password = db.Column(db.String)
    is_admin = db.Column(db.Boolean)

#    collections = association_proxy("user_collection", "collection")

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User {id} {username}>".format(**self.__dict__)

    @staticmethod
    def _user_filter(id=None, username=None, email=None):
        if id is not None:
            return User.id == id
        elif username is not None:
            return User.username == username
        elif email is not None:
            return User.email == email
        else:
            raise ValueError("One argument must be set.")

    @staticmethod
    def has_user(id=None, username=None, email=None):
        if id is not None:
            return User.query.get(id) is not None
        return User.query.filter(User._user_filter(id, username, email)).count() != 0

    @staticmethod
    def get_user(id=None, username=None, email=None):
        if id is not None:
            return User.query.get(id)
        return User.query.filter(User._user_filter(id, username, email)).one_or_none()

    @staticmethod
    def get_user_list():
        return User.query.all()

    @staticmethod
    def create_user(username, password, email, is_admin=False):
        return User(
            username = username,
            password = generate_password_hash(password),
            email    = email,
            is_admin = is_admin,
        )

    @staticmethod
    def delete_user(id=None, username=None, email=None):
        user = User.get_user(id, username, email)
        if not User:
            raise RuntimeError("User not found.")

        db.session.delete(user)
        db.session.commit()
