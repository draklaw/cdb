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

import { RouteMapping } from "./framework/route.js";

import CdbApi from "./api/cdb_api.js";
import CdbModel from "./models/cdb_model.js";

import CollectionModule from "./collection/collection_module.js";

// import MainView from "./views/main_view.js";

// import { SendLogin } from "./actions/login.js";


class Cdb {
	constructor(parentElement) {
		this.api = new CdbApi("/api");
		this.model = new CdbModel(this);
		this.modules = [];

		this.routes = new RouteMapping();
		this.view = null;

		this._updatePending = false;
		this._boundDoUpdate = this.doUpdate.bind(this);

		this._parentElement = parentElement;
		this._element = null;

		this.logActions = true;

		this.register(new CollectionModule());

		this.goTo("/items");
	}

	goTo(path, query = {}, fragment = "") {
		const {
			value: actionFactory,
			args,
		} = this.routes.get(path);

		if(actionFactory === null) {
			console.warn(`Go to "${path}: Path not found."`);
			// TODO:
			return;
		}

		console.log(`Go to "${path}": ${args}.`);

		const action = actionFactory(args, query, fragment);
		this.exec(action);
	}

	register(module) {
		module.register(this);
		this.modules.push(module);
	}

	addRoute(route, actionFactory) {
		this.routes.addRoute(route, actionFactory);
	}

	addView(viewName, view) {
		this.views[viewName] = view;
	}

	exec(action) {
		if(this.logActions) {
			// eslint-disable-next-line no-console
			console.log(action.describe());
		}

		action.exec(this);
	}

	setMainView(view) {
		if(view === this.view) {
			return;
		}

		if(this.view) {
			this.view.destroy();
		}

		this.view = view;

		if(this.view) {
			this.view.initialize();
		}

		this.update();
	}

	update() {
		if(this._updatePending) {
			return;
		}

		setTimeout(this._boundDoUpdate);
		this._updatePending = true;
	}

	doUpdate() {
		this._updatePending = false;

		const elem = this.view._render();

		if(elem === this._element) {
			return;
		}

		if(this._element) {
			this._parentElement.replaceChild(elem, this._element);
		}
		else {
			this._parentElement.appendChild(elem);
		}

		this._element = elem;
	}
}

window.cdb = new Cdb(document.body);
