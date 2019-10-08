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

import Model from "../framework/model.js";

import MessageBox from "./message_box.js";
import ItemsList from "../collection/models/items_list.js";


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
