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

from pydantic import BaseModel

# Schema has been renamed Field in recent version of pydantic
try:
    from pydantic import Field
except ImportError:
    from pydantic import Schema as Field

from sqlalchemy import (
    String,
    bindparam,
)
from sqlalchemy.engine import Connection

from .schema import create_table


class User(BaseModel):
    id: int = Field(..., primary_key=True)
    username: str = Field(...,
                          min_length=3, max_length=64,
                          unique=True, index=True)
    email: str = Field(..., max_length=128, unique=True, index=True)
    hashed_password: str = Field(..., max_length=128)
    is_admin: bool = False
    is_active: bool = True


user = create_table(User)


_create_user = user.insert()
_user_by_username = (
    user.select()
        .where(user.c.username == bindparam("username", type_=String))
)


def create_user(
    connection: Connection,
    username: str,
    email: str,
    hashed_password: str,
    is_admin: bool = False,
    is_active: bool = True,
) -> int:
    return connection.execute(
        _create_user,
        username=username,
        email=email,
        hashed_password=hashed_password,
        is_admin=is_admin,
        is_active=is_active,
    ).inserted_primary_key[0]


def user_by_username(
    connection: Connection,
    username: str,
) -> User:
    return User(**connection.execute(
        _user_by_username,
        username=username
    ).first())
