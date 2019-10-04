import { domElement as de } from "../framework/element.js";
import View from "../framework/view.js";

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

		if(this._element)
			return this._element;

		this._usernameInput = de("input", {
			type: "text",
			name: "username",
			placeholder: "Username",
		});

		this._passwordInput = de("input", {
			type: "password",
			name: "password"
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
		)

		this._form.addEventListener("submit", this._boundLogin);

		this._element = this._form;
		return this._element;
	}

	_login(event) {
		event.preventDefault();
		this.loginCallback(
			this._form["username"].value,
			this._form["password"].value
		);
	}
}
