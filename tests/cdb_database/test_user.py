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

from cdb_database.user import (
    create_user,
    user_by_username,
)


def test_user_create_and_get(db):
    id = create_user(db, "test", "test@test.com", "123")
    user = user_by_username(db, "test")
    assert user.id == id
    assert user.username == "test"
    assert user.email == "test@test.com"
    assert user.hashed_password == "123"
    assert not user.is_admin
    assert user.is_active
