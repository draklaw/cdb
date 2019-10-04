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
