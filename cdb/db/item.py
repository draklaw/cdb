from .db import db


class Item(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey("collection.id"))
    name          = db.Column(db.String, index=True)
    label         = db.Column(db.String, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('collection_id', 'name', name='uq_item_collection_name'),
    )
