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

import { removeAllChildren } from "../framework/util.js";
import { domElement as de } from "../framework/element.js";
import View from "../framework/view.js";


export default class ItemTableView extends View {
	constructor(app, props = {}) {
		super(app, props);

		this.addModel(this.app.model.items);

		this._body = null;
	}

	initialize() {
		super.initialize();

		this._body = de("tbody", {});

		this._element = de("table", { class: "cdbItemTable" },
			de("thead", {},
				de("tr", {},
					de("th", {}, "Id"),
					de("th", {}, "Name"),
					de("th", {}, "Label"),
				),
			),
			this._body,
		);
	}

	doRender() {
		const items = this.app.model.items;

		removeAllChildren(this._body);

		for(const item of Object.values(items.items)) {
			this._body.appendChild(
				de("tr", {},
					de("td", {}, `${item.id}`),
					de("td", {}, item.name),
					de("td", {}, item.label),
				),
			);
		}
	}
}
