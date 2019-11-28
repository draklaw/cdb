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

from cdb_database.error import (
    AlreadyExistsError,
    NotFoundError,
    ForbiddenError,
)
from cdb_database.collection import (
    CollectionCreate,
    CollectionDb,
    CollectionIn,
    Collection,
    create_collection,
    get_collection,
    get_collections,
    update_collection,
    delete_collection,
    link_user_to_collection,
)
from cdb_database.item import (
    ItemDb,
    ItemCreate,
    ItemUpdate,
    get_items,
    get_item,
    create_item,
    update_item,
    delete_item,
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
    test_test_items,
)


pytestmark = pytest.mark.asyncio


async def test_get_items(database):
    items = await get_items(
        database,
        test_test_col.id,
    )

    assert items == sorted(test_test_items, key=lambda i: i.title)


async def test_get_item(database):
    item = await get_item(
        database,
        test_test_col.id,
        test_test_items[3].name,
    )

    assert item == test_test_items[3]


async def test_create_item(database):
    async with database.transaction(force_rollback=True):
        item = ItemCreate(
            collection = test_test_col.id,
            name = "foo",
            title = "Bar",
            properties = dict(stuff="foobar"),
        )
        result = await create_item(database, item)

        expected = ItemDb(
            id = result.id,
            deleted = False,
            **item.dict(),
        )

        assert result == expected

        result = await get_item(
            database,
            test_test_col.id,
            item.name,
        )

        assert result == expected


async def test_create_duplicate_item(database):
    async with database.transaction(force_rollback=True):
        item = ItemCreate(
            collection = test_test_col.id,
            name = test_test_items[7].name,
            title = "Bar",
            properties = dict(stuff="foobar"),
        )

        with pytest.raises(AlreadyExistsError):
            await create_item(database, item)


async def test_update_item(database):
    async with database.transaction(force_rollback=True):
        item = ItemUpdate(
            name = "foo",
            title = "FooBar",
            properties = dict(stuff="foobar"),
        )
        result = await update_item(
            database,
            test_test_items[4].id,
            item,
        )

        expected = ItemDb(
            id = test_test_items[4].id,
            collection = test_test_col.id,
            name = item.name,
            title = item.title,
            properties = dict(stuff="foobar"),
            deleted = False,
        )

        assert result == expected

        result = await get_item(
            database,
            test_test_col.id,
            item.name,
        )

        assert result == expected


async def test_delete_item(database):
    async with database.transaction(force_rollback=True):
        await delete_item(
            database,
            test_test_items[6].id,
        )

        with pytest.raises(NotFoundError):
            result = await get_item(
                database,
                test_test_col.id,
                test_test_items[6].name,
            )
