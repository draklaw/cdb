import ApiError from "./api_error.js";

export default class ItemsApi {
	constructor(api, path = "/item") {
		this.api  = api;
		this.path = path;
	}

	fetchItems() {
		return this.api.fetchAndGet(this.path, "items");
	}
}
