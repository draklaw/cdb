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

from pydantic import BaseModel, SecretStr
from sqlalchemy import (
    ForeignKey, PrimaryKeyConstraint, UniqueConstraint,
)

from .schema import Field, create_table


class UserDb(BaseModel):
    """A user as stored in the DB.
    """

    id: int = Field(..., primary_key=True)
    username: str = Field(..., unique=True)
    email: str = Field(..., unique=True)
    hashed_password: SecretStr = ...
    is_admin: bool = False
    disabled: bool = False

    @classmethod
    def from_row(cls, row):
        return cls(**row)


class CollectionDb(BaseModel):
    """A collection as stored in the DB.
    """

    id: int = Field(..., primary_key=True)
    owner: int = Field(..., ForeignKey("users.id"), index=True)
    name: str = Field(..., index=True)
    title: str = ...
    public: bool = False
    deleted: bool = False

    class Config:
        sql_alchemy = [
            UniqueConstraint("owner", "name"),
        ]


class UserCollection(BaseModel):
    """The link between a user and a collection.
    """

    user_id: int = Field(..., ForeignKey("users.id"), index=True)
    collection_id: int = Field(..., ForeignKey("collections.id"), index=True)
    can_edit: bool = True

    class Config:
        sql_alchemy = [
            PrimaryKeyConstraint("user_id", "collection_id"),
        ]


class ItemDb(BaseModel):
    """An item as stored in the db.
    """

    id: int = Field(..., primary_key=True)
    collection: int = Field(..., ForeignKey("collections.id"), index=True)
    name: str = Field(..., index=True)
    title: str = ...
    properties: dict = Field(...)
    deleted: bool = False

    class Config:
        sql_alchemy = [
            UniqueConstraint("collection", "name"),
        ]

    @classmethod
    def from_row(cls, row):
        return cls(**row)


class FieldDb(BaseModel):
    id: int = Field(..., primary_key=True)
    collection: int = Field(..., ForeignKey("collections.id"), index=True)
    name: str = ...
    field: str = ...
    label: str = ...
    type: str = ...
    sort_index: int = ...
    width: float = -1.0
    deleted: bool = False

    class Config:
        sql_alchemy = [
            UniqueConstraint("collection", "name"),
        ]

    @classmethod
    def from_row(cls, row):
        return cls(**row)


users = create_table("users", UserDb)
collections = create_table("collections", CollectionDb)
user_collections = create_table("user_collections", UserCollection)
items = create_table("items", ItemDb)
fields = create_table("fields", FieldDb)
