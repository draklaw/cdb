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
from .user import get_user
from .collection import get_collection


class ItemCreate(BaseModel):
    """An item without id, suitable for creation."""

    name: str = Field(..., index=True)
    title: str = ...
    # properties: dict = Field(...)

    @classmethod
    def from_row(cls, row):
        return cls(**row)


class ItemDb(ItemCreate):
    """An item as stored in the db."""

    id: int = Field(..., primary_key=True)
    collection: int = Field(..., ForeignKey("collections.id"), index=True)
    deleted: bool = False

    class Config:
        sql_alchemy = [
            UniqueConstraint("collection", "name"),
        ]


items = create_table("items", ItemDb)


@convert_error
async def create_item(
    database: Database,
    item: Union[ItemCreate, ItemDb],
) -> ItemDb:
    """Creates an item, returns it."""

    params = item.dict(exclude={"id"})
    params.setdefault("deleted", False)

    id = await database.execute(items.insert(), params)

    return ItemDb(
        id = id,
        **params,
    )


def get_item_query(
    collection_id: int,
    *,
    include_deleted: bool = False,
    order_by_title: bool = True,
):
    query = (
        select([items])
        .where(items.c.collection == collection_id)
    )

    if not include_deleted:
        query = query.where(~items.c.deleted)

    if order_by_title:
        query = query.order_by(items.c.title)

    return query


async def get_items(
    database: Database,
    collection_id: int,
    *,
    include_deleted: bool = False,
    order_by_title: bool = True,
) -> List[ItemDb]:

    query = get_item_query(collection_id, include_deleted=include_deleted)

    return await database.all(query, ItemDb.from_row)
