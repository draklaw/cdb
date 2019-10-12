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

import { domElement as de } from "../../framework/element.js";
import View from "../../framework/view.js";


export default class MessageBoxView extends View {
	constructor(messageBox) {
		super();

		this._messageBox = messageBox;
		this.addModel(this._messageBox);

		this._text = null;
	}

	initialize() {
		super.initialize();

		if(this._element) {
			return this._element;
		}

		this._text = document.createTextNode("");
		this._element = de("div", {}, this._text);

		return this._element;
	}

	render() {
		super.render();

		const visible = this._messageBox.isMessageBoxVisible();
		this._element.hidden = !visible;
		if(visible) {
			this._element.className = this._messageBox.messageClass();
			this._text.textContent = this._messageBox.message();
		}

		return this._element;
	}
}
