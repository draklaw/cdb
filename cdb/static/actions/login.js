import Action from "../framework/action.js";

import { loginStatus } from "../models/cdb_model.js";

export class CompleteLogin extends Action {
	constructor(user) {
		super();

		this.user = user;
	}

	describe() {
		return `CompleteLogin(${this.user.username})`;
	}

	exec(controller) {
		const model = controller.model;

		model.user = this.user;
		model.loginStatus = loginStatus.connected;
		model.loginAttempts = 0;

		model.messageBox.setMessage("success", `Logged as ${model.user.username}`);
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
		const model = controller.model;

		model.loginStatus = loginStatus.disconnected;
		model.loginAttempts += 1;

		model.messageBox.setMessage("error", `Login failed: ${this.error}`);
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

		if(model.loginStatus !== loginStatus.disconnected) {
			throw Error(`Cannot send login when login status is ${model.loginStatus}.`);
		}
		model.loginStatus = loginStatus.pending;

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
		const model = controller.model;

		model.user = null;
		model.loginStatus = loginStatus.disconnected;

		model.messageBox.setMessage("success", "Logged-out.");
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
		const model = controller.model;

		model.loginStatus = loginStatus.connected;

		model.messageBox.setMessage("error", `Failed to log-out: ${this.errors}.`);
	}
}

export class SendLogout extends Action {
	constructor() {
		super();
	}

	async exec(controller) {
		const { model, api } = controller;

		if(model.loginStatus !== loginStatus.disconnected) {
			throw Error(`Cannot send login when login status is ${model.loginStatus}.`);
		}
		model.loginStatus = loginStatus.pending;

		try {
			await api.logout();
			model.exec(new CompleteLogout());
		}
		catch(error) {
			model.exec(new FailLogout(error));
		}
	}
}
