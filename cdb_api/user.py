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

from fastapi import APIRouter

from cdb_database import user as user_db

from .db import Database, transaction


router = APIRouter()


@router.get("/user/me")
def get_logged_user():
    return dict(result="TODO")


@router.get("/user/{username}", response_model=user_db.UserPublic)
async def get_user(username: str, db: Database = transaction):
    # TODO: ACL

    return await user_db.get_user(db, username=username)
