from sqlalchemy.ext.associationproxy import association_proxy

from .db import db
from .user import User
from .item import Item
from .collection import Collection
from .user_collection import UserCollection


User.owned_collections = db.relationship(Collection, back_populates="owner")
User.user_collections = db.relationship(UserCollection, back_populates="user")
User.collections = association_proxy("user_collections", "collection")

Collection.owner = db.relationship(User, back_populates="owned_collections")
Collection.user_collections = db.relationship(UserCollection, back_populates="collection")
Collection.users = association_proxy("user_collections", "user")
Collection.items = db.relationship(Item, back_populates="collection")

UserCollection.user = db.relationship(User, back_populates="user_collections")
UserCollection.collection = db.relationship(Collection, back_populates="user_collections")

Item.collection = db.relationship(Collection, back_populates="items")


def query_collections_from_user(user_id):
    return (
        db.query(Collection, UserCollection)
            .filter(UserCollection.user_id == user_id)
    )
