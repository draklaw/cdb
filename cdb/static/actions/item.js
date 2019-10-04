import Action from "../framework/action.js";


export class SetItems extends Action {
	constructor(items) {
		super();

		this.items = items;
	}

	describe() {
		return `SetItems(${this.items.length} items)`;
	}

	exec(controller) {
		const { model } = controller;

		model.items.setItems(this.items);
	}
}

export class FetchItems extends Action {
	constructor() {
		super();
	}

	async exec(controller) {
		const { api } = controller;

		const items = await api.items.fetchItems();
		controller.exec(new SetItems(items));
	}
}

export class ShowCollection extends Action {
	constructor() {
		super();
	}

	exec(controller) {
		controller.setMainView("items");
		controller.exec(new FetchItems());
	}
}
