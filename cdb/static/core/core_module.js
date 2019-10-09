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

import Module from "../framework/module.js";

import LoginApi from "./api/login_api.js";
import LoginModel from "./models/login_model.js";
import MessageBox from "./models/message_box.js";
// import { ShowSignIn } from "./actions/login.js";


export default class CoreModule extends Module {
	constructor() {
		super("login");

		this.api = {
			login: api => new LoginApi(api),
		};

		this.model = {
			login: model => new LoginModel(model),
			messageBox: model => new MessageBox(model),
		};

		this.routes = [
			// [ "/signin", () => new ShowSignIn() ],
			// [ "/signup", () => new ShowSignUp() ],
		];
	}
}
