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
    get_user,
)
from cdb_database.test_db import *


pytestmark = pytest.mark.asyncio


async def test_get_user_by_id(database):
    user = await get_user(database, id=admin_user.id)
    assert user == admin_user


async def test_get_user_by_username(database):
    user = await get_user(database, username=test_user.username)
    assert user == test_user


async def test_get_user_by_email(database):
    user = await get_user(database, email=disabled_user.email)
    assert user == disabled_user
