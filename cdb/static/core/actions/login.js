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

import Action from "../../framework/action.js";

import { loginStatus } from "../models/login_model.js";


export class CompleteLogin extends Action {
	constructor(user) {
		super();

		this.user = user;
	}

	describe() {
		return `CompleteLogin(${this.user.username})`;
	}

	exec(controller) {
		const { login, messageBox } = controller.model;

		login.user = this.user;
		login.status = loginStatus.connected;
		login.attempts = 0;

		messageBox.setMessage("success", `Logged as ${login.user.username}`);
	}
}

export class FailLogin extends Action {
	constructor(error) {
		super();

		this.error = error;
	}

	describe() {
		return `FailLogin(${this.error})`;
	}

	exec(controller) {
		const { login, messageBox } = controller.model;

		login.status = loginStatus.disconnected;
		login.attempts += 1;

		messageBox.setMessage("error", `Login failed: ${this.error}`);
	}
}

export class SendLogin extends Action {
	constructor(username, password) {
		super();

		this.username = username;
		this.password = password;
	}

	describe() {
		return `SendLogin(${this.username}, ***)`;
	}

	async exec(controller) {
		const { model, api } = controller;
		const { login } = model;

		if(login.status !== loginStatus.disconnected) {
			throw Error(`Cannot send login when login status is ${login.status}.`);
		}
		login.status = loginStatus.pending;

		const username = this.username;
		const password = this.password;

		// Erase password to make sure we don't keep it around.
		this.password = null;

		try {
			const user = await api.login(username, password);
			controller.exec(new CompleteLogin(user));
		}
		catch(error) {
			controller.exec(new FailLogin(error));
		}
	}
}

export class CompleteLogout extends Action {
	constructor() {
		super();
	}

	exec(controller) {
		const { login, messageBox } = controller.model;

		login.user = null;
		login.status = loginStatus.disconnected;

		messageBox.setMessage("success", "Logged-out.");
	}
}

export class FailLogout extends Action {
	constructor(error) {
		super();

		this.error = error;
	}

	describe() {
		return `FailLogout(${this.error})`;
	}

	exec(controller) {
		const { login, messageBox } = controller.model;

		login.status = loginStatus.connected;

		messageBox.setMessage("error", `Failed to log-out: ${this.errors}.`);
	}
}

export class SendLogout extends Action {
	constructor() {
		super();
	}

	async exec(controller) {
		const { model, api } = controller;
		const { login } = model;

		if(login.status !== loginStatus.disconnected) {
			throw Error(`Cannot send login when login status is ${login.status}.`);
		}
		login.status = loginStatus.pending;

		try {
			await api.logout();
			model.exec(new CompleteLogout());
		}
		catch(error) {
			model.exec(new FailLogout(error));
		}
	}
}
