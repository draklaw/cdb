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
    collection as collection_db
)

from .db import Database, transaction
from .user import current_user


router = APIRouter()


@router.get(
    "/users/{username}/collections",
    response_model = List[collection_db.Collection],
    tags = ["collection"],
    summary = "Get the (visible) collections owned by a user",
)
async def get_collections(
    username: str,
    only_owned: bool = True,
    logged_user: user_db.UserDb = current_user,
    db: Database = transaction,
):
    if (not only_owned
        and not logged_user.is_admin
        and username != logged_user.username
    ):
        raise HTTPException(
            status_code = HTTP_403_FORBIDDEN,
            detail =
                "Accessing linked collections of other users is not allowed."
        )

    user = await user_db.get_user(
        db,
        username = username,
        include_disabled = logged_user.is_admin,
    )

    return await collection_db.get_collections(
        db,
        logged_user = logged_user,
        user_id = user.id,
        only_owned = only_owned,
        include_private = user.id == logged_user.id or logged_user.is_admin,
        include_deleted = logged_user.is_admin,
    )


@router.get(
    "/users/{username}/collections/{collection_name}",
    response_model = collection_db.Collection,
    tags = ["collection"],
    summary = "Get a collection along with its items",
)
async def get_collection(
    username: str,
    collection_name: str,
    logged_user: user_db.UserDb = current_user,
    db: Database = transaction,
):
    user = await user_db.get_user(
        db,
        username = username,
        include_disabled = logged_user.is_admin,
    )

    return await collection_db.get_collection(
        db,
        logged_user = logged_user,
        user_id = user.id,
        collection_name = collection_name,
        include_private = user.id == logged_user.id or logged_user.is_admin,
        include_deleted = logged_user.is_admin,
    )


@router.post(
    "/users/{username}/collections",
    response_model = collection_db.Collection,
    status_code = 201,
    tags = ["collection"],
    summary = "Create a new collection",
)
async def create_collection(
    username: str,
    collection: collection_db.CollectionIn,
    logged_user: user_db.UserDb = current_user,
    db: Database = transaction,
):
    user = await user_db.get_user(
        db,
        username = username,
        include_disabled = logged_user.is_admin,
    )

    if user.id != logged_user.id and not logged_user.is_admin:
        raise HTTPException(
            status_code = HTTP_403_FORBIDDEN,
            detail =
                "Users can only create collections in their own repository."
        )

    col = await collection_db.create_collection(
        db,
        collection_db.CollectionCreate(
            owner = user.id,
            **collection.dict(),
        ),
    )

    return collection_db.Collection(
        **col.dict(),
        can_edit = True,
    )


@router.put(
    "/users/{username}/collections/{collection_name}",
    response_model = collection_db.Collection,
    tags = ["collection"],
    summary = "Update a collection",
)
async def update_collection(
    username: str,
    collection_name: str,
    value: collection_db.CollectionUpdate,
    logged_user: user_db.UserDb = current_user,
    db: Database = transaction,
):
    user = await user_db.get_user(
        db,
        username = username,
        include_disabled = logged_user.is_admin,
    )

    collection = await collection_db.get_collection(
        db,
        logged_user = logged_user,
        user_id = user.id,
        collection_name = collection_name,
        include_private = user.id == logged_user.id or logged_user.is_admin,
        include_deleted = logged_user.is_admin,
    )

    if not collection.can_edit:
        raise HTTPException(
            status_code = HTTP_403_FORBIDDEN,
            detail = "You don't have edit rights on this collection."
        )

    return await collection_db.update_collection(
        db,
        collection_id = collection.id,
        value = value,
    )


@router.delete(
    "/users/{username}/collections/{collection_name}",
    tags = ["collection"],
    summary = "Delete a collection",
)
async def delete_collection(
    username: str,
    collection_name: str,
    logged_user: user_db.UserDb = current_user,
    db: Database = transaction,
):
    user = await user_db.get_user(
        db,
        username = username,
        include_disabled = logged_user.is_admin,
    )

    collection = await collection_db.get_collection(
        db,
        logged_user = logged_user,
        user_id = user.id,
        collection_name = collection_name,
        include_private = user.id == logged_user.id or logged_user.is_admin,
        include_deleted = logged_user.is_admin,
    )

    if logged_user.id != collection.owner and not logged_user.is_admin:
        raise HTTPException(
            status_code = HTTP_403_FORBIDDEN,
            detail = "Only the owner of a collection can delete it."
        )

    await collection_db.delete_collection(
        db,
        collection_id = collection.id,
    )

    return dict(
        detail = "Collection deleted successfully."
    )
