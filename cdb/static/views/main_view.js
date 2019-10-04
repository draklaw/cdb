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
