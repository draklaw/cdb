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
import argparse
import asyncio

from dotenv import load_dotenv


def init(args):
    from sqlalchemy import create_engine
    from cdb_database import create_tables

    db_url = os.getenv("CDB_DATABASE")

    print("Connect to database...")
    engine = create_engine(db_url)

    print("Create tables...")
    create_tables(engine)

    print("Done.")


async def test_db(args):
    from sqlalchemy import create_engine
    from databases import Database
    from cdb_database import create_tables, drop_tables
    from cdb_database.test_db import fill_test_db

    db_url = os.getenv("CDB_DATABASE")

    print("Connect to database...")
    engine = create_engine(db_url)

    print("Drop existing tables...")
    drop_tables(engine)

    print("Create tables...")
    create_tables(engine)

    print("Fill database with test data...")
    async with Database(db_url) as database:
        await fill_test_db(database)

    print("Done.")


def parse_args():
    parser = argparse.ArgumentParser(
        description = "CDB api command-line tools.",
    )

    subparsers = parser.add_subparsers(
        title = "subcommands",
        dest = "command",
        required = True,
        metavar = "COMMAND",
        help = "Sub-command to run",
    )

    init_parser = subparsers.add_parser(
        "init",
        help = "Initialize the database.",
    )
    init_parser.set_defaults(cmd=init)

    test_db_parser = subparsers.add_parser(
        "test_db",
        help = "Clear the db and fill it with test data.",
    )
    test_db_parser.set_defaults(cmd=test_db)

    return parser.parse_args()


if __name__ == "__main__":
    load_dotenv()

    args = parse_args()

    result = args.cmd(args)
    if asyncio.iscoroutine(result):
        asyncio.run(result)
