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

from typing import List

from starlette.status import HTTP_403_FORBIDDEN
from fastapi import APIRouter, HTTPException

from cdb_database import (
    user as user_db,
    collection as collection_db,
    field as field_db,
)

from .db import Database, transaction
from .user import current_user
from .collection import get_collection


router = APIRouter()


@router.get(
    "/users/{username}/collections/{collection_name}/fields",
    response_model = List[field_db.FieldDb],
    tags = ["field"],
    summary = "Get the fields of a collection",
)
async def get_fields(
    username: str,
    collection_name: str,
    logged_user: user_db.UserDb = current_user,
    db: Database = transaction,
):
    collection = await get_collection(
        username,
        collection_name,
        logged_user,
        db,
    )

    return await field_db.get_fields(
        db,
        collection.id,
        include_deleted = logged_user.is_admin,
    )


@router.get(
    "/users/{username}/collections/{collection_name}/fields/{field_name}",
    response_model = field_db.FieldDb,
    tags = ["field"],
    summary = "Get a field",
)
async def get_field(
    username: str,
    collection_name: str,
    field_name: str,
    logged_user: user_db.UserDb = current_user,
    db: Database = transaction,
):
    collection = await get_collection(
        username,
        collection_name,
        logged_user,
        db,
    )

    return await field_db.get_field(
        db,
        collection.id,
        field_name,
        include_deleted = logged_user.is_admin,
    )


@router.post(
    "/users/{username}/collections/{collection_name}/fields",
    response_model = field_db.FieldDb,
    status_code = 201,
    tags = ["field"],
    summary = "Create a new field",
)
async def create_field(
    username: str,
    collection_name: str,
    field: field_db.FieldIn,
    logged_user: user_db.UserDb = current_user,
    db: Database = transaction,
):
    collection = await get_collection(
        username,
        collection_name,
        logged_user,
        db,
    )

    if not collection.can_edit and not logged_user.is_admin:
        raise HTTPException(HTTP_403_FORBIDDEN,
            "You don't have create rights on this collection.")

    return await field_db.create_field(
        db,
        field_db.FieldCreate(
            collection = collection.id,
            **field.dict(),
        ),
    )


@router.put(
    "/users/{username}/collections/{collection_name}/fields/{field_name}",
    response_model = field_db.FieldDb,
    tags = ["field"],
    summary = "Update an field",
)
async def update_field(
    username: str,
    collection_name: str,
    field_name: str,
    value: field_db.FieldUpdate,
    logged_user: user_db.UserDb = current_user,
    db: Database = transaction,
):
    collection = await get_collection(
        username,
        collection_name,
        logged_user,
        db,
    )

    if not collection.can_edit:
        raise HTTPException(
            status_code = HTTP_403_FORBIDDEN,
            detail = "You don't have edit rights on this field."
        )

    field = await field_db.get_field(
        db,
        collection.id,
        field_name,
        include_deleted = logged_user.is_admin,
    )

    return await field_db.update_field(
        db,
        field.id,
        value,
    )


@router.delete(
    "/users/{username}/collections/{collection_name}/fields/{field_name}",
    tags = ["field"],
    summary = "Delete an field",
)
async def delete_field(
    username: str,
    collection_name: str,
    field_name: str,
    logged_user: user_db.UserDb = current_user,
    db: Database = transaction,
):
    collection = await get_collection(
        username,
        collection_name,
        logged_user,
        db,
    )

    if not collection.can_edit:
        raise HTTPException(
            status_code = HTTP_403_FORBIDDEN,
            detail = "You don't have delete rights on this field."
        )

    field = await field_db.get_field(
        db,
        collection.id,
        field_name,
        include_deleted = logged_user.is_admin,
    )

    await field_db.delete_field(
        db,
        field.id,
    )

    return dict(
        detail = "Field deleted successfully."
    )
