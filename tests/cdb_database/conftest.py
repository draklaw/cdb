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

import os
import asyncio
import pytest
from sqlalchemy import create_engine
from dotenv import load_dotenv

from cdb_database import Database, create_tables, drop_tables
from cdb_database.test_db import fill_test_db


load_dotenv()


@pytest.yield_fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def database():
    db_url = os.getenv("CDB_TEST_DATABASE")

    engine = create_engine(db_url)
    drop_tables(engine)
    create_tables(engine)

    async with Database(db_url) as database:
        await fill_test_db(database)
        yield database
