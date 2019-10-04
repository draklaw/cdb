export default class Model {
	constructor(parent) {
		this._parent = parent;
		this._version = 1;
	}

	version() {
		return this._version;
	}

	update() {
		this._version += 1;
		this._parent.update();
	}

	updateAlone() {
		this._version += 1;
	}
}
