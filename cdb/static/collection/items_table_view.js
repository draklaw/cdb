import { removeAllChildren } from "../framework/util.js";
import { domElement as de } from "../framework/element.js";
import View from "../framework/view.js";


export default class ItemTableView extends View {
	constructor(app, props = {}) {
		super(app, props);

		this.addModel(this.app.model.items);

		this._body = null;
	}

	initialize() {
		super.initialize();

		this._body = de("tbody", {});

		this._element = de("table", { class: "cdbItemTable" },
			de("thead", {},
				de("tr", {},
					de("th", {}, "Id"),
					de("th", {}, "Name"),
					de("th", {}, "Label"),
				),
			),
			this._body,
		);
	}

	doRender() {
		const items = this.app.model.items;

		removeAllChildren(this._body);

		for(const item of Object.values(items.items)) {
			this._body.appendChild(
				de("tr", {},
					de("td", {}, `${item.id}`),
					de("td", {}, item.name),
					de("td", {}, item.label),
				),
			);
		}
	}
}
