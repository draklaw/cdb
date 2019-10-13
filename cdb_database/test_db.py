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

from .user import UserDb, create_users


admin_user = UserDb(
    id=1,
    username="admin",
    email="admin@cdb.org",
    hashed_password="password",
    is_admin=True,
)

test_user = UserDb(
    id=2,
    username="test",
    email="test@test.com",
    hashed_password="123",
)

disabled_user = UserDb(
    id=3,
    username="disabled",
    email="disabled@foo.net",
    hashed_password="disabled",
    is_active=False,
)

users = [
    admin_user,
    test_user,
    disabled_user,
]


async def fill_test_db(database):
    await create_users(database, *users)
