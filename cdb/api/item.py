from flask_restful import Resource, fields, marshal

from ..db import Item


item_fields = {
    "id":    fields.Integer,
    "name":  fields.String,
    "label": fields.String,
}


class ItemApi(Resource):
    def get(self, name=None):
        if name is None:
            return self.get_item_list()
        return self.get_item_by_name(name)

    def get_item_list(self):
        items = Item.query.all()
        return {
            "success": True,
            "items": marshal(items, item_fields),
        }

    def get_item_by_name(self, name):
        item = Item.query.filter(Item.name == name).one()
        return {
            "success": True,
            "item": marshal(item, item_fields),
        }
