import { domElement as de } from "../framework/element.js";
import View from "../framework/view.js";

import ItemsTableView from "./items_table_view.js";


export default class CollectionView extends View {
	constructor(app, props = {}) {
		super(app, props);

		this.table = new ItemsTableView(this.app);
	}

	initialize() {
		super.initialize();

		this.addChild(this.table);

		this._element = de("div", { class: "cdbCollection" },
			this.table.element(),
		);
	}
}
