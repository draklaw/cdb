// This file is part of cdb.
//
// Copyright (C) 2019  the authors (see AUTHORS)
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as
// published by the Free Software Foundation, either version 3 of the
// License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

import Module from "../framework/module.js";

import ItemsApi from "./api/items_api.js";
import ItemsList from "./models/items_list.js";
import { ShowCollection } from "./actions/item.js";


export default class CollectionModule extends Module {
	constructor() {
		super("collection");

		this.api = {
			items: api => new ItemsApi(api),
		};

		this.model = {
			items: model => new ItemsList(model),
		};

		this.routes = [
			[ "/items", () => new ShowCollection() ],
		];
	}
}
