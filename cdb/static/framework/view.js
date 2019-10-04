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


import Model from "./model.js";

export default class View {
	constructor(app, props) {
		this.app = app;
		this.props = props;
		this._models = [];
		this._children = [];
		this._element = null;
		this._initialized = false;
	}

	addModel(model) {
		if(!(model instanceof Model)) {
			throw Error("View.addModel(): first parameter \"model\" must be of type \"Model\".");
		}

		this._models.push({
			model,
			version: 0,
		});
	}

	updateModelsVersion() {
		for(const model of this._models) {
			model.version = model.model.version();
		}
	}

	addChild(child) {
		if(!this._initialized) {
			throw Error("View must be initialized in order to add children.");
		}
		if(!(child instanceof View)) {
			throw Error("View.addChild(): first parameter \"child\" must be of type \"View\".");
		}
		if(this._children.find(c => c === child)) {
			throw Error("Child already added.");
		}

		this._children.push(child);
		child.initialize();
	}

	removeChild(child) {
		if(!this._children.find(c => c === child)) {
			throw Error("Child not found.");
		}

		child.destroy();
		this._children = this.children.filter(c => c === child);
	}

	removeAllChildren() {
		for(const child of this._children) {
			this.removeChild(child);
		}
	}

	needUpdate() {
		for(const {model, version} of this._models) {
			if(model.version() !== version) {
				return true;
			}
		}

		for(const child of this._children) {
			if(child.needUpdate()) {
				return true;
			}
		}

		return false;
	}

	element() {
		return this._element;
	}

	updateChild(child) {
		const prevElem = child._element;
		const elem = child.render();
		if(elem !== prevElem) {
			prevElem.parentElement.replaceChild(elem, prevElem);
		}
		return elem;
	}

	updateChildren() {
		for(const child of this._children) {
			this.updateChild(child);
		}
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

		this._initialized = false;
		this.removeAllChildren();
	}

	render() {
		if(!this._initialized) {
			throw Error("View is not initialized.");
		}
		if(!this.needUpdate()) {
			return this._element;
		}

		this.updateChildren();
		this.doRender();
		this.updateModelsVersion();

		return this._element;
	}

	doRender() {
	}
}
