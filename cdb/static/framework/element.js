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

import { isString } from "./util.js";


export function domElement(tag, attrs = {}, ...children) {
	const elem = document.createElement(tag);

	for(const [k, v] of Object.entries(attrs)) {
		elem.setAttribute(k, v);
	}

	for(let child of children) {
		if(isString(child)) {
			child = document.createTextNode(child);
		}

		elem.appendChild(child);
	}

	return elem;
}

export class Element {
	constructor(tag, attrs = {}, ...children) {
		this.tag = tag;
		this.attrs = attrs;
		this.children = children;
		this.domNode = null;
		this.map = {};
	}
}

export function ce(tag, attrs = {}, ...children) {
	return new Element(tag, attrs, ...children);
}

// export class ElementMap {
// 	constructor(elementFactory) {
// 		this._elementFactory = elementFactory;
// 		this._map = new Map();
// 	}
//
// 	map(items, props) {
// 		const newMap = new Map();
// 		for(let item of items) {
// 			let elem = this._map.get(item);
// 			if(elem === undefined)
// 				elem = this._elementFactory()
// 		}
// 	}
// }
