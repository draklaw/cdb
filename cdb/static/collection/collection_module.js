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

import { ShowCollection } from "../actions/item.js";

import CollectionView from "./collection_view.js";


export default class CollectionModule {
	constructor() {
		this.app = null;

		this.routes = [
			[ "/items", () => new ShowCollection() ],
		];

		this.views = [
			[ "items", (app) => new CollectionView(app) ],
		];
	}

	register(app) {
		this.app = app;

		for(const [route, actionFactory] of this.routes) {
			this.app.addRoute(route, actionFactory);
		}

		for(const [viewName, viewFactory] of this.views) {
			this.app.addView(viewName, viewFactory(this.app));
		}
	}
}
