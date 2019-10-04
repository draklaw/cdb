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
