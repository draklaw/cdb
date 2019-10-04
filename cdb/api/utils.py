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

from functools import wraps

from flask_restful import abort


def api_error(status_code, message, data={}):
    abort(status_code, message=message, success=False, **data)


def bad_request_error(message=None, code=400):
    api_error(code, message or "Bad request")


def unauthorized_error(message=None, code=401):
    api_error(code, message or "Unauthorized")


def forbidden_error(message=None, code=403):
    api_error(code, message or "Forbidden")


def not_found_error(message=None, code=404):
    api_error(code, message or "Not Found")


def get_first(it, default=None):
    try:
        return next(it)
    except StopIteration:
        return default


class ErrorConverter:
    def __init__(self, error_map):
        self.error_map = error_map

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except BaseException as err:
                new_error = get_first(
                    ne
                    for etype in type(err).__mro__
                    for ne in (self.error_map.get(etype),)
                    if ne
                )
                if new_error:
                    raise new_error(err) from err
                raise
        return wrapper
