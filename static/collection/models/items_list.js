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

import Model from "../../framework/model.js";


export class Item extends Model {
	constructor(parent) {
		super(parent);
	}

	set(item, options = {}) {
		const { propagateUpdate = true } = options;

		const { id, name, label } = item;
		const needUpdate = (
			id    !== this.id ||
			name  !== this.name ||
			label !== this.label
		);

		if(!needUpdate) {
			return;
		}

		this.id    = id;
		this.name  = name;
		this.label = label;

		if(propagateUpdate) {
			this.update();
		}
		else {
			this.updateAlone();
		}
	}
}

export default class ItemsList extends Model {
	constructor(parent) {
		super(parent);

		this.items = {};
	}

	setItems(items) {
		let needUpdate = false;

		for(const item of Object.values(this.items)) {
			if(items[item.name] === undefined) {
				delete this.items[item.name];
				needUpdate = true;
			}
		}

		for(const item of items) {
			if(this.items[item.name] === undefined) {
				this.items[item.name] = item;
				needUpdate = true;
			}
			else {
				this.item[item.name].set(item, { "propagateUpdate": false });
				needUpdate = true;
			}
		}

		if(needUpdate) {
			this.update();
		}
	}
}
