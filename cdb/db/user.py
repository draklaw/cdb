# This file is part of cdb.
#
# Copyright (C) 2019  the authors (see AUTHORS)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
