from .db import db


class UserCollection(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey("user.id"))
    collection_id = db.Column(db.Integer, db.ForeignKey("collection.id"))
    is_admin      = db.Column(db.Boolean)

    def __repr__(self):
        return "<UserCollection {id} user={user_id} col={collection_id} is_admin={is_admin}".format(**self.__dict__)
