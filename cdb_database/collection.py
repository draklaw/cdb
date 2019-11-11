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
)
from databases import Database

from .tables import (
    UserDb, CollectionDb,
    users, collections, user_collections,
)
from .error import convert_error, ForbiddenError
from .user import get_user_query
from .utils import raise_if_all_none


class CollectionIn(BaseModel):
    """A collection without id, suitable for creation."""

    name: str = ...
    title: str = ...
    public: bool = False


class CollectionCreate(BaseModel):
    """A collection without id, suitable for creation."""

    owner: int = ...
    name: str = ...
    title: str = ...
    public: bool = False


class Collection(BaseModel):
    """A collection along with info related to a user (rw rights, etc.)"""

    id: int = ...
    owner: int = ...
    name: str = ...
    title: str = ...
    public: bool = False
    deleted: bool = False

    can_edit: bool = True

    @classmethod
    def from_row(cls, logged_user, row):
        col_dict = dict(**row)

        if col_dict["user_id"] is None:
            col_dict["user_id"] = logged_user.id
            col_dict["can_edit"] = logged_user.is_admin

        return Collection(**col_dict)

    @classmethod
    def wrapper(cls, logged_user):
        return lambda row: cls.from_row(logged_user, row)


class CollectionUpdate(CollectionIn):
    name: str
    title: str
    public: bool


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
    logged_user: UserDb,
    user_id: int,
    *,
    collection_name: str = None,
    only_owned: bool = True,
    include_private: bool = False,
    include_deleted: bool = False,
):
    query = (
        select([collections, user_collections])
        .select_from(
            collections.outerjoin(
                user_collections,
                and_(
                    collections.c.id == user_collections.c.collection_id,
                    user_collections.c.user_id == logged_user.id,
                )
            )
        )
    )

    if not include_private:
        query = query.where(
            or_(
                collections.c.public,
                user_collections.c.user_id != None,
            )
        )

    if collection_name is not None:
        query = query.where(collections.c.name == collection_name)

    if only_owned:
        query = query.where(collections.c.owner == user_id)
    else:
        query = query.where(user_collections.c.user_id == user_id)

    if not include_deleted:
        query = query.where(~collections.c.deleted)

    return query


async def get_collection(
    database: Database,
    logged_user: UserDb,
    user_id: int,
    collection_name: str,
    *,
    only_owned: bool = True,
    include_private: bool = False,
    include_deleted: bool = False,
) -> Collection:

    query = get_user_collections_query(
        logged_user = logged_user,
        user_id = user_id,
        collection_name = collection_name,
        only_owned = only_owned,
        include_private = include_private,
        include_deleted = include_deleted,
    )

    return await database.one(query, Collection.wrapper(logged_user))


async def get_collections(
    database: Database,
    logged_user: UserDb,
    user_id: int,
    *,
    only_owned: bool = True,
    include_private: bool = False,
    include_deleted: bool = False,
    order_by_title: bool = True,
) -> List[Collection]:

    query = get_user_collections_query(
        logged_user,
        user_id = user_id,
        only_owned = only_owned,
        include_private = include_private,
        include_deleted = include_deleted,
    )

    if order_by_title:
        query = query.order_by(collections.c.title)

    return await database.all(query, Collection.wrapper(logged_user))


def update_collection_query(
    database: Database,
    collection_id: int,
):
    return (
        collections.update()
        .returning(collections)
        .where(collections.c.id == collection_id)
    )


async def update_collection(
    database: Database,
    collection_id: int,
    value: CollectionIn,
) -> Collection:
    query = (
        update_collection_query(
            database,
            collection_id = collection_id,
        )
        .values(**value.dict(include={"name", "title", "public"}))
    )

    return await database.one(query)


async def delete_collection(
    database: Database,
    collection_id: int,
):
    query = (
        update_collection_query(
            database,
            collection_id = collection_id,
        )
        .values(deleted = True)
    )

    await database.one(query)
