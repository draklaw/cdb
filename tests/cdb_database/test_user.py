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
from cdb_database.user import (
    UserDb,
    get_user,
    get_users,
    unwrapped_user_dict,
)
from cdb_database.error import NotFoundError
from cdb_database.test_db import (
    admin_user, test_user, disabled_user,
)


pytestmark = pytest.mark.asyncio


async def test_get_user_by_id(database):
    user = await get_user(database, user_id=admin_user.id)
    assert unwrapped_user_dict(user) == unwrapped_user_dict(admin_user)


async def test_get_user_by_username(database):
    user = await get_user(database, username=test_user.username)
    assert unwrapped_user_dict(user) == unwrapped_user_dict(test_user)


async def test_get_user_by_email(database):
    user = await get_user(database, email=test_user.email)
    assert unwrapped_user_dict(user) == unwrapped_user_dict(test_user)


async def test_get_disabled_user_fail(database):
    with pytest.raises(NotFoundError):
        await get_user(database, user_id=disabled_user.id)


async def test_get_disabled_user_explicitly(database):
    user = await get_user(
        database,
        user_id = disabled_user.id,
        include_disabled = True,
    )
    assert unwrapped_user_dict(user) == unwrapped_user_dict(disabled_user)


async def test_get_all_active_users(database):
    users = await get_users(database)

    unwrapped_users = list(map(unwrapped_user_dict, users))
    expected = list(map(unwrapped_user_dict, [
        admin_user,
        test_user,
    ]))

    assert unwrapped_users == expected


async def test_get_all_users(database):
    users = await get_users(database, include_disabled=True)

    unwrapped_users = list(map(unwrapped_user_dict, users))
    expected = list(map(unwrapped_user_dict, [
        admin_user,
        disabled_user,
        test_user,
    ]))

    assert unwrapped_users == expected
