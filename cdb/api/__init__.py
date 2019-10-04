import sqlalchemy.orm.exc

from flask import Blueprint
from flask_restful import Api, Resource

from .utils import not_found_error, ErrorConverter
from .login import LoginApi, LogoutApi
from .user import UserApi
from .collection import CollectionApi
from .item import ItemApi


class ApiNotFound(Resource):
    def dispatch_request(self, *args, **kwargs):
        not_found_error()


def create_api():
    error_converter = ErrorConverter({
        sqlalchemy.orm.exc.NoResultFound:
            lambda e: not_found_error(),
    })

    blueprint = Blueprint("cdbApi", __name__)
    api = Api(
        blueprint,
        serve_challenge_on_401=True,
        decorators=[error_converter],
    )

    api.add_resource(LoginApi, "/login")
    api.add_resource(LogoutApi, "/logout")
    api.add_resource(UserApi, "/users", "/users/<username>")
    api.add_resource(
        CollectionApi,
        "/collections/<username>",
        "/collections/<username>/<col_name>",
    )
    # api.add_resource(ItemApi, "/item", "/item/<name>")

    api.add_resource(ApiNotFound, "/", "/<path:path>")
    # def api_not_found(path=None):
        # apiError(404, "Resource does not exists.")

    return blueprint
