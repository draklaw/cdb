#!/usr/bin/env python3

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
import os.path
from flask import Flask, url_for

from .db import db


def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = "dev",
        SQLALCHEMY_DATABASE_URI =
            "sqlite:///{}/cdb.sqlite".format(app.instance_path),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    from .commands import register_commands
    register_commands(app)

    from .api import create_api

    api_blueprint = create_api()
    app.register_blueprint(api_blueprint, url_prefix="/api")

    @app.route("/")
    def index(path = "/"):
        with app.open_resource("static/index.html", "r") as stream:
            index = stream.read()
        return index.format(
            lang="en",
            title="Collections",
            stylesheet=url_for("static", filename="style.css"),
            main_js=url_for("static", filename="cdb.js"))
    app.add_url_rule("/<path:path>", "index")

    return app
