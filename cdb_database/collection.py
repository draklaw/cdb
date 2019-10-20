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

from typing import Union
from pydantic import BaseModel

from sqlalchemy import (
    select,
    Integer, Unicode,
    ForeignKey, PrimaryKeyConstraint, UniqueConstraint, bindparam,
)
from databases import Database

from .schema import Field, create_table
from .error import NotFoundError
from .query import Query
from .user import user


class CollectionCreate(BaseModel):
    """A collection without id, suitable for creation."""

    name: str = Field(..., index=True)
    title: str = ...
    public: bool = False


class CollectionDb(CollectionCreate):
    """A collection as stored in the DB.
    """

    id: int = Field(..., primary_key=True)
    owner: int = Field(..., ForeignKey("users.id"), index=True)
    deleted: bool = False

    class Config:
        sql_alchemy = [
            UniqueConstraint("owner", "name"),
        ]


class UserCollection(BaseModel):
    """The link between a user and a collection."""

    user_id: int = Field(..., ForeignKey("users.id"), index=True)
    collection_id: int = Field(..., ForeignKey("collections.id"), index=True)
    can_edit: bool = True

    class Config:
        sql_alchemy = [
            PrimaryKeyConstraint("user_id", "collection_id"),
        ]


class Collection(CollectionDb):
    """A collection along with info related to a user (rw rights, etc.)"""

    id: int = ...
    user_id: int = ...
    can_edit: bool = True


collection = create_table("collections", CollectionDb)
user_collection = create_table("user_collections", UserCollection)


# _id = bindparam("id", type_=Unicode)
# _name = bindparam("name", type_=Unicode)
# _user_id = bindparam("user_id", type_=Integer)
# _username = bindparam("username", type_=Integer)

# _user_id_by_username = (
#     user.select(user.c.id)
#     .where(user.c.username == _username)
#     .alias()
# )

_create_collection = collection.insert()
_create_user_collection = user_collection.insert()


def user_id_expr(*, user_id: int = None, username: str = None):
    if int(user_id is not None) + int(username is not None) != 1:
        raise TypeError("user_id_exp: either user_id or username must be set")

    if user_id is not None:
        return user_id
    else:
        return (
            select([user.c.id])
            .where(user.c.username == username)
            .alias()
        )



class CollectionQuery(Query):
    def __init__(
        self,
        database: Database,
        *,
        user_id: int = None,
        username: str = None,
        include_deleted = False,
    ):
        super().__init__(
            database,
            user_collection,
            collection,
            wrapper = Collection,
        )

        self._include_deleted = include_deleted

        self.where(user_collection.c.collection_id == collection.c.id)

        user_expr = user_id_expr(user_id=user_id, username=username)
        self.where(user_collection.c.user_id == user_expr)

    def query(self):
        query = super().query()
        if not self._include_deleted:
            query = query.where(~collection.c.deleted)
        return query

    def only_owned(self):
        return self.where(user_collection.c.user_id == collection.c.owner)

    def only_public(self) -> "CollectionQuery":
        return self.where(collection.c.public)

    def include_deleted(self) -> "CollectionQuery":
        self._include_deleted = True
        return self

    def with_id(self, id: int) -> "CollectionQuery":
        return self.where(collection.c.id == id)

    def with_name(self, name: str) -> "CollectionQuery":
        return self.where(collection.c.name == name)

    def order_by_title(self) -> "CollectionQuery":
        return self.order_by(collection.c.title)


async def create_collection(
    database: Database,
    user_id: int,
    collection: CollectionCreate,
) -> int:
    """Creates a collection, returns its id."""

    id = await database.execute(
        _create_collection,
        dict(
            **collection.dict(),
            owner = user_id,
        ),
    )

    await link_user_to_collection(
        database,
        collection.owner,
        id,
    )

    return id


async def create_collections(
    database: Database,
    *collections: CollectionDb,
):
    await database.execute_many(
        _create_collection,
        [collection.dict() for collection in collections],
    )
    await database.execute_many(
        _create_user_collection,
        [
            dict(
                user_id = collection.owner,
                collection_id = collection.id,
                can_edit = True,
            )
            for collection in collections
        ],
    )


async def link_user_to_collection(
    database: Database,
    user_id = int,
    collection_id = int,
    can_edit = True,
) -> int:
    return await database.execute(
        _create_user_collection,
        dict(
            user_id = user_id,
            collection_id = collection_id,
            can_edit = can_edit,
        ),
    )


async def get_collection(database: Database, *, id: int) -> CollectionDb:
    query = Query(database, collection, wrapper=CollectionDb)
    return await query.where(collection.c.id == id).one()
