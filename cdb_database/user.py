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

from typing import Union
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
from databases import Database

from .schema import create_table


class UserBase(BaseModel):
    """Base class for users.
    """

    username: str = Field(...,
                          min_length=3, max_length=64,
                          unique=True, index=True)
    email: str = Field(..., max_length=128, unique=True, index=True)
    is_admin: bool = False
    is_active: bool = True


class UserCreate(UserBase):
    """A user without id but with a hashed_password, useful for inserting user
    in the DB.
    """

    hashed_password: str = Field(..., max_length=128)


class UserDb(UserCreate):
    """A user as stored in the DB.
    """

    id: int = Field(..., primary_key=True)


class UserPublic(UserBase):
    """A user without password field, can be exposed publicly (e.g. through an
    api.
    """

    id: int


user = create_table(UserDb)


_create_user = user.insert()
_user_by_id = (
    user.select()
        .where(user.c.id == bindparam("id", type_=String))
)
_user_by_username = (
    user.select()
        .where(user.c.username == bindparam("username", type_=String))
)
_user_by_email = (
    user.select()
        .where(user.c.email == bindparam("email", type_=String))
)


async def create_user(
    database: Database,
    user: Union[UserCreate, UserDb],
) -> int:
    """Creates a user (from a UserCreate or UserDb), returns its primary key.
    """

    return await database.execute(
        _create_user,
        user[0].dict(),
    )


async def create_users(
    database: Database,
    *users: UserDb,
) -> None:
    """Creates several users, users must be UserDb objects.
    """

    await database.execute_many(
        _create_user,
        [user.dict() for user in users],
    )


async def get_user(
    database: Database,
    *,
    id: int = None,
    username: str = None,
    email: str = None,
) -> UserDb:
    """Get a user (UserDb). One of the keyword parameters must be set.
    """

    count = sum(param is not None for param in (id, username, email))
    if count != 1:
        raise TypeError(
            f"get_user() should have exactly one of id, username or email set "
            f"({count} set)"
        )

    if id is not None:
        row = await database.fetch_one(
            _user_by_id.params(id=id)
        )
    elif username is not None:
        row = await database.fetch_one(
            _user_by_username.params(username=username)
        )
    elif email is not None:
        row = await database.fetch_one(
            _user_by_email.params(email=email)
        )

    return UserDb(**row)
