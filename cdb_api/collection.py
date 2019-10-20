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

from starlette.status import HTTP_401_UNAUTHORIZED
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
    user: user_db.UserDb = current_user,
    db: Database = transaction,
):
    user_query = user_db.UserQuery(db).with_username(username)
    if user.is_admin:
        user_query.include_disabled()
    target_user = await user_query.one()

    query = (
        collection_db.CollectionQuery(db, user_id=target_user.id)
        .order_by_title()
    )
    query.only_owned()

    if username != user.username and not user.is_admin:
        query.only_public()
    if user.is_admin:
        query.include_deleted()

    return await query.all()


@router.post(
    "/users/{username}/collections",
    response_model = collection_db.Collection,
    tags = ["collection"],
    summary = "Create a new collection",
)
async def post_collection(
    username: str,
    collection: collection_db.CollectionIn,
    user: user_db.UserDb = current_user,
    db: Database = transaction,
):
    if username != user.username and not user.is_admin:
        raise HTTPException(
            status_code = HTTP_401_UNAUTHORIZED,
            detail =
                "Users can only create collections in their own repository."
        )

    user_query = user_db.UserQuery(db).with_username(username)
    if user.is_admin:
        user_query.include_disabled()
    target_user = await user_query.one()

    col = await collection_db.create_collection(
        db,
        collection_db.CollectionCreate(
            owner = target_user.id,
            **collection.dict(),
        ),
    )

    return collection_db.Collection(
        **col.dict(),
        user_id = target_user.id,
        can_edit = True,
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
    user: user_db.UserDb = current_user,
    db: Database = transaction,
):
    user_query = user_db.UserQuery(db).with_username(username)
    if user.is_admin:
        user_query.include_disabled()
    target_user = await user_query.one()

    query = (
        collection_db.CollectionQuery(db, user_id=target_user.id)
        .only_owned()
        .with_name(collection_name)
    )

    if username != user.username and not user.is_admin:
        query.only_public()
    if user.is_admin:
        query.include_deleted()

    return await query.one()


@router.put(
    "/users/{username}/collections/{collection_name}",
    response_model = collection_db.Collection,
    tags = ["collection"],
    summary = "Update a collection",
)
async def update_collection(
    username: str,
    collection_name: str,
    collection: collection_db.CollectionCreate,
    user: user_db.UserDb = current_user,
    db: Database = transaction,
):
    ...


@router.delete(
    "/users/{username}/collections/{collection_name}",
    response_model = collection_db.Collection,
    tags = ["collection"],
    summary = "Delete a collection",
)
async def delete_collection(
    username: str,
    collection_name: str,
    user: user_db.UserDb = current_user,
    db: Database = transaction,
):
    ...
