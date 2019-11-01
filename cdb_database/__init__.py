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

import databases

from . import (
    schema,
    user,
    collection,
    item,
)
from .error import NotFoundError


def _identity(row):
    return row


class Database(databases.Database):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def one(self, query, wrapper=_identity):
        rows = await super().fetch_all(query)

        assert len(rows) < 2

        if not rows:
            raise NotFoundError("Collection does not exist.")

        return wrapper(rows[0])

    async def all(self, query, wrapper=_identity):
        rows = await super().fetch_all(query)

        return [
            wrapper(row)
            for row in rows
        ]


def create_tables(engine):
    schema.metadata.create_all(engine)


def drop_tables(engine):
    schema.metadata.drop_all(engine)
