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
