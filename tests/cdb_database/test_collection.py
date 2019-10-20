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
# from cdb_database.user import (
#     get_user,
# )
from cdb_database.collection import (
    CollectionQuery,
    Collection,
    get_collection,
)
from cdb_database.test_db import (
    admin_user,
    test_user,
    admin_public_col,
    admin_private_col,
    test_test_col,
    test_public_col,
    test_deleted_col,
)


pytestmark = pytest.mark.asyncio


async def test_get_collection_by_id(database):
    collection = await get_collection(database, id=test_test_col.id)
    assert collection == test_test_col


async def test_get_collection_by_user_id_and_name(database):
    collection = await (
        CollectionQuery(database, user_id=test_user.id)
        .with_name(test_test_col.name)
        .one()
    )

    expected = Collection(
        **test_test_col.dict(),
        user_id = test_user.id,
        can_edit = True,
    )

    assert collection == expected


async def test_get_collection_by_username_and_name(database):
    collection = await (
        CollectionQuery(database, username=admin_user.username)
        .with_name(admin_private_col.name)
        .one()
    )

    expected = Collection(
        **admin_private_col.dict(),
        user_id = admin_user.id,
        can_edit = True,
    )

    assert collection == expected


async def test_get_collections_by_user_id(database):
    collection = await (
        CollectionQuery(database, user_id=test_user.id)
        .order_by_title()
        .all()
    )

    expected = [
        Collection(
            **admin_private_col.dict(),
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

    assert collection == expected


async def test_get_collections_by_user_id_including_deleted(database):
    collection = await (
        CollectionQuery(database, user_id=test_user.id)
        .include_deleted()
        .order_by_title()
        .all()
    )

    expected = [
        Collection(
            **test_deleted_col.dict(),
            user_id = test_user.id,
            can_edit = True,
        ),
        Collection(
            **admin_private_col.dict(),
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

    assert collection == expected


async def test_get_collections_by_owner_id(database):
    collection = await (
        CollectionQuery(database, user_id=admin_user.id)
        .only_owned()
        .order_by_title()
        .all()
    )

    expected = [
        Collection(
            **admin_public_col.dict(),
            user_id = admin_user.id,
            can_edit = True,
        ),
        Collection(
            **admin_private_col.dict(),
            user_id = admin_user.id,
            can_edit = True,
        ),
    ]

    assert collection == expected


async def test_get_public_collections_by_owner_id(database):
    collection = await (
        CollectionQuery(database, user_id=test_user.id)
        .only_owned()
        .only_public()
        .order_by_title()
        .all()
    )

    expected = [
        Collection(
            **test_public_col.dict(),
            user_id = test_user.id,
            can_edit = True,
        ),
    ]

    assert collection == expected
