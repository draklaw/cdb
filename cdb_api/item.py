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
    item as item_db
)

from .db import Database, transaction
from .user import current_user
from .collection import get_collection


router = APIRouter()


@router.get(
    "/users/{username}/collections/{collection_name}/items",
    response_model = List[item_db.ItemDb],
    tags = ["item"],
    summary = "Get the items of a collection",
)
async def get_items(
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

    return await item_db.get_items(
        db,
        collection.id,
        include_deleted = logged_user.is_admin,
    )


@router.get(
    "/users/{username}/collections/{collection_name}/items/{item_name}",
    response_model = item_db.ItemDb,
    tags = ["item"],
    summary = "Get an item",
)
async def get_item(
    username: str,
    collection_name: str,
    item_name: str,
    logged_user: user_db.UserDb = current_user,
    db: Database = transaction,
):
    collection = await get_collection(
        username,
        collection_name,
        logged_user,
        db,
    )

    return await item_db.get_item(
        db,
        collection.id,
        item_name,
        include_deleted = logged_user.is_admin,
    )


@router.post(
    "/users/{username}/collections/{collection_name}/items",
    response_model = item_db.ItemDb,
    status_code = 201,
    tags = ["item"],
    summary = "Create a new item",
)
async def create_item(
    username: str,
    collection_name: str,
    item: item_db.ItemIn,
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

    return await item_db.create_item(
        db,
        item_db.ItemCreate(
            collection = collection.id,
            **item.dict(),
        ),
    )


@router.put(
    "/users/{username}/collections/{collection_name}/items/{item_name}",
    response_model = item_db.ItemDb,
    tags = ["item"],
    summary = "Update an item",
)
async def update_item(
    username: str,
    collection_name: str,
    item_name: str,
    value: item_db.ItemUpdate,
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
            detail = "You don't have edit rights on this item."
        )

    item = await item_db.get_item(
        db,
        collection.id,
        item_name,
        include_deleted = logged_user.is_admin,
    )

    return await item_db.update_item(
        db,
        item.id,
        value,
    )


@router.delete(
    "/users/{username}/collections/{collection_name}/items/{item_name}",
    tags = ["item"],
    summary = "Delete an item",
)
async def delete_item(
    username: str,
    collection_name: str,
    item_name: str,
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
            detail = "You don't have delete rights on this item."
        )

    item = await item_db.get_item(
        db,
        collection.id,
        item_name,
        include_deleted = logged_user.is_admin,
    )

    await item_db.delete_item(
        db,
        item.id,
    )

    return dict(
        detail = "Item deleted successfully."
    )
