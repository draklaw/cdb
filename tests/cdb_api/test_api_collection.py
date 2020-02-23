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


import pytest

from cdb_database.test_db import (
    builder,
    test_user,
    admin_user,
    disabled_user,
    admin_public_col,
    admin_private_col,
    admin_shared_col,
    admin_shared_edit_col,
    test_test_col,
    test_public_col,
    test_deleted_col,
    disabled_public_col,
)


# Unauthentified tests --------------------------------------------------------


def test_unauthentified_get_collection_fail(client):
    response = client.get("/users/test/collections/test")
    assert response.status_code == 401
    assert "detail" in response.json()


def test_unauthentified_get_collections_fail(client):
    response = client.get("/users/test/collections")
    assert response.status_code == 401
    assert "detail" in response.json()


def test_unauthentified_get_unknown_collection_fail(client):
    response = client.get("/users/test/collections/foobar")
    assert response.status_code == 401
    assert "detail" in response.json()


def test_unauthentified_post_collection_fail(client):
    response = client.post(
        "/users/test/collections",
        json = dict(
            name = "hello",
            title = "world",
            public = True,
        ),
    )
    assert response.status_code == 401
    assert "detail" in response.json()


def test_unauthentified_update_collection_fail(client):
    response = client.put(
        "/users/test/collections/test",
        json = dict(
            title = "ABC",
        ),
    )
    assert response.status_code == 401
    assert "detail" in response.json()


def test_unauthentified_delete_collection_fail(client):
    response = client.delete(
        "/users/test/collections/test",
    )
    assert response.status_code == 401
    assert "detail" in response.json()


# User tests ------------------------------------------------------------------


def test_get_owned_public_collection(client, user_headers):
    response = client.get(
        "/users/test/collections/public",
        headers = user_headers,
    )

    expected = dict(
        **test_public_col.dict(include={
            "id", "owner", "name", "title", "public", "std_fields", "deleted",
        }),
        can_edit = True,
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_get_owned_private_collection(client, user_headers):
    response = client.get(
        "/users/test/collections/test",
        headers = user_headers,
    )

    expected = dict(
        **test_test_col.dict(include={
            "id", "owner", "name", "title", "public", "std_fields", "deleted",
        }),
        can_edit = True,
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_get_other_public_collection(client, user_headers):
    response = client.get(
        "/users/admin/collections/public",
        headers = user_headers,
    )

    expected = dict(
        **admin_public_col.dict(include={
            "id", "owner", "name", "title", "public", "std_fields", "deleted",
        }),
        can_edit = False,
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_get_other_private_collection(client, user_headers):
    response = client.get(
        "/users/admin/collections/private",
        headers = user_headers,
    )

    assert response.status_code == 404
    assert "detail" in response.json()


def test_get_other_shared_collection(client, user_headers):
    response = client.get(
        "/users/admin/collections/shared",
        headers = user_headers,
    )

    expected = dict(
        **admin_shared_col.dict(include={
            "id", "owner", "name", "title", "public", "std_fields", "deleted",
        }),
        can_edit = False,
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_get_inexistant_collection(client, user_headers):
    response = client.get(
        "/users/admin/collections/foo",
        headers = user_headers,
    )

    assert response.status_code == 404
    assert "detail" in response.json()


def test_get_owned_collections(client, user_headers):
    response = client.get(
        "/users/test/collections",
        headers = user_headers,
    )

    expected = [
        dict(
            **test_public_col.dict(),
            can_edit = True,
        ),
        dict(
            **test_test_col.dict(),
            can_edit = True,
        ),
    ]

    assert response.status_code == 200
    assert response.json() == expected


def test_get_other_collections(client, user_headers):
    response = client.get(
        "/users/admin/collections",
        headers = user_headers,
    )

    expected = [
        dict(
            **admin_public_col.dict(),
            can_edit = False,
        ),
        dict(
            **admin_shared_col.dict(),
            can_edit = False,
        ),
        dict(
            **admin_shared_edit_col.dict(),
            can_edit = True,
        ),
    ]

    assert response.status_code == 200
    assert response.json() == expected


def test_get_deleted_user_collections(client, user_headers):
    response = client.get(
        "/users/deleted/collections",
        headers = user_headers,
    )

    assert response.status_code == 404
    assert "detail" in response.json()


def test_create_owned_collection(client, user_headers):
    collection = dict(
        name = "new",
        title = "A new collection",
        public = True,
        std_fields = [
            dict(
                name = "test",
                type = "text",
            ),
        ],
    )

    response = client.post(
        "/users/test/collections",
        json = collection,
        headers = user_headers,
    )

    expected = dict(
        **collection,
        id = response.json()["id"],
        owner = test_user.id,
        deleted = False,
        can_edit = True,
    )

    assert response.status_code == 201
    assert response.json() == expected

    response = client.get(
        "/users/test/collections/new",
        headers = user_headers,
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_create_other_collection(client, user_headers):
    collection = dict(
        name = "new",
        title = "A new collection",
        public = True,
        std_fields = [
            dict(
                name = "test",
                type = "text",
            ),
        ],
    )

    response = client.post(
        "/users/admin/collections",
        json = collection,
        headers = user_headers,
    )

    assert response.status_code == 403
    assert "detail" in response.json()


def test_create_duplicate_collection(client, user_headers):
    collection = dict(
        name = "new",
        title = "A new collection",
        public = True,
        std_fields = [
            dict(
                name = "test",
                type = "text",
            ),
        ],
    )

    response = client.post(
        "/users/test/collections",
        json = collection,
        headers = user_headers,
    )

    assert response.status_code == 201

    response = client.post(
        "/users/test/collections",
        json = collection,
        headers = user_headers,
    )

    assert response.status_code == 403
    assert "detail" in response.json()


def test_update_owned_collection(client, user_headers):
    collection = dict(
        name = "new-name",
        title = "A renamed collection",
        public = True,
        std_fields = [
            dict(
                name = "foo",
                type = "bar",
            ),
        ],
    )

    response = client.put(
        "/users/test/collections/test",
        json = collection,
        headers = user_headers,
    )

    expected = dict(
        **collection,
        id = test_test_col.id,
        owner = test_user.id,
        deleted = False,
        can_edit = True,
    )

    assert response.status_code == 200
    assert response.json() == expected

    response = client.get(
        "/users/test/collections/new-name",
        headers = user_headers,
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_update_private_collection(client, user_headers):
    collection = dict(
        name = "new-name",
        title = "A renamed collection",
        public = True,
        std_fields = [
            dict(
                name = "foo",
                type = "bar",
            ),
        ],
    )

    response = client.put(
        "/users/admin/collections/private",
        json = collection,
        headers = user_headers,
    )

    assert response.status_code == 404
    assert "detail" in response.json()


def test_update_shared_collection(client, user_headers):
    collection = dict(
        name = "new-name",
        title = "A renamed collection",
        public = True,
        std_fields = [
            dict(
                name = "foo",
                type = "bar",
            ),
        ],
    )

    response = client.put(
        "/users/admin/collections/shared",
        json = collection,
        headers = user_headers,
    )

    assert response.status_code == 403
    assert "detail" in response.json()


def test_update_shared_edit_collection(client, user_headers):
    collection = dict(
        name = "new-name",
        title = "A renamed collection",
        public = True,
        std_fields = [
            dict(
                name = "foo",
                type = "bar",
            ),
        ],
    )

    response = client.put(
        "/users/admin/collections/shared-edit",
        json = collection,
        headers = user_headers,
    )

    expected = dict(
        **collection,
        id = admin_shared_edit_col.id,
        owner = admin_user.id,
        deleted = False,
        can_edit = True,
    )

    assert response.status_code == 200
    assert response.json() == expected

    response = client.get(
        "/users/admin/collections/new-name",
        headers = user_headers,
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_update_deleted_collection(client, user_headers):
    collection = dict(
        name = "new-name",
        title = "A renamed collection",
        public = True,
        std_fields = [
            dict(
                name = "foo",
                type = "bar",
            ),
        ],
    )

    response = client.put(
        "/users/test/collections/deleted",
        json = collection,
        headers = user_headers,
    )

    assert response.status_code == 404
    assert "detail" in response.json()


def test_update_inexistant_collection(client, user_headers):
    collection = dict(
        name = "new-name",
        title = "A renamed collection",
        public = True,
        std_fields = [
            dict(
                name = "foo",
                type = "bar",
            ),
        ],
    )

    response = client.put(
        "/users/test/collections/foobar",
        json = collection,
        headers = user_headers,
    )

    assert response.status_code == 404
    assert "detail" in response.json()


def test_delete_owned_collection(client, user_headers):
    response = client.delete(
        "/users/test/collections/test",
        headers = user_headers,
    )

    assert response.status_code == 200
    assert "detail" in response.json()

    response = client.get(
        "/users/test/collections/test",
        headers = user_headers,
    )

    assert response.status_code == 404
    assert "detail" in response.json()


def test_delete_private_collection(client, user_headers):
    response = client.delete(
        "/users/admin/collections/private",
        headers = user_headers,
    )

    assert response.status_code == 404
    assert "detail" in response.json()


def test_delete_public_collection(client, user_headers):
    response = client.delete(
        "/users/admin/collections/public",
        headers = user_headers,
    )

    assert response.status_code == 403
    assert "detail" in response.json()


def test_delete_shared_collection(client, user_headers):
    response = client.delete(
        "/users/admin/collections/shared",
        headers = user_headers,
    )

    assert response.status_code == 403
    assert "detail" in response.json()


def test_delete_shared_edit_collection(client, user_headers):
    response = client.delete(
        "/users/admin/collections/shared-edit",
        headers = user_headers,
    )

    assert response.status_code == 403
    assert "detail" in response.json()


def test_delete_deleted_collection(client, user_headers):
    response = client.delete(
        "/users/test/collections/deleted",
        headers = user_headers,
    )

    assert response.status_code == 404
    assert "detail" in response.json()


def test_delete_inexistant_collection(client, user_headers):
    response = client.delete(
        "/users/test/collections/foobar",
        headers = user_headers,
    )

    assert response.status_code == 404
    assert "detail" in response.json()


# Admin tests ------------------------------------------------------------------


def test_get_owned_public_collection_as_admin(client, admin_headers):
    response = client.get(
        "/users/admin/collections/public",
        headers = admin_headers,
    )

    expected = dict(
        **admin_public_col.dict(include={
            "id", "owner", "name", "title", "public", "std_fields", "deleted",
        }),
        can_edit = True,
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_get_owned_private_collection_as_admin(client, admin_headers):
    response = client.get(
        "/users/admin/collections/private",
        headers = admin_headers,
    )

    expected = dict(
        **admin_private_col.dict(include={
            "id", "owner", "name", "title", "public", "std_fields", "deleted",
        }),
        can_edit = True,
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_get_other_public_collection_as_admin(client, admin_headers):
    response = client.get(
        "/users/test/collections/public",
        headers = admin_headers,
    )

    expected = dict(
        **test_public_col.dict(include={
            "id", "owner", "name", "title", "public", "std_fields", "deleted",
        }),
        can_edit = True,
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_get_other_private_collection_as_admin(client, admin_headers):
    response = client.get(
        "/users/test/collections/test",
        headers = admin_headers,
    )

    expected = dict(
        **test_test_col.dict(include={
            "id", "owner", "name", "title", "public", "std_fields", "deleted",
        }),
        can_edit = True,
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_get_inexistant_collection_as_admin(client, admin_headers):
    response = client.get(
        "/users/admin/collections/foo",
        headers = admin_headers,
    )

    assert response.status_code == 404
    assert "detail" in response.json()


def test_get_owned_collections_as_admin(client, admin_headers):
    response = client.get(
        "/users/admin/collections",
        headers = admin_headers,
    )

    expected = [
        dict(
            **admin_public_col.dict(),
            can_edit = True,
        ),
        dict(
            **admin_private_col.dict(),
            can_edit = True,
        ),
        dict(
            **admin_shared_col.dict(),
            can_edit = True,
        ),
        dict(
            **admin_shared_edit_col.dict(),
            can_edit = True,
        ),
    ]

    assert response.status_code == 200
    assert response.json() == expected


def test_get_other_collections_as_admin(client, admin_headers):
    response = client.get(
        "/users/test/collections",
        headers = admin_headers,
    )

    expected = [
        dict(
            **test_deleted_col.dict(),
            can_edit = True,
        ),
        dict(
            **test_public_col.dict(),
            can_edit = True,
        ),
        dict(
            **test_test_col.dict(),
            can_edit = True,
        ),
    ]

    assert response.status_code == 200
    assert response.json() == expected


def test_get_deleted_user_collections_as_admin(client, admin_headers):
    response = client.get(
        "/users/disabled/collections",
        headers = admin_headers,
    )

    expected = [
        dict(
            **disabled_public_col.dict(),
            can_edit = True,
        ),
    ]

    assert response.status_code == 200
    assert response.json() == expected


def test_create_owned_collection_as_admin(client, admin_headers):
    collection = dict(
        name = "new",
        title = "A new collection",
        public = True,
        std_fields = [
            dict(
                name = "foo",
                type = "bar",
            ),
        ],
    )

    response = client.post(
        "/users/admin/collections",
        json = collection,
        headers = admin_headers,
    )

    expected = dict(
        **collection,
        id = response.json()["id"],
        owner = admin_user.id,
        deleted = False,
        can_edit = True,
    )

    assert response.status_code == 201
    assert response.json() == expected

    response = client.get(
        "/users/admin/collections/new",
        headers = admin_headers,
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_create_other_collection_as_admin(client, admin_headers):
    collection = dict(
        name = "new",
        title = "A new collection",
        public = True,
        std_fields = [
            dict(
                name = "foo",
                type = "bar",
            ),
        ],
    )

    response = client.post(
        "/users/test/collections",
        json = collection,
        headers = admin_headers,
    )

    expected = dict(
        **collection,
        id = response.json()["id"],
        owner = test_user.id,
        deleted = False,
        can_edit = True,
    )

    assert response.status_code == 201
    assert response.json() == expected

    response = client.get(
        "/users/test/collections/new",
        headers = admin_headers,
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_create_duplicate_collection_as_admin(client, admin_headers):
    collection = dict(
        name = "new",
        title = "A new collection",
        public = True,
        std_fields = [
            dict(
                name = "foo",
                type = "bar",
            ),
        ],
    )

    response = client.post(
        "/users/admin/collections",
        json = collection,
        headers = admin_headers,
    )

    assert response.status_code == 201

    response = client.post(
        "/users/admin/collections",
        json = collection,
        headers = admin_headers,
    )

    assert response.status_code == 403
    assert "detail" in response.json()


def test_update_owned_collection_as_admin(client, admin_headers):
    collection = dict(
        name = "new-name",
        title = "A renamed collection",
        public = True,
        std_fields = [
            dict(
                name = "foo",
                type = "bar",
            ),
        ],
    )

    response = client.put(
        "/users/admin/collections/private",
        json = collection,
        headers = admin_headers,
    )

    expected = dict(
        **collection,
        id = admin_private_col.id,
        owner = admin_user.id,
        deleted = False,
        can_edit = True,
    )

    assert response.status_code == 200
    assert response.json() == expected

    response = client.get(
        "/users/admin/collections/new-name",
        headers = admin_headers,
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_update_private_collection_as_admin(client, admin_headers):
    collection = dict(
        name = "new-name",
        title = "A renamed collection",
        public = True,
        std_fields = [
            dict(
                name = "foo",
                type = "bar",
            ),
        ],
    )

    response = client.put(
        "/users/test/collections/test",
        json = collection,
        headers = admin_headers,
    )

    expected = dict(
        **collection,
        id = test_test_col.id,
        owner = test_user.id,
        deleted = False,
        can_edit = True,
    )

    assert response.status_code == 200
    assert response.json() == expected

    response = client.get(
        "/users/test/collections/new-name",
        headers = admin_headers,
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_update_deleted_collection_as_admin(client, admin_headers):
    collection = dict(
        name = "new-name",
        title = "A renamed collection",
        public = True,
        std_fields = [
            dict(
                name = "foo",
                type = "bar",
            ),
        ],
    )

    response = client.put(
        "/users/disabled/collections/public",
        json = collection,
        headers = admin_headers,
    )

    expected = dict(
        **collection,
        id = disabled_public_col.id,
        owner = disabled_user.id,
        deleted = False,
        can_edit = True,
    )

    assert response.status_code == 200
    assert response.json() == expected

    response = client.get(
        "/users/disabled/collections/new-name",
        headers = admin_headers,
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_update_inexistant_collection_as_admin(client, admin_headers):
    collection = dict(
        name = "new-name",
        title = "A renamed collection",
        public = True,
        std_fields = [
            dict(
                name = "foo",
                type = "bar",
            ),
        ],
    )

    response = client.put(
        "/users/test/collections/foobar",
        json = collection,
        headers = admin_headers,
    )

    assert response.status_code == 404
    assert "detail" in response.json()


def test_delete_owned_collection_as_admin(client, admin_headers):
    response = client.delete(
        "/users/admin/collections/private",
        headers = admin_headers,
    )

    assert response.status_code == 200
    assert "detail" in response.json()

    response = client.get(
        "/users/admin/collections/private",
        headers = admin_headers,
    )

    assert response.status_code == 200
    assert response.json()["deleted"] is True


def test_delete_private_collection_as_admin(client, admin_headers):
    response = client.delete(
        "/users/test/collections/test",
        headers = admin_headers,
    )

    assert response.status_code == 200
    assert "detail" in response.json()

    response = client.get(
        "/users/test/collections/test",
        headers = admin_headers,
    )

    assert response.status_code == 200
    assert response.json()["deleted"] is True


def test_delete_public_collection_as_admin(client, admin_headers):
    response = client.delete(
        "/users/test/collections/public",
        headers = admin_headers,
    )

    assert response.status_code == 200
    assert "detail" in response.json()

    response = client.get(
        "/users/test/collections/public",
        headers = admin_headers,
    )

    assert response.status_code == 200
    assert response.json()["deleted"] is True


def test_delete_deleted_collection_as_admin(client, admin_headers):
    response = client.delete(
        "/users/test/collections/deleted",
        headers = admin_headers,
    )

    assert response.status_code == 200
    assert "detail" in response.json()


def test_delete_inexistant_collection_as_admin(client, admin_headers):
    response = client.delete(
        "/users/test/collections/foobar",
        headers = admin_headers,
    )

    assert response.status_code == 404
    assert "detail" in response.json()
