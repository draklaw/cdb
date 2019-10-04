import { isString } from "./util.js";

export function domElement(tag, attrs = {}, ...children) {
	const elem = document.createElement(tag);

	for(let [k, v] of Object.entries(attrs)) {
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
