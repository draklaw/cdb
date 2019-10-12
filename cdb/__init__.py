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
