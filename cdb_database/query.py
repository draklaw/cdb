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

from typing import Callable

from databases import Database
from sqlalchemy import select

from .error import NotFoundError


class Query:
    def __init__(
        self,
        database: Database,
        *columns: list,
        wrapper: Callable = None,
    ):
        self._database = database
        self._query = select(columns)
        self._wrapper = wrapper

    def where(self, predicate):
        self._query = self._query.where(predicate)
        return self

    def order_by(self, *clauses):
        self._query = self._query.order_by(*clauses)
        return self

    def print_sql(self):
        compiled = self.query().compile()
        print(compiled)
        print(compiled.params)
        return self

    def query(self):
        return self._query

    def _wrap_result(self, row, *, wrapper=None):
        wrapper = wrapper or self._wrapper
        if wrapper:
            return self._wrapper(**row)
        return row

    async def one(self, *, wrapper=None):
        row = await self._database.fetch_one(self.query())
        if row is None:
            raise NotFoundError("Ressource does not exists")
        return self._wrap_result(row, wrapper=wrapper)

    async def all(self, *, wrapper=None):
        return list(map(
            lambda row: self._wrap_result(row, wrapper=wrapper),
            await self._database.fetch_all(self.query()),
        ))
