import Model from "../framework/model.js";

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
