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
	constructor(loginCallback) {
		super();

		this.loginCallback = loginCallback;
		this._boundLogin = this._login.bind(this);

		this._form = null;
		this._usernameInput = null;
		this._passwordInput = null;
	}

	initialize() {
		super.initialize();

		if(this._element) {
			return this._element;
		}

		this._usernameInput = de("input", {
			type: "text",
			name: "username",
			placeholder: "Username",
		});

		this._passwordInput = de("input", {
			type: "password",
			name: "password",
		});

		this._form = de("form", { class: "cdbLoginForm" },
			de("label", {},
				de("div", { class: "cdbLoginFormLabel" },
					"Username:",
				),
				this._usernameInput
			),
			de("label", {},
				de("div", { class: "cdbLoginFormLabel" },
					"Password:",
				),
				this._passwordInput
			),
			de("input", { type: "submit", value: "Login" })
		);

		this._form.addEventListener("submit", this._boundLogin);

		this._element = this._form;
		return this._element;
	}

	_login(event) {
		event.preventDefault();
		this.loginCallback(
			this._form.username.value,
			this._form.password.value,
		);
	}
}
