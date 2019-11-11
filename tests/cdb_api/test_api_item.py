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
    admin_private_items,
    admin_shared_items,
    admin_shared_edit_items,
    admin_public_items,
    test_test_items,
    test_public_items,
    test_deleted_items,
    disabled_public_items,
)


# Unauthentified tests --------------------------------------------------------


def test_unauthentified_get_item_fail(client):
    response = client.get("/users/test/collections/test/items/item_03")
    assert response.status_code == 401
    assert "detail" in response.json()


def test_unauthentified_create_item_fail(client):
    response = client.post(
        "/users/test/collections/test/items",
        json = dict(
            name = "new-item",
            title = "New item",
        )
    )
    assert response.status_code == 401
    assert "detail" in response.json()


# User tests ------------------------------------------------------------------


def test_get_item_in_owned_public_collection(client, user_headers):
    response = client.get(
        "/users/test/collections/public/items/item_03",
        headers = user_headers,
    )

    assert response.status_code == 200
    assert response.json() == test_public_items[2].dict()


def test_get_item_in_owned_private_collection(client, user_headers):
    response = client.get(
        "/users/test/collections/test/items/item_03",
        headers = user_headers,
    )

    assert response.status_code == 200
    assert response.json() == test_test_items[2].dict()


def test_get_item_in_other_public_collection(client, user_headers):
    response = client.get(
        "/users/admin/collections/public/items/item_03",
        headers = user_headers,
    )

    assert response.status_code == 200
    assert response.json() == admin_public_items[2].dict()


def test_get_item_in_other_private_collection(client, user_headers):
    response = client.get(
        "/users/admin/collections/private/items/item_03",
        headers = user_headers,
    )

    assert response.status_code == 404
    assert "detail" in response.json()


def test_get_item_in_other_shared_collection(client, user_headers):
    response = client.get(
        "/users/admin/collections/shared/items/item_03",
        headers = user_headers,
    )

    assert response.status_code == 200
    assert response.json() == admin_shared_items[2].dict()


def test_get_item_in_other_shared_edit_collection(client, user_headers):
    response = client.get(
        "/users/admin/collections/shared-edit/items/item_03",
        headers = user_headers,
    )

    assert response.status_code == 200
    assert response.json() == admin_shared_edit_items[2].dict()


def test_get_inexistant_item(client, user_headers):
    response = client.get(
        "/users/test/collections/test/items/foobar",
        headers = user_headers,
    )

    assert response.status_code == 404
    assert "detail" in response.json()


def test_get_items_in_owned_public_collection(client, user_headers):
    response = client.get(
        "/users/test/collections/public/items",
        headers = user_headers,
    )

    expected = [
        item.dict()
        for item in sorted(test_public_items, key=lambda i: i.title)
    ]

    assert response.status_code == 200
    assert response.json() == expected


def test_get_items_in_owned_private_collection(client, user_headers):
    response = client.get(
        "/users/test/collections/test/items",
        headers = user_headers,
    )

    expected = [
        item.dict()
        for item in sorted(test_test_items, key=lambda i: i.title)
    ]

    assert response.status_code == 200
    assert response.json() == expected


def test_get_items_in_other_public_collection(client, user_headers):
    response = client.get(
        "/users/admin/collections/public/items",
        headers = user_headers,
    )

    expected = [
        item.dict()
        for item in sorted(admin_public_items, key=lambda i: i.title)
    ]

    assert response.status_code == 200
    assert response.json() == expected


def test_get_items_in_other_private_collection(client, user_headers):
    response = client.get(
        "/users/admin/collections/private/items",
        headers = user_headers,
    )

    assert response.status_code == 404
    assert "detail" in response.json()


def test_get_items_in_other_shared_collection(client, user_headers):
    response = client.get(
        "/users/admin/collections/shared/items",
        headers = user_headers,
    )

    expected = [
        item.dict()
        for item in sorted(admin_shared_items, key=lambda i: i.title)
    ]

    assert response.status_code == 200
    assert response.json() == expected


def test_get_items_in_other_shared_edit_collection(client, user_headers):
    response = client.get(
        "/users/admin/collections/shared-edit/items",
        headers = user_headers,
    )

    expected = [
        item.dict()
        for item in sorted(admin_shared_edit_items, key=lambda i: i.title)
    ]

    assert response.status_code == 200
    assert response.json() == expected


def test_create_item_in_owned_collection(client, user_headers):
    item_dict = dict(
        name = "new-item",
        title = "New item",
    )

    response = client.post(
        "/users/test/collections/test/items",
        json = item_dict,
        headers = user_headers,
    )

    expected = dict(
        **item_dict,
        id = response.json()["id"],
        collection = test_test_col.id,
        deleted = False,
    )

    assert response.status_code == 201
    assert response.json() == expected

    response = client.get(
        "/users/test/collections/test/items/new-item",
        headers = user_headers,
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_create_item_in_other_public_collection(client, user_headers):
    item_dict = dict(
        name = "new-item",
        title = "New item",
    )

    response = client.post(
        "/users/admin/collections/public/items",
        json = item_dict,
        headers = user_headers,
    )

    assert response.status_code == 403
    assert "detail" in response.json()


def test_create_item_in_other_private_collection(client, user_headers):
    item_dict = dict(
        name = "new-item",
        title = "New item",
    )

    response = client.post(
        "/users/admin/collections/private/items",
        json = item_dict,
        headers = user_headers,
    )

    assert response.status_code == 404
    assert "detail" in response.json()


def test_create_item_in_other_shared_collection(client, user_headers):
    item_dict = dict(
        name = "new-item",
        title = "New item",
    )

    response = client.post(
        "/users/admin/collections/shared/items",
        json = item_dict,
        headers = user_headers,
    )

    assert response.status_code == 403
    assert "detail" in response.json()


def test_create_item_in_other_shared_edit_collection(client, user_headers):
    item_dict = dict(
        name = "new-item",
        title = "New item",
    )

    response = client.post(
        "/users/admin/collections/shared-edit/items",
        json = item_dict,
        headers = user_headers,
    )

    expected = dict(
        **item_dict,
        id = response.json()["id"],
        collection = admin_shared_edit_col.id,
        deleted = False,
    )

    assert response.status_code == 201
    assert response.json() == expected

    response = client.get(
        "/users/admin/collections/shared-edit/items/new-item",
        headers = user_headers,
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_update_item_in_owned_private_collection(client, user_headers):
    item_dict = dict(
        name = "new-item",
        title = "New item",
    )

    response = client.put(
        "/users/test/collections/test/items/item_03",
        json = item_dict,
        headers = user_headers,
    )

    expected = dict(
        **item_dict,
        id = test_test_items[2].id,
        collection = test_test_col.id,
        deleted = False,
    )

    assert response.status_code == 200
    assert response.json() == expected

    response = client.get(
        "/users/test/collections/test/items/new-item",
        headers = user_headers,
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_update_item_in_owned_public_collection(client, user_headers):
    item_dict = dict(
        name = "new-item",
        title = "New item",
    )

    response = client.put(
        "/users/test/collections/public/items/item_03",
        json = item_dict,
        headers = user_headers,
    )

    expected = dict(
        **item_dict,
        id = test_public_items[2].id,
        collection = test_public_col.id,
        deleted = False,
    )

    assert response.status_code == 200
    assert response.json() == expected

    response = client.get(
        "/users/test/collections/public/items/new-item",
        headers = user_headers,
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_update_item_in_other_private_collection(client, user_headers):
    item_dict = dict(
        name = "new-item",
        title = "New item",
    )

    response = client.put(
        "/users/admin/collections/private/items/item_03",
        json = item_dict,
        headers = user_headers,
    )

    assert response.status_code == 404
    assert "detail" in response.json()


def test_update_item_in_other_public_collection(client, user_headers):
    item_dict = dict(
        name = "new-item",
        title = "New item",
    )

    response = client.put(
        "/users/admin/collections/public/items/item_03",
        json = item_dict,
        headers = user_headers,
    )

    assert response.status_code == 403
    assert "detail" in response.json()


def test_update_item_in_other_shared_collection(client, user_headers):
    item_dict = dict(
        name = "new-item",
        title = "New item",
    )

    response = client.put(
        "/users/admin/collections/shared/items/item_03",
        json = item_dict,
        headers = user_headers,
    )

    assert response.status_code == 403
    assert "detail" in response.json()


def test_update_item_in_other_shared_edit_collection(client, user_headers):
    item_dict = dict(
        name = "new-item",
        title = "New item",
    )

    response = client.put(
        "/users/admin/collections/shared-edit/items/item_03",
        json = item_dict,
        headers = user_headers,
    )

    expected = dict(
        **item_dict,
        id = admin_shared_edit_items[2].id,
        collection = admin_shared_edit_col.id,
        deleted = False,
    )

    assert response.status_code == 200
    assert response.json() == expected

    response = client.get(
        "/users/admin/collections/shared-edit/items/new-item",
        headers = user_headers,
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_delete_item_owned_private_collection(client, user_headers):
    response = client.delete(
        "/users/test/collections/test/items/item_03",
        headers = user_headers,
    )

    assert response.status_code == 200
    assert "detail" in response.json()


def test_delete_item_owned_public_collection(client, user_headers):
    response = client.delete(
        "/users/test/collections/public/items/item_03",
        headers = user_headers,
    )

    assert response.status_code == 200
    assert "detail" in response.json()


def test_delete_item_other_private_collection(client, user_headers):
    response = client.delete(
        "/users/admin/collections/private/items/item_03",
        headers = user_headers,
    )

    assert response.status_code == 404
    assert "detail" in response.json()


def test_delete_item_other_public_collection(client, user_headers):
    response = client.delete(
        "/users/admin/collections/public/items/item_03",
        headers = user_headers,
    )

    assert response.status_code == 403
    assert "detail" in response.json()


def test_delete_item_other_shared_collection(client, user_headers):
    response = client.delete(
        "/users/admin/collections/shared/items/item_03",
        headers = user_headers,
    )

    assert response.status_code == 403
    assert "detail" in response.json()


def test_delete_item_other_shared_edit_collection(client, user_headers):
    response = client.delete(
        "/users/admin/collections/shared-edit/items/item_03",
        headers = user_headers,
    )

    assert response.status_code == 200
    assert "detail" in response.json()


# Admin tests -----------------------------------------------------------------
