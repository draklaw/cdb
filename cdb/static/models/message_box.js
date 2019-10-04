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
