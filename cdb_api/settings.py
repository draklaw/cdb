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

import databases
from starlette.datastructures import Secret
from starlette.config import Config


config = Config(".env")

debug = config(
    "CDB_DEBUG",
    cast = bool,
    default = False
)

api_prefix = config(
    "CDB_API_PREFIX",
    cast = str,
    default = "/api"
)

database_url = config(
    "CDB_DATABASE",
    cast = databases.DatabaseURL
)

access_token_duration_in_minutes = config(
    "CDB_ACCESS_TOKEN_DURATION_IN_MINUTES",
    cast = int,
    default = 30,
)

token_secret_key = config(
    "CDB_TOKEN_SECRET_KEY",
    cast = Secret,
)

token_algorithm = config(
    "CDB_TOKEN_ALGORITHM",
    cast = str,
    default = "HS256",
)
