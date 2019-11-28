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

from .tables import (
    ItemDb,
    items,
)
from .error import convert_error


class ItemIn(BaseModel):
    """An item without id, suitable for creation."""

    name: str = ...
    title: str = ...
    properties: dict = ...


class ItemCreate(BaseModel):
    """An item without id, suitable for creation."""

    collection: int = ...
    name: str = ...
    title: str = ...
    properties: dict = ...


class ItemUpdate(BaseModel):
    """An item without id, suitable for creation."""

    name: str
    title: str
    properties: dict


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


async def get_item(
    database: Database,
    collection_id: int,
    item_name: str,
    *,
    include_deleted: bool = False,
) -> List[ItemDb]:

    query = (
        get_item_query(collection_id, include_deleted=include_deleted)
        .where(items.c.name == item_name)
    )

    return await database.one(query, ItemDb.from_row)


async def update_item(
    database: Database,
    item_id: int,
    value: ItemUpdate,
) -> ItemDb:

    query = (
        items.update()
        .returning(items)
        .where(items.c.id == item_id)
        .values(**value.dict(include={"name", "title", "properties"}))
    )

    return await database.one(query, ItemDb.from_row)


async def delete_item(
    database: Database,
    item_id: int,
) -> ItemDb:

    query = (
        items.update()
        .returning(items)
        .where(items.c.id == item_id)
        .values(deleted = True)
    )

    await database.one(query)
