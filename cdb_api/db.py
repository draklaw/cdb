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

from fastapi import Depends

from cdb_database import Database

from . import settings
from .utils import logger


database_url = None
database = None


async def setup_database():
    global database, database_url

    assert database is None

    database_url = (
        settings.database_url
        if not settings.test
        else settings.test_database_url
    )

    logger.info(f"Connect to database {database_url!r}...")
    database = Database(database_url)

    await database.connect()


async def teardown_database():
    global database

    assert database is not None

    await database.disconnect()

    database = None


async def get_db_transaction():
    if not settings.test:
        async with database.transaction():
            yield database
    else:
        yield database


transaction = Depends(get_db_transaction)
