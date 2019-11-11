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


from cdb_database.test_db import (
    test_user,
    admin_user,
    disabled_user,
)


# Unauthentified tests --------------------------------------------------------


def test_unauthentified_get_user_fail(client):
    response = client.get("/users/test")
    assert response.status_code == 401


def test_unauthentified_get_users_fail(client):
    response = client.get("/users")
    assert response.status_code == 401


def test_unauthentified_get_unknown_user_fail(client):
    response = client.get("/users/foobar")
    assert response.status_code == 401


# User tests ------------------------------------------------------------------


def test_get_user_self(client, user_headers):
    response = client.get(
        "/users/test",
        headers = user_headers,
    )

    expected = test_user.dict(include={"id", "username", "email", "is_admin"})

    assert response.status_code == 200
    assert response.json() == expected


def test_get_other_user(client, user_headers):
    response = client.get(
        "/users/admin",
        headers = user_headers,
    )

    expected = admin_user.dict(include={"id", "username"})

    assert response.status_code == 200
    assert response.json() == expected


def test_get_deleted_user(client, user_headers):
    response = client.get(
        "/users/disabled",
        headers = user_headers,
    )

    assert response.status_code == 404


def test_get_unknown_user(client, user_headers):
    response = client.get(
        "/users/foobar",
        headers = user_headers,
    )

    assert response.status_code == 404


def test_get_users(client, user_headers):
    response = client.get(
        "/users",
        headers = user_headers,
    )

    assert response.status_code == 200
    assert response.json() == [
        admin_user.dict(include={"id", "username"}),
        test_user.dict(include={"id", "username"}),
    ]


# Admin tests ------------------------------------------------------------------


def test_get_user_self_as_admin(client, admin_headers):
    response = client.get(
        "/users/admin",
        headers = admin_headers,
    )

    expected = admin_user.dict(include={"id", "username", "email", "is_admin"})

    assert response.status_code == 200
    assert response.json() == expected


def test_get_other_user_as_admin(client, admin_headers):
    response = client.get(
        "/users/test",
        headers = admin_headers,
    )

    expected = test_user.dict(include={
        "id", "username", "email", "is_admin", "disabled"
    })

    assert response.status_code == 200
    assert response.json() == expected


def test_get_disabled_user_as_admin(client, admin_headers):
    response = client.get(
        "/users/disabled",
        headers = admin_headers,
    )

    expected = disabled_user.dict(include={
        "id", "username", "email", "is_admin", "disabled"
    })

    assert response.status_code == 200
    assert response.json() == expected


def test_get_unknown_user_as_admin(client, admin_headers):
    response = client.get(
        "/users/foobar",
        headers = admin_headers,
    )

    assert response.status_code == 404


def test_get_users_as_admin(client, admin_headers):
    response = client.get(
        "/users",
        headers = admin_headers,
    )

    assert response.status_code == 200
    assert response.json() == [
        admin_user.dict(include={"id", "username", "email", "is_admin", "disabled"}),
        disabled_user.dict(include={"id", "username", "email", "is_admin", "disabled"}),
        test_user.dict(include={"id", "username", "email", "is_admin", "disabled"}),
    ]
