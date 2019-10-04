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
