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

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN
from fastapi import FastAPI

from . import settings, db, user, collection

from cdb_database.error import NotFoundError, AlreadyExistsError


app = FastAPI(
    title = "CDB",
    description = "A generic collection database.",
    version = "0.1.0",
    openapi_prefix = settings.api_prefix,
    debug = settings.debug,
)

app.include_router(user.router)
app.include_router(collection.router)

# test_transaction = None


@app.on_event("startup")
async def connect_to_database():
    await db.setup_database()


@app.on_event("shutdown")
async def disconnect_from_database():
    await db.teardown_database()


@app.middleware("http")
async def convert_db_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except NotFoundError:
        return JSONResponse(
            status_code = HTTP_404_NOT_FOUND,
            content = dict(
                detail = f"Ressource {request.url} does not exists",
            )
        )
    except AlreadyExistsError:
        return JSONResponse(
            status_code = HTTP_403_FORBIDDEN,
            content = dict(
                detail = f"Ressource already exists",
            )
        )
