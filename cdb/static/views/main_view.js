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

import { domElement as de } from "../framework/element.js";
import View from "../framework/view.js";

import MessageBoxView from "./message_box_view.js";
import LoginFormView from "./login_form_view.js";


export default class MainView extends View {
	constructor(app, props) {
		super();

		this._app = app;
		this.addModel(this._app);

		this.messageBox = new MessageBoxView(this._app.messageBox);
		this.loginForm = new LoginFormView(props.loginCallback);
	}

	initialize() {
		super.initialize();

		this.addChild(this.messageBox);
		this.addChild(this.loginForm);

		this._userBox =

		this._element = de("div", { class: "cdbApp" },
			de("header", { class: "cdbHeader" },
				de("h1", {}, this._app.title)
			),
			this.messageBox.element(),
			this.loginForm.element()
		);

		return this._element;
	}
}
