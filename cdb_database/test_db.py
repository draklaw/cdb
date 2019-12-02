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

from .user import UserDb, UserCreate, create_user
from .collection import (
    CollectionDb,
    CollectionCreate,
    create_collection,
    link_user_to_collection,
)
from .item import create_item, ItemDb
from .field import create_field, FieldDb


class Builder:
    def __init__(self):
        self.users = []
        self.collections = []
        self.items = []
        self.fields = []

    def add_user(self, **kwargs):
        user = UserDb(
            id = len(self.users) + 1,
            **kwargs,
        )
        self.users.append(user)
        return user

    def add_collection(self, **kwargs):
        collection = CollectionDb(
            id = len(self.collections) + 1,
            **kwargs,
        )
        self.collections.append(collection)
        return collection

    def add_item(self, **kwargs):
        item = ItemDb(
            id = len(self.items) + 1,
            **kwargs,
        )
        self.items.append(item)
        return item

    def add_field(self, **kwargs):
        field = FieldDb(
            id = len(self.fields) + 1,
            **kwargs,
        )
        self.fields.append(field)
        return field

    async def fill_database(self, database: Database):
        for user in self.users:
            await create_user(database, user)

        for collection in self.collections:
            await create_collection(database, collection)

        for item in self.items:
            await create_item(database, item)

        for field in self.fields:
            await create_field(database, field)


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

admin_shared_col = builder.add_collection(
    owner = admin_user.id,
    name = "shared",
    title = "Private but shared with test",
)

admin_shared_edit_col = builder.add_collection(
    owner = admin_user.id,
    name = "shared-edit",
    title = "Private but shared with test, with edit rights",
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

disabled_public_col = builder.add_collection(
    owner = disabled_user.id,
    name = "public",
    title = "Public collection",
    public = True,
)


def build_items(collection, count=10):
    return [
        builder.add_item(
            name = f"item_{i:02d}",
            title = f"Item #{i}",
            collection = collection.id,
            properties = dict(index=i)
        )
        for i in range(1, count + 1)
    ]


admin_private_items = build_items(admin_private_col)
admin_shared_items = build_items(admin_shared_col)
admin_shared_edit_items = build_items(admin_shared_edit_col)
admin_public_items = build_items(admin_public_col)
test_test_items = build_items(test_test_col)
test_public_items = build_items(test_public_col)
test_deleted_items = build_items(test_deleted_col)
disabled_public_items = build_items(disabled_public_col)


def build_fields(collection):
    return [
        builder.add_field(
            collection = collection.id,
            name = "title",
            field = "title",
            label = "Title",
            type = "string",
            sort_index = 1,
            width = -1.0,
        ),
        builder.add_field(
            collection = collection.id,
            name = "index",
            field = "properties.index",
            label = "Index",
            type = "int",
            sort_index = 2,
            width = 4,
        ),
    ]


admin_private_fields = build_fields(admin_private_col)
admin_shared_fields = build_fields(admin_shared_col)
admin_shared_edit_fields = build_fields(admin_shared_edit_col)
admin_public_fields = build_fields(admin_public_col)
test_test_fields = build_fields(test_test_col)
test_public_fields = build_fields(test_public_col)
test_deleted_fields = build_fields(test_deleted_col)
disabled_public_fields = build_fields(disabled_public_col)


async def fill_test_db(database: Database):
    await builder.fill_database(database)

    await link_user_to_collection(
        database,
        test_user.id,
        admin_shared_col.id,
        can_edit = False,
    )

    await link_user_to_collection(
        database,
        test_user.id,
        admin_shared_edit_col.id,
        can_edit = True,
    )
