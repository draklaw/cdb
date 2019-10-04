import os
import tempfile
import warnings

import pytest

from sqlalchemy.exc import SADeprecationWarning

from cdb import create_app, db
from cdb.db import User, Collection, UserCollection, Item

from utils import api_post


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    warnings.filterwarnings("ignore", category=SADeprecationWarning,
        message="The create_engine.convert_unicode parameter and corresponding dialect-level parameters are deprecated")
    warnings.filterwarnings("ignore", category=SADeprecationWarning,
        message="Use .persist_selectable")

    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///{}".format(db_path),
    })

    def fill_test_db():
        db.create_all()

        def add_user(username, password, email, is_admin=False):
            user = User.create_user(username, password, email, is_admin)
            db.session.add(user)
            return user

        def add_collection(owner, name, label):
            coll = Collection(owner_id=owner.id, name=name, label=label)
            db.session.add(coll)
            return coll

        def add_user_collection(user, collection, is_admin):
            uc = UserCollection(
                is_admin=is_admin
            )
            uc.user = user
            uc.collection = collection
            return uc

        def add_item(collection, name, label):
            item = Item(collection_id=collection.id, name=name, label=label)
            db.session.add(item)
            return item

        def add_n_items(collection, label, count):
            for i in range(count):
                fmt_label = label.format(index=i)
                fmt_name = fmt_label.lower().replace(" ", "_")
                add_item(collection, fmt_name, fmt_label)

        admin = add_user("admin", "password", "admin@foo.com", True)
        user = add_user("user", "123", "user@foo.com", False)
        add_user("john_doe", "hello", "john.doe@foo.com", False)

        db.session.commit()

        shared_admin_coll = add_collection(admin, "shared_admin", "Shared Admin Collection")
        shared_user_coll = add_collection(user, "shared_user", "Shared User Collection")
        user_coll = add_collection(user, "test", "Test Collection")

        add_user_collection(admin, shared_admin_coll, True)
        add_user_collection(admin, shared_user_coll, False)
        add_user_collection(user, user_coll, True)
        add_user_collection(user, shared_admin_coll, False)
        add_user_collection(user, shared_user_coll, True)

        add_n_items(shared_admin_coll, "Admin Item {index}", 5)
        add_n_items(shared_user_coll, "User Item {index}", 24)
        add_n_items(user_coll, "User Item {index}", 12)

        db.session.commit()

    try:
        with app.app_context():
            fill_test_db()
    except:
        pass
    else:
        yield app
    finally:
        with app.app_context():
            db.session.rollback()
        os.close(db_fd)
        os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


def connect_user(client, username, password):
    return api_post(client, "/api/login", field="user", data={
        "username": username,
        "password": password,
    })


@pytest.fixture
def admin(client):
    yield connect_user(client, "admin", "password")


@pytest.fixture
def user(client):
    yield connect_user(client, "user", "123")


@pytest.fixture
def john(client):
    yield connect_user(client, "john_doe", "hello")
