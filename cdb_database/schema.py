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

from pydantic import ConstrainedStr
from sqlalchemy import (
    MetaData, Table, Column,
    Boolean, Integer, Float, String,
)


metadata = MetaData()


_type_map = [
    (ConstrainedStr, lambda f: String(f.type_.max_length)),

    (bool, lambda f: Boolean),
    (str, lambda f: String),
    (float, lambda f: Float),
    (int, lambda f: Integer),
]


def sa_type_from_field(field):
    # print(f"{field.name}: type: {field.type_}")
    for type_, factory in _type_map:
        # print(f"  try {type_}...")
        if issubclass(field.type_, type_):
            # print("    Found !")
            return factory(field)
    # print("  Fail")
    raise TypeError(f"No mapping for type {field.type_}")


def create_table(cls):
    name = cls.__name__.lower()

    columns = [
        create_column(field)
        for field in cls.__fields__.values()
    ]

    return Table(name, metadata, *columns)


def create_column(field):
    type = sa_type_from_field(field)

    # schema will be renamed field_info in future pydantic
    extra = field.schema.extra
    args = {**extra}
    if field.required or field.default is not None:
        args["nullable"] = False
    if field.default is not None:
        args["default"] = field.default

    return Column(field.name, type, **args)
