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


export default class MessageBox extends Model {
	constructor(parent) {
		super(parent);
		this._message = "";
		this._messageClass = "";
	}

	isMessageBoxVisible() {
		return this._message !== "";
	}

	messageClass() {
		return this._messageClass;
	}

	message() {
		return this._message;
	}

	setMessage(messageClass, message) {
		if(message === this._message && messageClass === this._messageClass) {
			return;
		}

		console.log(`${messageClass}: ${message}`);

		this._messageClass = messageClass;
		this._message = message;

		this.update();
	}

	clearMessage() {
		if(this._message === "") {
			return;
		}

		this._messageClass = "";
		this._message = "";

		this.update();
	}
}
