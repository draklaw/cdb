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

from typing import List, Union
from pydantic import BaseModel, SecretStr

from sqlalchemy import select
from databases import Database

from .tables import (
    UserDb,
    users,
)


class UserCreate(BaseModel):
    """A user without id but with a hashed_password, useful for inserting user
    in the DB.
    """

    username: str = ...
    email: str = ...
    hashed_password: SecretStr = ...
    is_admin: bool = False
    disabled: bool = False

def unwrapped_user_dict(user, **kwargs) -> dict:
    d = user.dict(**kwargs)
    d["hashed_password"] = d["hashed_password"].get_secret_value()
    return d


async def create_user(
    database: Database,
    user: Union[UserCreate, UserDb],
) -> UserDb:
    """Creates a user, returns it."""

    params = unwrapped_user_dict(user, exclude={"id"})
    params.setdefault("disabled", False)
    id = await database.execute(users.insert(), params)

    return UserDb(id=id, **params)


def get_user_query(
    *,
    user_id: int = None,
    username: str = None,
    include_disabled: bool = False,
):
    query = select([users])

    if user_id is not None:
        query = query.where(users.c.id == user_id)

    if username is not None:
        query = query.where(users.c.username == username)

    if not include_disabled:
        query = query.where(~users.c.disabled)

    return query


async def get_user(
    database: Database,
    *,
    user_id: int = None,
    username: str = None,
    email: str = None,
    include_disabled: bool = False,
) -> UserDb:

    arg_sum = (
        int(user_id is not None)
        + int(username is not None)
        + int(email is not None)
    )
    if arg_sum != 1:
        raise TypeError("get_user: invalid arguments")

    query = get_user_query(
        include_disabled = include_disabled,
    )

    if user_id is not None:
        query = query.where(users.c.id == user_id)
    elif username is not None:
        query = query.where(users.c.username == username)
    else:
        query = query.where(users.c.email == email)

    return await database.one(query, UserDb.from_row)


async def get_users(
    database: Database,
    *,
    include_disabled: bool = False,
    order_by_username: bool = True,
) -> List[UserDb]:

    query = get_user_query(
        include_disabled = include_disabled,
    )

    if order_by_username:
        query = query.order_by(users.c.username)

    return await database.all(query, UserDb.from_row)
