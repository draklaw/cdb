export default class ApiError extends Error {
	constructor(message, extra = {}, ...args) {
		super(message, ...args);

		this.url = null;
		this.status = null;

		Object.assign(this, extra);
	}
}
