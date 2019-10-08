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

import { areObjectsEqual, isString, flatten } from "./util.js";
import { domElement as de } from "./element.js";
import Model from "./model.js";


function splitAttrs(attrs) {
	const elemAttrs = {};
	const viewAttrs = {};

	for(const [key, value] of Object.entries(attrs)) {
		if(key.startsWith("on")) {
			viewAttrs[key] = value;
		}
		else {
			elemAttrs[key] = value;
		}
	}

	return [elemAttrs, viewAttrs];
}


export default class View {
	constructor(app, props) {
		this.app = app;
		this.props = null;

		this._needUpdate = true;
		this._models = new Map();
		this._children = new Map();
		this._childrenPool = new Map();
		this._element = null;
		this._initialized = false;

		this.setProps(props);
	}

	setProps(props) {
		if(this._needUpdate || !areObjectsEqual(props, this.props)) {
			this.props = props;

			this._models.clear();
			for(const value of Object.values(this.props)) {
				if(value instanceof Model) {
					this._models.set(value, value.version());
				}
			}

			this._needUpdate = true;
		}
	}

	updateModelsVersion() {
		for(const model of Object.keys(this._models)) {
			this._models[model] = model.version();
		}
	}

	needUpdate() {
		if(this._needUpdate) {
			return true;
		}

		for(const {model, version} of this._models) {
			if(model.version() !== version) {
				return true;
			}
		}

		for(const child of this._children.values()) {
			if(child.needUpdate()) {
				return true;
			}
		}

		return false;
	}

	moveChildrenToPool() {
		const emptyMap = this._childrenPool;
		this._childrenPool = this._children;
		this._children = emptyMap;
	}

	destroyUnusedChildren() {
		for(const child of this._childrenPool.values()) {
			child.destroy();
		}
		this._childrenPool.clear();
	}

	renderChild(key, view, props) {
		const allProps = {
			key,
			...props,
		};
		let child = this._childrenPool.get(key);
		if(child !== undefined && Object.getPrototypeOf(child) === view.prototype) {
			child.setProps(allProps);
			this._childrenPool.delete(key);
		}
		else {
			child = new view(this.app, allProps);
			child.initialize();
		}
		this._children.set(key, child);
		child._render();
		return child._element;
	}

	element() {
		return this._element;
	}

	initialize() {
		if(this._initialized) {
			throw Error("Cannot initialize: View already initialized.");
		}

		this._initialized = true;
	}

	destroy() {
		if(!this._initialized) {
			throw Error("Cannot destroy: View is not initialized.");
		}

		this._models = [];
		this._children.clear();
		this._childrenPool.clear();
		this._element = null;
		this._initialized = false;
	}

	_render() {
		if(!this._initialized) {
			throw Error("View is not initialized.");
		}
		if(!this.needUpdate()) {
			return this._element;
		}

		this.moveChildrenToPool();
		this._element = this.renderElement(this.render());
		this.destroyUnusedChildren();

		this._needUpdate = false;
		this.updateModelsVersion();

		if(this.props.key !== undefined) {
			this._element.key = this.props.key;
			this._element.setAttribute("data-key", this.props.key);
		}

		return this._element;
	}

	renderElement(elem) {
		if(isString(elem)) {
			return document.createTextNode(elem);
		}
		if(isString(elem.tag)) {
			const [elemAttrs, viewAttrs] = splitAttrs(elem.attrs);
			const domElem = de(elem.tag, elemAttrs);
			for(const child of flatten(elem.children)) {
				const childElem = this.renderElement(child);
				domElem.appendChild(childElem);
			}
			for(const [key, value] of Object.entries(viewAttrs)) {
				if(key.startsWith("on")) {
					domElem.addEventListener(key.slice(2).toLowerCase(), value);
				}
			}
			return domElem;
		}
		else {
			// TODO: support child elements ?
			return this.renderChild(elem.attrs.key, elem.tag, elem.attrs);
		}
	}
}
