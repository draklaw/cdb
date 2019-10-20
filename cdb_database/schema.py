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

from typing import Any

from pydantic import ConstrainedStr, SecretStr

# Schema has been renamed Field in recent version of pydantic
try:
    from pydantic import PydanticField
except ImportError:
    from pydantic import Schema as PydanticField

from sqlalchemy import (
    MetaData, Table, Column,
    Boolean, Integer, Float, Unicode, UnicodeText,
)


metadata = MetaData()


_type_map = [
    (ConstrainedStr, lambda f: Unicode(f.type_.max_length)),
    (SecretStr, lambda f: UnicodeText),

    (bool, lambda f: Boolean),
    (str, lambda f: UnicodeText),
    (float, lambda f: Float),
    (int, lambda f: Integer),
]


class Field(PydanticField):
    """Similar to Pydantic's Field, but with arbitrary positional args."""

    def __init__(
        self,
        default: Any,
        *args,
        alias: str = None,
        title: str = None,
        description: str = None,
        const: bool = None,
        gt: float = None,
        ge: float = None,
        lt: float = None,
        le: float = None,
        multiple_of: float = None,
        min_items: int = None,
        max_items: int = None,
        min_length: int = None,
        max_length: int = None,
        regex: str = None,
        **extra: Any,
    ):
        super().__init__(
            default,
            alias = alias,
            title = title,
            description = description,
            const = const,
            gt = gt,
            ge = ge,
            lt = lt,
            le = le,
            multiple_of = multiple_of,
            min_items = min_items,
            max_items = max_items,
            min_length = min_length,
            max_length = max_length,
            regex = regex,
            args = args,
            **extra,
        )


def sa_type_from_field(field):
    # print(f"{field.name}: type: {field.type_}")
    for type_, factory in _type_map:
        # print(f"  try {type_}...")
        if issubclass(field.type_, type_):
            # print("    Found !")
            return factory(field)
    # print("  Fail")
    raise TypeError(f"No mapping for type {field.type_}")


def create_table(name, cls):
    sa_args = []
    if hasattr(cls.__config__, "sql_alchemy"):
        sa_args = cls.__config__.sql_alchemy

    columns = [
        create_column(field)
        for field in cls.__fields__.values()
    ] + sa_args

    return Table(name, metadata, *columns)


def create_column(field):
    type = sa_type_from_field(field)

    # schema will be renamed field_info in future pydantic
    extra = field.schema.extra
    kwargs = {**extra}
    args = kwargs.pop("args", [])
    if field.required or field.default is not None:
        kwargs["nullable"] = False
    if field.default is not None:
        kwargs["default"] = field.default

    return Column(field.name, type, *args, **kwargs)
