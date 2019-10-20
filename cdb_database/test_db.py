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

from databases import Database

from .user import UserDb, create_users
from .collection import (
    CollectionDb,
    create_collections,
    link_user_to_collection,
)


class Builder:
    def __init__(self):
        self.users = []
        self.collections = []

    def add_user(self, **kwargs):
        if "id" not in kwargs:
            kwargs["id"] = len(self.users) + 1

        user = UserDb(**kwargs)
        self.users.append(user)
        return user

    def add_collection(self, **kwargs):
        if "id" not in kwargs:
            kwargs["id"] = len(self.collections) + 1

        collection = CollectionDb(**kwargs)
        self.collections.append(collection)
        return collection

    async def fill_database(self, database: Database):
        await create_users(database, *self.users)
        await create_collections(database, *self.collections)


builder = Builder()

admin_user = builder.add_user(
    username = "admin",
    email = "admin@cdb.org",
    # password = "password",
    hashed_password =
        "$2b$12$/nZ5kOk767gETPPP6tJo6eFMJKMldF1KcfXBfQbMEUkUUVEW8uGIq",
    is_admin = True,
)

test_user = builder.add_user(
    username = "test",
    email = "test@test.com",
    # password = "123",
    hashed_password =
        "$2b$12$g.Ht1khxE7obzOHlBs4/VOZGf7w6E16R04uXOhy6hKS28fpn4wCra",
)

disabled_user = builder.add_user(
    username = "disabled",
    email = "disabled@foo.net",
    # password = "disabled",
    hashed_password =
        "$2b$12$MUwE2PFQfScLrqxGsMGMXOH4xj5yz8Ai5cHW5RLOcm6JHvdp5Ogb.",
    disabled = True,
)


admin_private_col = builder.add_collection(
    owner = admin_user.id,
    name = "private",
    title = "Nobody can see this but me",
)

admin_public_col = builder.add_collection(
    owner = admin_user.id,
    name = "public",
    title = "Everybody can see this",
    public = True,
)

test_test_col = builder.add_collection(
    owner = test_user.id,
    name = "test",
    title = "This is a test",
)

test_public_col = builder.add_collection(
    owner = test_user.id,
    name = "public",
    title = "Public collection",
    public = True,
)

test_deleted_col = builder.add_collection(
    owner = test_user.id,
    name = "deleted",
    title = "Deleted collection",
    deleted = True,
)


async def fill_test_db(database: Database):
    await builder.fill_database(database)

    await link_user_to_collection(
        database,
        test_user.id,
        admin_private_col.id,
        can_edit = False
    )
