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

from functools import wraps

from flask import session, request
from flask_restful import Resource, marshal, reqparse, fields

from ..db import User
from .utils import unauthorized_error, forbidden_error


login_parser = reqparse.RequestParser()
login_parser.add_argument("username", required=True)
login_parser.add_argument("password", required=True)


user_fields = {
    "id":       fields.Integer,
    "username": fields.String,
    "email":    fields.String,
    "is_admin": fields.Boolean,
}


def log_user(username, password):
    user = User.get_user(username=username)
    if not user or not user.check_password(password):
        forbidden_error("Invalid username or password.")

    session["username"] = user.username

    return user


def logged_user():
    if "username" not in session:
        auth = request.authorization
        if auth:
            return log_user(auth["username"], auth["password"])
        return None
    return User.query.filter(User.username == session["username"]).one_or_none()


def with_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = logged_user()
        if user is None:
            unauthorized_error()
        kwargs["user"] = user
        return fn(*args, **kwargs)
    return wrapper


def login_required(as_admin=False):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if "username" not in session or (
                as_admin and not logged_user().is_admin
            ):
                unauthorized_error()
            return fn(*args, **kwargs)
        return wrapper
    return decorator


class LoginApi(Resource):
    def post(self):
        if "username" in session:
            forbidden_error("Already logged in. Please log-out first.")

        args = login_parser.parse_args()

        user = log_user(args["username"], args["password"])

        return {
            "success": True,
            "message": "Successfuly logged as {}.".format(user.username),
            "user": marshal(user, user_fields),
        }


class LogoutApi(Resource):
    def get(self):
        if "username" not in session:
            forbidden_error("Not logged in.")

        session.pop("username")

        return {
            "success": True,
            "message": "Successfuly logged-out.",
        }
