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
    FieldDb,
    fields,
)
from .error import convert_error


class FieldIn(BaseModel):
    name: str = ...
    field: str = ...
    label: str = ...
    type: str = ...
    sort_index: int = -1
    width: float = -1.0


class FieldCreate(BaseModel):
    collection: int = ...
    name: str = ...
    field: str = ...
    label: str = ...
    type: str = ...
    sort_index: int = -1
    width: float = -1.0


class FieldUpdate(BaseModel):
    name: str
    field: str
    label: str
    type: str
    sort_index: int
    width: float


@convert_error
async def create_field(
    database: Database,
    field: Union[FieldCreate, FieldDb],
) -> FieldDb:
    params = field.dict(exclude={"id"})
    params.setdefault("deleted", False)

    id = await database.execute(fields.insert(), params)

    return FieldDb(
        id = id,
        **params,
    )


def get_field_query(
    collection_id: int,
    *,
    include_deleted: bool = False,
    order_by_title: bool = True,
):
    query = (
        select([fields])
        .where(fields.c.collection == collection_id)
    )

    if not include_deleted:
        query = query.where(~fields.c.deleted)

    if order_by_title:
        query = query.order_by(fields.c.sort_index)

    return query


async def get_fields(
    database: Database,
    collection_id: int,
    *,
    include_deleted: bool = False,
    order_by_title: bool = True,
) -> List[FieldDb]:

    query = get_field_query(collection_id, include_deleted=include_deleted)

    return await database.all(query, FieldDb.from_row)


async def get_field(
    database: Database,
    collection_id: int,
    field_name: str,
    *,
    include_deleted: bool = False,
) -> List[FieldDb]:

    query = (
        get_field_query(collection_id, include_deleted=include_deleted)
        .where(fields.c.name == field_name)
    )

    return await database.one(query, FieldDb.from_row)


async def update_field(
    database: Database,
    field_id: int,
    value: FieldUpdate,
) -> FieldDb:

    query = (
        fields.update()
        .returning(fields)
        .where(fields.c.id == field_id)
        .values(**value.dict(include={"name", "field", "label", "type", "sort_index", "width"}))
    )

    return await database.one(query, FieldDb.from_row)


async def delete_item(
    database: Database,
    field_id: int,
) -> FieldDb:

    query = (
        fields.update()
        .returning(fields)
        .where(fields.c.id == field_id)
        .values(deleted = True)
    )

    await database.one(query)
