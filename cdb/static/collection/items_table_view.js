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

import { map } from "../framework/util.js";
import { ce } from "../framework/element.js";
import View from "../framework/view.js";


export default class ItemTableView extends View {
	constructor(app, props = {}) {
		super(app, props);
	}

	render() {
		const items = this.props.collection.items;

		return ce("table", { class: "cdbItemTable" },
			ce("thead", {},
				ce("tr", {},
					ce("th", {}, "Id"),
					ce("th", {}, "Name"),
					ce("th", {}, "Label"),
				),
			),
			map(Object.values(items), item =>
				ce("tr", {},
					ce("td", {}, `${item.id}`),
					ce("td", {}, item.name),
					ce("td", {}, item.label),
				),
			),
		);
	}
}
