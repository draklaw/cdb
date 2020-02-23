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
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from . import settings, db, user, collection, item, field

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
app.include_router(item.router)
app.include_router(field.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:8080", "http://localhost:8081"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)
# test_transaction = None


@app.on_event("startup")
async def connect_to_database():
    await db.setup_database()


@app.on_event("shutdown")
async def disconnect_from_database():
    await db.teardown_database()


@app.exception_handler(NotFoundError)
def not_found_error_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        {
            "detail": f"Ressource {request.url} does not exists",
        },
        status_code = HTTP_404_NOT_FOUND,
    )


@app.exception_handler(AlreadyExistsError)
def already_exsits_error_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        {
            "detail": str(exc),
        },
        status_code = HTTP_403_FORBIDDEN,
    )
