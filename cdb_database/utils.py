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


def print_query(query):
    compiled = query.compile()
    print(compiled)
    print(compiled.params)


def raise_if_all_none(**kwargs):
    for value in kwargs.values():
        if value is not None:
            return
    arg_list = ", ".join(kwargs.keys())
    raise TypeError(f"One of the following argument must be set: {arg_list}")
