def log_as_admin(client):
    response = client.post(
        "/api/login",
        data={
            "username": "admin",
            "password": "password",
        }
    )

    assert response.status_code == 200
    assert response.is_json

    return response.get_json()["user"]


def test_login_admin_success(client):
    response = client.post(
        "/api/login",
        data={
            "username": "admin",
            "password": "password",
        }
    )

    assert response.status_code == 200
    assert response.is_json
    json = response.get_json()
    assert json["success"]
    user = json["user"]
    assert user["id"] != 0
    assert user["username"] == "admin"
    assert user["email"] == "admin@foo.com"
    assert user["is_admin"]

    response = client.get("/api/users/admin")

    assert response.status_code == 200

    response = client.get("/api/logout")

    assert response.status_code == 200

    response = client.get("/api/users/admin")

    assert response.status_code == 401


def test_login_user_success(client):
    response = client.post(
        "/api/login",
        data={
            "username": "user",
            "password": "123",
        }
    )

    assert response.status_code == 200
    assert response.is_json
    json = response.get_json()
    assert json["success"]
    user = json["user"]
    assert user["id"] != 0
    assert user["username"] == "user"
    assert user["email"] == "user@foo.com"
    assert not user["is_admin"]


def test_login_wrong_password(client):
    response = client.post(
        "/api/login",
        data={
            "username": "admin",
            "password": "123",
        }
    )

    assert response.status_code == 403
    assert response.is_json
    json = response.get_json()
    assert not json["success"]
    assert json["message"]


def test_user_list(client):
    log_as_admin(client)

    response = client.get("/api/users")

    assert response.status_code == 200
    assert response.is_json
    json = response.get_json()
    assert json["success"]
    users = json["users"]
    assert isinstance(users, list)
    usernames = set([user["username"] for user in users])
    assert usernames == set(["admin", "john_doe", "user"])


def test_user_list_disconnected(client):
    response = client.get("/api/users")

    assert response.status_code == 401
    assert response.is_json
    json = response.get_json()
    assert not json["success"]
    assert json["message"]
