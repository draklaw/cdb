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
from starlette.testclient import TestClient

import cdb_api


cdb_api.settings.test = True


def get_connection_token(client, username, password):
    response = client.post(
        "/token",
        data = dict(
            grant_type = "password",
            username = username,
            password = password,
        ),
    )

    assert response.status_code == 200

    json = response.json()

    assert "access_token" in json
    assert json["token_type"] == "Bearer"

    return json["access_token"]


@pytest.fixture(scope="session")
def client_no_rollback(setup_database):
    with TestClient(cdb_api.app) as client:
        yield client


@pytest.fixture(scope="session")
def user_headers_no_rollback(client_no_rollback):
    token = get_connection_token(client_no_rollback, "test", "123")
    return dict(
        Authorization = f"Bearer {token}",
    )


@pytest.fixture(scope="session")
def admin_headers_no_rollback(client_no_rollback):
    token = get_connection_token(client_no_rollback, "admin", "password")
    return dict(
        Authorization = f"Bearer {token}",
    )


@pytest.fixture()
def client(client_no_rollback):
    trx = cdb_api.db.database.transaction()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(trx.start())
    yield client_no_rollback
    loop.run_until_complete(trx.rollback())


@pytest.fixture()
def user_headers(client, user_headers_no_rollback):
    return user_headers_no_rollback


@pytest.fixture()
def admin_headers(client, admin_headers_no_rollback):
    return admin_headers_no_rollback
