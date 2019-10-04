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
