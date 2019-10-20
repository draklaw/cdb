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
from functools import wraps
from asyncio import iscoroutinefunction

import asyncpg


class CdbDatabaseError(RuntimeError):
    def __init__(self, *args):
        super().__init__(*args)


class NotFoundError(CdbDatabaseError):
    def __init__(self, *args):
        super().__init__(*args)


class AlreadyExistsError(CdbDatabaseError):
    def __init__(self, *args):
        super().__init__(*args)


def convert_error(func: Callable):
    if iscoroutinefunction(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except asyncpg.exceptions.UniqueViolationError:
                raise AlreadyExistsError("Resource already exists")
    else:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except asyncpg.exceptions.UniqueViolationError:
                raise AlreadyExistsError("Resource already exists")
    return wrapper
