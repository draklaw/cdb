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

from ..db import db, User, Collection, UserCollection
from .utils import unauthorized_error, bad_request_error
from .login import with_user

collection_fields = {
    "id":       fields.Integer(attribute="collection.id"),
    "name":     fields.String(attribute="collection.name"),
    "label":    fields.String(attribute="collection.label"),
    "is_admin": fields.Boolean(attribute="is_admin"),
}


class CollectionApi(Resource):
    @with_user
    def get(self, user, username, col_name=None):
        if col_name is None:
            user_collections = (db.session.query(UserCollection)
                .join(UserCollection.collection)
                .join(Collection.owner)
                .options(
                    db.contains_eager(UserCollection.collection),
                )
                .filter(UserCollection.user_id == user.id)
                .filter(Collection.owner_id == User.id)
                .filter(User.username == username)
                .order_by(Collection.label)
                .all()
            )

            return {
                "success": True,
                "collections": marshal(user_collections, collection_fields),
            }
        else:
            user_collection = (db.session.query(UserCollection)
                .join(UserCollection.collection)
                .join(Collection.owner)
                .options(
                    db.contains_eager(UserCollection.collection),
                )
                .filter(UserCollection.user_id == user.id)
                .filter(Collection.owner_id == User.id)
                .filter(User.username == username)
                .filter(Collection.name == col_name)
                .one()
            )

            return {
                "success": True,
                "collection": marshal(user_collection, collection_fields),
            }
