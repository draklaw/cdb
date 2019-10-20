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
from pydantic import BaseModel, SecretStr

from sqlalchemy import (
    Unicode,
    bindparam,
)
from databases import Database

from .schema import Field, create_table
from .query import Query


class UserBase(BaseModel):
    """Base class for users.
    """

    username: str = Field(..., unique=True)
    email: str = Field(..., unique=True)
    is_admin: bool = False


class UserCreate(UserBase):
    """A user without id but with a hashed_password, useful for inserting user
    in the DB.
    """

    hashed_password: SecretStr = ...

    def unwrapped_dict(self) -> dict:
        d = self.dict()
        d["hashed_password"] = d["hashed_password"].get_secret_value()
        return d


class UserDb(UserCreate):
    """A user as stored in the DB.
    """

    id: int = Field(..., primary_key=True)
    disabled: bool = False


user = create_table("users", UserDb)


_create_user = user.insert()
_user_by_id = (
    user.select()
        .where(user.c.id == bindparam("id", type_=Unicode))
)


class UserQuery(Query):
    def __init__(
        self,
        database: Database,
        *,
        include_disabled = False,
    ):
        super().__init__(
            database,
            user,
            wrapper = UserDb,
        )

        self._include_disabled = include_disabled

    def query(self):
        query = super().query()
        if not self._include_disabled:
            query = query.where(~user.c.disabled)
        return query

    def include_disabled(self) -> "UserQuery":
        self._include_disabled = True
        return self

    def with_id(self, id: int) -> "UserQuery":
        return self.where(user.c.id == id)

    def with_username(self, username: str) -> "UserQuery":
        return self.where(user.c.username == username)

    def with_email(self, email: str) -> "UserQuery":
        return self.where(user.c.email == email)

    def order_by_username(self) -> "UserQuery":
        return self.order_by(user.c.username)


async def create_user(
    database: Database,
    user: Union[UserCreate, UserDb],
) -> int:
    """Creates a user (from a UserCreate or UserDb), returns its primary key.
    """

    return await database.execute(
        _create_user,
        user[0].unwrapped_dict(),
    )


async def create_users(
    database: Database,
    *users: UserDb,
) -> None:
    """Creates several users, users must be UserDb objects.
    """

    await database.execute_many(
        _create_user,
        [user.unwrapped_dict() for user in users],
    )
