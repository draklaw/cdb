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

import pytest

from cdb_database.error import AlreadyExistsError, NotFoundError
from cdb_database.collection import (
    CollectionCreate,
    CollectionDb,
    CollectionIn,
    Collection,
    create_collection,
    get_collection,
    get_collections,
    update_collection,
    link_user_to_collection,
)
from cdb_database.test_db import (
    builder,
    admin_user,
    test_user,
    disabled_user,
    admin_public_col,
    admin_private_col,
    admin_shared_col,
    test_test_col,
    test_public_col,
    test_deleted_col,
    disabled_public_col,
)


pytestmark = pytest.mark.asyncio


async def test_get_owned_private_collection_by_user_id_and_name(database):
    collection = await get_collection(
        database,
        test_user,
        user_id = test_user.id,
        collection_name = test_test_col.name,
    )

    expected = Collection(
        **test_test_col.dict(),
        user_id = test_user.id,
        can_edit = True,
    )

    assert collection == expected


async def test_get_owned_private_collection_by_username_and_name(database):
    collection = await get_collection(
        database,
        admin_user,
        username = admin_user.username,
        collection_name = admin_private_col.name,
    )

    expected = Collection(
        **admin_private_col.dict(),
        user_id = admin_user.id,
        can_edit = True,
    )

    assert collection == expected


async def test_get_owned_public_collection_by_username_and_name(database):
    collection = await get_collection(
        database,
        admin_user,
        username = admin_user.username,
        collection_name = admin_public_col.name,
    )

    expected = Collection(
        **admin_public_col.dict(),
        user_id = admin_user.id,
        can_edit = True,
    )

    assert collection == expected


async def test_get_other_public_collection_by_username_and_name(database):
    collection = await get_collection(
        database,
        test_user,
        username = admin_user.username,
        collection_name = admin_public_col.name,
    )

    expected = Collection(
        **admin_public_col.dict(),
        user_id = test_user.id,
        can_edit = False,
    )

    assert collection == expected


async def test_get_other_private_collection_by_username_and_name(database):
    with pytest.raises(NotFoundError):
        await get_collection(
            database,
            test_user,
            username = admin_user.username,
            collection_name = admin_private_col.name,
        )


async def test_get_other_shared_collection_by_username_and_name(database):
    collection = await get_collection(
        database,
        test_user,
        username = admin_user.username,
        collection_name = admin_shared_col.name,
    )

    expected = Collection(
        **admin_shared_col.dict(),
        user_id = test_user.id,
        can_edit = False,
    )

    assert collection == expected


async def test_get_other_private_collection_by_username_and_name_as_admin(database):
    collection = await get_collection(
        database,
        admin_user,
        username = test_user.username,
        collection_name = test_test_col.name,
    )

    expected = Collection(
        **test_test_col.dict(),
        user_id = admin_user.id,
        can_edit = True,
    )

    assert collection == expected


async def test_get_owned_collection_by_username_and_name_disabled_user(database):
    with pytest.raises(NotFoundError):
        await get_collection(
            database,
            disabled_user,
            username = disabled_user.username,
            collection_name = disabled_public_col.name,
        )


async def test_get_all_collections_by_user_id(database):
    collections = await get_collections(
        database,
        test_user,
        user_id = test_user.id,
        only_owned = False,
    )

    expected = [
        Collection(
            **admin_shared_col.dict(),
            user_id = test_user.id,
            can_edit = False,
        ),
        Collection(
            **test_public_col.dict(),
            user_id = test_user.id,
            can_edit = True,
        ),
        Collection(
            **test_test_col.dict(),
            user_id = test_user.id,
            can_edit = True,
        ),
    ]

    assert collections == expected


async def test_get_all_collections_by_user_id_including_deleted(database):
    collections = await get_collections(
        database,
        test_user,
        user_id = test_user.id,
        include_deleted = True,
        only_owned = False,
    )

    expected = [
        Collection(
            **test_deleted_col.dict(),
            user_id = test_user.id,
            can_edit = True,
        ),
        Collection(
            **admin_shared_col.dict(),
            user_id = test_user.id,
            can_edit = False,
        ),
        Collection(
            **test_public_col.dict(),
            user_id = test_user.id,
            can_edit = True,
        ),
        Collection(
            **test_test_col.dict(),
            user_id = test_user.id,
            can_edit = True,
        ),
    ]

    assert collections == expected


async def test_get_owned_collections_by_user_id(database):
    collections = await get_collections(
        database,
        test_user,
        user_id = test_user.id,
    )

    expected = [
        Collection(
            **test_public_col.dict(),
            user_id = test_user.id,
            can_edit = True,
        ),
        Collection(
            **test_test_col.dict(),
            user_id = test_user.id,
            can_edit = True,
        ),
    ]

    assert collections == expected


async def test_get_other_owned_collections_by_user_id(database):
    collections = await get_collections(
        database,
        test_user,
        user_id = admin_user.id,
    )

    expected = [
        Collection(
            **admin_public_col.dict(),
            user_id = test_user.id,
            can_edit = False,
        ),
        Collection(
            **admin_shared_col.dict(),
            user_id = test_user.id,
            can_edit = False,
        ),
    ]

    assert collections == expected


async def test_create_collection(database):
    async with database.transaction(force_rollback=True):
        collection = CollectionCreate(
            name = "new",
            owner = test_user.id,
            title = "A new collection",
            public = True,
        )
        result = await create_collection(database, collection)

        expected = CollectionDb(
            id = len(builder.collections) + 1,
            deleted = False,
            **collection.dict(),
        )

        assert result == expected


async def test_create_duplicate_collection(database):
    async with database.transaction(force_rollback=True):
        collection = CollectionCreate(
            name = "new",
            owner = test_user.id,
            title = "A new collection",
            public = True,
        )
        await create_collection(database, collection)

        with pytest.raises(AlreadyExistsError):
            await create_collection(database, collection)


async def test_update_owned_collection(database):
    async with database.transaction(force_rollback=True):
        update = CollectionIn(
            name = "updated",
            title = "Another title",
            public = True,
        )

        await update_collection(
            database,
            test_user,
            value = update,
            username = test_user.username,
            collection_name = test_test_col.name,
        )

        collection = await get_collection(
            database,
            test_user,
            username = test_user.username,
            collection_name = update.name,
        )

        expected = Collection(
            **test_test_col.dict(exclude={"name", "title", "public"}),
            **update.dict(),
            user_id = test_user.id,
            can_edit = True,
        )

        assert collection == expected


async def test_update_shared_collection(database):
    async with database.transaction(force_rollback=True):
        await link_user_to_collection(
            database,
            test_user.id,
            admin_private_col.id,
            can_edit = True,
        )

        update = CollectionIn(
            name = "updated",
            title = "Another title",
            public = True,
        )

        await update_collection(
            database,
            test_user,
            value = update,
            username = admin_user.username,
            collection_name = admin_private_col.name,
        )

        collection = await get_collection(
            database,
            test_user,
            username = admin_user.username,
            collection_name = update.name,
        )

        expected = Collection(
            **admin_private_col.dict(exclude={"name", "title", "public"}),
            **update.dict(),
            user_id = test_user.id,
            can_edit = True,
        )

        assert collection == expected


async def test_update_shared_collection_no_edit(database):
    async with database.transaction(force_rollback=True):
        update = CollectionIn(
            name = "updated",
            title = "Another title",
            public = True,
        )

        with pytest.raises(NotFoundError):
            await update_collection(
                database,
                test_user,
                value = update,
                username = admin_user.username,
                collection_name = admin_shared_col.name,
            )
