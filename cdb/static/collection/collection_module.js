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
