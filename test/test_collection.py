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

from utils import api_get, sql_dump


def test_collection_list_require_login(client):
    response = client.get("/api/collections/user")

    assert response.status_code == 401
    assert response.is_json
    json = response.get_json()
    assert not json["success"]


def test_collection_list_empty(client, john):
    collections = api_get(client, "/api/collections/john_doe", field="collections")

    assert not collections


def test_collection_list_owned(client, user):
    collections = api_get(client, "/api/collections/user", field="collections")

    assert len(collections) == 2
    assert collections[0]["name"] == "shared_user"
    assert collections[1]["name"] == "test"
    assert collections[0]["is_admin"]
    assert collections[1]["is_admin"]


def test_collection_list_shared(client, user):
    collections = api_get(client, "/api/collections/admin", field="collections")

    assert len(collections) == 1
    assert collections[0]["name"] == "shared_admin"
    assert not collections[0]["is_admin"]


def test_collection_get(client, user):
    collection = api_get(client, "/api/collections/user/test", field="collection")

    assert collection["name"] == "test"
    assert collection["is_admin"]


def test_collection_get_wrong_user(client, john):
    response = client.get("/api/collections/user/test")

    assert response.status_code == 404
    assert response.is_json
    json = response.get_json()
    assert not json["success"]


def test_collection_admin_access_all(client, admin):
    collection = api_get(client, "/api/collections/user/test", field="collection")

    assert collection["name"] == "test"
    assert not collection["is_admin"]
