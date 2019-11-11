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

from typing import Optional, List
from datetime import datetime, timedelta

from passlib.context import CryptContext
import jwt
from jwt import PyJWTError
from pydantic import BaseModel, SecretStr
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from cdb_database import user as user_db
from cdb_database.error import NotFoundError

from . import settings
from .db import Database, transaction


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.api_prefix + "/token")

router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str


class UserInput(BaseModel):
    username: str
    email: str
    password: SecretStr


class UserPublic(BaseModel):
    id: int = ...
    username: str = ...
    email: str = None
    is_admin: bool = None
    disabled: bool = None


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


def create_access_token(*, data: dict, expires_delta: timedelta) -> str:
    """Creates a JWT token for user authentication."""

    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + expires_delta

    return jwt.encode(
        to_encode,
        str(settings.token_secret_key),
        algorithm = settings.token_algorithm,
    )


async def authenticate_user(
    db: Database,
    username: str,
    password: str,
) -> Optional[user_db.UserDb]:
    try:
        user = await user_db.get_user(db, username=username)
    except NotFoundError:
        return None

    if verify_password(password, user.hashed_password.get_secret_value()):
        return user
    return None


async def get_current_user_unchecked(
    token: str = Depends(oauth2_scheme),
    db: Database = transaction,
) -> user_db.UserDb:
    try:
        payload = jwt.decode(
            token,
            str(settings.token_secret_key),
            algorithms = [settings.token_algorithm]
        )
        user_id = payload.get("sub") if isinstance(payload, dict) else None
    except PyJWTError:
        user_id = None

    if user_id is not None:
        user = await user_db.get_user(db, user_id=user_id)
    else:
        user = None

    if user is None:
        raise HTTPException(
            status_code = HTTP_401_UNAUTHORIZED,
            detail = "Could not validate credentials",
            headers = {"WWW-Authenticate": "Bearer"},
        )

    return user


async def create_user(user: UserInput) -> user_db.UserDb:
    hashed_password = hash_password(user.password)
    db_user = user_db.UserDb(
        hashed_password = hashed_password,
        **user.dict(exclude={"password"}),
    )
    await user_db.create_user(db_user)


def get_current_user(
    user: user_db.UserDb = Depends(get_current_user_unchecked),
) -> user_db.UserDb:
    if user.disabled:
        raise HTTPException(
            status_code = HTTP_401_UNAUTHORIZED,
            detail = "Inactive user",
        )
    return user


def get_current_admin(
    user: user_db.UserDb = Depends(get_current_user),
) -> user_db.UserDb:
    if not user.is_admin:
        raise HTTPException(
            status_code = HTTP_401_UNAUTHORIZED,
            detail = "Unauthorized",
        )
    return user


current_user = Depends(get_current_user)
current_admin = Depends(get_current_admin)


def strip_user_info(user):
    return user.dict(include={"id", "username"})


@router.post(
    "/token",
    response_model = Token,
    tags = ["users"],
    summary = "Get authentication token",
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Database = transaction,
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code = HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password",
            headers = {"WWW-Authenticate": "Bearer"},
        )
    if user.disabled:
        raise HTTPException(
            status_code = HTTP_401_UNAUTHORIZED,
            detail = "User account disabled",
            headers = {"WWW-Authenticate": "Bearer"},
        )

    expires_delta = timedelta(
        minutes = settings.access_token_duration_in_minutes
    )
    token = create_access_token(
        data = dict(
            sub = user.id,
            username = user.username,
            email = user.email,
            is_admin = user.is_admin,
        ),
        expires_delta = expires_delta,
    )

    return dict(
        access_token = token,
        token_type = "Bearer",
    )


@router.get(
    "/users",
    response_model = List[UserPublic],
    response_model_skip_defaults = True,
    tags = ["users"],
    summary = "Get the list of all users",
)
async def get_users(
    logged_user: user_db.UserDb = current_user,
    db: Database = transaction,
):
    users = await user_db.get_users(
        db,
        include_disabled = logged_user.is_admin,
    )

    if not logged_user.is_admin:
        users = list(map(strip_user_info, users))

    return users


@router.get(
    "/users/{username}",
    response_model = UserPublic,
    response_model_skip_defaults = True,
    tags = ["users"],
    summary = "Get the user with the given username",
)
async def get_user(
    username: str,
    logged_user: user_db.UserDb = current_user,
    db: Database = transaction,
):
    target_user = await user_db.get_user(
        db,
        username = username,
        include_disabled = logged_user.is_admin,
    )

    if target_user.id == logged_user.id:
        del target_user.disabled
    elif not logged_user.is_admin:
        target_user = strip_user_info(target_user)

    return target_user
