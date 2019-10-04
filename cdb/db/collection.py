from .db import db


class Collection(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    owner_id    = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name        = db.Column(db.String, unique=True, index=True)
    label       = db.Column(db.String, nullable=False)
    template_id = db.Column(db.Integer)

    __table_args__ = (
        db.Index(
            "ix_collection_owner_name",
            "owner_id",
            "name"
        ),
    )

    def __repr__(self):
        return "<Collection {id} {owner_id}/{name}>".format(**self.__dict__)
