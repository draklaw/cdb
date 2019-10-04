#!/usr/bin/env python3

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
