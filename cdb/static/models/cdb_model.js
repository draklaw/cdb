import Model from "../framework/model.js";

import MessageBox from "./message_box.js";
import ItemsList from "./items_list.js";

export const loginStatus = {
	disconnected: "disconnected",
	pending:      "pending",
	connected:    "connected",
};

export default class CdbModel extends Model {
	constructor(parent) {
		super(parent);

		this.api = this._parent.api;

		this.title = "Cdb";

		this.messageBox = new MessageBox(this);

		this.user = null;
		this.loginStatus = loginStatus.disconnected;
		this.loginAttempts = 0;

		this.items = new ItemsList(this);
	}
}
