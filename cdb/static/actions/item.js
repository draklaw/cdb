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

import Action from "../framework/action.js";


export class SetItems extends Action {
	constructor(items) {
		super();

		this.items = items;
	}

	describe() {
		return `SetItems(${this.items.length} items)`;
	}

	exec(controller) {
		const { model } = controller;

		model.items.setItems(this.items);
	}
}

export class FetchItems extends Action {
	constructor() {
		super();
	}

	async exec(controller) {
		const { api } = controller;

		const items = await api.items.fetchItems();
		controller.exec(new SetItems(items));
	}
}

export class ShowCollection extends Action {
	constructor() {
		super();
	}

	exec(controller) {
		controller.setMainView("items");
		controller.exec(new FetchItems());
	}
}
