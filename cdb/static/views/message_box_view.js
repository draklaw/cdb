import { domElement as de } from "../framework/element.js";
import View from "../framework/view.js";

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
