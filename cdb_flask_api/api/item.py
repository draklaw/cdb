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
