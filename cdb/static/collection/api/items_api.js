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

import ApiError from "../../api/api_error.js";


export default class ItemsApi {
	constructor(api, path = "/item") {
		this.api  = api;
		this.path = path;
	}

	fetchItems() {
		return [
			{
				id: 1,
				name: "hello",
				label: "Hello World!",
			},
			{
				id: 2,
				name: "foo",
				label: "Foo",
			},
			{
				id: 3,
				name: "bar",
				label: "Bar",
			},
		];
		// return this.api.fetchAndGet(this.path, "items");
	}
}
