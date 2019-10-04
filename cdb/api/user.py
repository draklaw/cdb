from flask_restful import Resource, fields, marshal

from ..db import User
from .utils import unauthorized_error
from .login import with_user

user_fields = {
    "id":       fields.Integer,
    "username": fields.String,
    "email":    fields.String,
    "is_admin": fields.Boolean,
}


class UserApi(Resource):
    @with_user
    def get(self, user, username=None):
        if username is None:
            if user.is_admin:
                return {
                    "success": True,
                    "users": marshal(User.get_user_list(), user_fields),
                }
            else:
                unauthorized_error()
        else:
            if user.is_admin or username == user.username:
                return {
                    "success": True,
                    "users": marshal(user, user_fields),
                }
            else:
                unauthorized_error()
