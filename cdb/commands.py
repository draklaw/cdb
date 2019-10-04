from getpass import getpass

import click
from flask.cli import AppGroup, with_appcontext

from .db import db, User, Collection, UserCollection, Item

_commands = []


def register_commands(app):
    for command in _commands:
        app.cli.add_command(command)


def command(*args, **kwargs):
    def decorator(f):
        cmd = click.command(*args, **kwargs)(with_appcontext(f))
        _commands.append(cmd)
        return cmd
    return decorator


def app_group(*args, **kwargs):
    grp = AppGroup(*args, **kwargs)
    _commands.append(grp)
    return grp


user_cmd = app_group("user")


@command()
def init_db():
    """Initialize the database."""
    db.create_all()


@user_cmd.command("add")
@click.option("-a", "--admin/--no-admin", default=False)
@click.argument("username")
@click.argument("email")
def add_user(username, email, admin):
    """Add a user."""

    password   = "foo"
    password2 = "bar"
    while password != password2:
        password = getpass("Password: ")
        password2 = getpass("Password (confirmation): ")

    User.create_user(
        username = username,
        email    = email,
        password = password,
        is_admin = admin,
    )


@user_cmd.command("delete")
@click.option("-u", "--username")
@click.option("-m", "--email")
@click.argument("id")
def delete_user(id, username, email):
    User.delete_user(id, username, email)


@command()
def make_test_db():
    confirm = False
    while not confirm:
        line = input("Drop all tables ? (Y/n) ").strip().lower()
        if line in ["", "y", "yes"]:
            confirm = True
        elif line in ["n", "no"]:
            print("Aborting.")
            return
        else:
            print("Please answer yes or no.")

    db.drop_all()
    db.create_all()

    def add_user(username, password, email, is_admin=False):
        user = User.create_user(username, password, email, is_admin)
        db.session.add(user)
        return user

    def add_collection(owner, name, label):
        collection = Collection(owner_id=owner.id, name=name, label=label)
        db.session.add(collection)
        return collection

    admin = add_user("admin", "password", "admin@foo.com", True)
    user = add_user("user", "123", "user@foo.com", False)

    db.session.commit()

    test_col = add_collection(admin, "test", "Test collection")
    admin.user_collections.append(UserCollection(
        collection=test_col, is_admin=True))

    shared_col = add_collection(user, "shared", "Shared collection")
    admin.user_collections.append(UserCollection(
        collection=shared_col, is_admin=False))
    user.user_collections.append(UserCollection(
        collection=shared_col, is_admin=True))

    def add_item(collection, name, label):
        item = Item(name=name, label=label)
        collection.items.append(item)
        return item

    add_item(test_col, "foo", "A Foo")
    add_item(test_col, "test", "This is a test.")
    add_item(test_col, "foobar", "aoeuaoeuaoeu")

    for i in range(200):
        add_item(shared_col, "item_{}".format(i), "Item {}".format(i))

    db.session.commit()
