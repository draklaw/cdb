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

from typing import List, Union
from pydantic import BaseModel

from sqlalchemy import (
    select, and_, or_,
    ForeignKey, PrimaryKeyConstraint, UniqueConstraint,
)
from databases import Database

from .schema import Field, create_table
from .error import convert_error, ForbiddenError
from .user import users, UserDb, get_user_query
from .utils import raise_if_all_none


class CollectionIn(BaseModel):
    """A collection without id, suitable for creation."""

    name: str = Field(..., index=True)
    title: str = ...
    public: bool = False


class CollectionCreate(CollectionIn):
    """A collection without id, suitable for creation."""

    owner: int = Field(..., ForeignKey("users.id"), index=True)


class CollectionDb(CollectionCreate):
    """A collection as stored in the DB.
    """

    id: int = Field(..., primary_key=True)
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

    @classmethod
    def from_row(cls, user, row):
        col_dict = dict(**row)

        if col_dict["user_id"] is None:
            col_dict["user_id"] = user.id
            col_dict["can_edit"] = user.is_admin

        return Collection(**col_dict)

    @classmethod
    def wrapper(cls, user):
        return lambda row: cls.from_row(user, row)


class CollectionUpdate(CollectionIn):
    id: int


collections = create_table("collections", CollectionDb)
user_collections = create_table("user_collections", UserCollection)


@convert_error
async def create_collection(
    database: Database,
    collection: Union[CollectionCreate, CollectionDb],
) -> CollectionDb:
    """Creates a collection, returns it."""

    params = collection.dict(exclude={"id"})
    params.setdefault("deleted", False)

    id = await database.execute(collections.insert(), params)

    await link_user_to_collection(
        database,
        collection.owner,
        id,
    )

    return CollectionDb(
        id = id,
        **params,
    )


async def link_user_to_collection(
    database: Database,
    user_id = int,
    collection_id = int,
    can_edit = True,
) -> int:
    return await database.execute(
        user_collections.insert(),
        dict(
            user_id = user_id,
            collection_id = collection_id,
            can_edit = can_edit,
        ),
    )


def get_user_collections_query(
    user: UserDb,
    *,
    user_id: int = None,
    username: str = None,
    collection_name: str = None,
    only_owned: bool = True,
    include_deleted: bool = False,
):
    raise_if_all_none(user_id=user_id, username=username)

    tgt_user = get_user_query(
        user_id = user_id,
        username = username,
        include_disabled = user.is_admin,
    ).with_only_columns([users.c.id]).alias()

    query = (
        select([collections, user_collections])
        .select_from(
            collections.outerjoin(
                user_collections,
                and_(
                    collections.c.id == user_collections.c.collection_id,
                    user_collections.c.user_id == user.id,
                )
            )
        )
    )

    if not user.is_admin:
        query = query.where(
            or_(
                tgt_user.c.id == user.id,
                collections.c.public,
                user_collections.c.user_id != None,
            )
        )

    if collection_name is not None:
        query = query.where(collections.c.name == collection_name)

    if only_owned:
        query = query.where(collections.c.owner == tgt_user.c.id)
    else:
        query = query.where(user_collections.c.user_id == tgt_user.c.id)

    if not include_deleted:
        query = query.where(~collections.c.deleted)

    return query


async def get_collection(
    database: Database,
    user: UserDb,
    *,
    user_id: int = None,
    username: str = None,
    collection_name: str,
    only_owned: bool = True,
    include_deleted: bool = False,
) -> Collection:

    query = get_user_collections_query(
        user,
        user_id = user_id,
        username = username,
        collection_name = collection_name,
        only_owned = only_owned,
        include_deleted = include_deleted,
    )

    return await database.one(query, Collection.wrapper(user))


async def get_collections(
    database: Database,
    user: UserDb,
    *,
    user_id: int = None,
    username: str = None,
    only_owned: bool = True,
    include_deleted: bool = False,
    order_by_title: bool = True,
) -> List[Collection]:

    query = get_user_collections_query(
        user,
        user_id = user_id,
        username = username,
        only_owned = only_owned,
        include_deleted = include_deleted,
    )

    if order_by_title:
        query = query.order_by(collections.c.title)

    return await database.all(query, Collection.wrapper(user))


def update_collection_query(
    database: Database,
    user: UserDb,
    *,
    user_id: int = None,
    username: str = None,
    collection_name: str,
):
    col = (
        get_user_collections_query(
            user,
            user_id = user_id,
            username = username,
            collection_name = collection_name,
        )
        .with_only_columns([collections.c.id, user_collections.c.can_edit])
        .alias()
    )

    return (
        collections.update()
        .returning(collections.c.id)
        .where(collections.c.id == col.c.id)
        .where(col.c.can_edit)
    )


async def update_collection(
    database: Database,
    user: UserDb,
    *,
    value: CollectionIn,
    user_id: int = None,
    username: str = None,
    collection_name: str,
):
    query = (
        update_collection_query(
            database,
            user,
            user_id = user_id,
            username = username,
            collection_name = collection_name,
        )
        .values(**value.dict(include={"name", "title", "public"}))
    )

    await database.one(query)


async def delete_collection(
    database: Database,
    user: UserDb,
    *,
    user_id: int = None,
    username: str = None,
    collection_name: str,
):
    if not user.is_admin and (
        (user_id is not None and user_id != user.id)
        or (username is not None and username != user.username)
    ):
        raise ForbiddenError("Collections can only be deleted by their owners")

    query = (
        update_collection_query(
            database,
            user,
            user_id = user_id,
            username = username,
            collection_name = collection_name,
        )
        .values(deleted=True)
    )

    await database.one(query)
