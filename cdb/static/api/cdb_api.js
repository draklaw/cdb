import ApiError from "./api_error.js";
import ItemsApi from "./items_api.js";

export default class CdbApi {
	constructor(url) {
		this.url = url;

		this.items = new ItemsApi(this);
	}

	getUrl(path) {
		return this.url + path;
	}

	fetchOnly(path, init={}) {
		const headers = (init.headers !== undefined)? init.headers: new Headers();
		if(!headers.has("Content-Type")) {
			headers.set("Content-Type", "application/json");
		}

		const url = this.getUrl(path);
		console.log("apiFetch:", url, init);
		try {
			return fetch(url, {
				...init,
				headers,
			});
		}
		catch(error) {
			throw new ApiError(`Network error: ${error.message}.`, { url });
		}
	}

	async fetch(path, init = {}) {
		const response = await this.fetchOnly(path, init);
		this.checkResponse(response, path);
		return this.getJson(response, path);
	}

	async fetchAndGet(path, field, init = {}) {
		const json = await this.fetch(path, init);

		if(!json.success) {
			throw new ApiError(json.message);
		}

		if(!json[field]) {
			throw new ApiError(`Invalid response: missing field "${field}".`);
		}

		return json[field];
	}

	checkResponse(response, path) {
		if(!response.ok) {
			throw new ApiError(
				`Error ${response.status}: ${response.statusText}.`,
				{ url: this.getUrl(path), status: response.status},
			);
		}
	}

	getJson(response, path) {
		try {
			return response.json();
		}
		catch(error) {
			throw new ApiError(
				`Json error: ${error.message}.`,
				{ url: this.getUrl(path) },
			);
		}
	}

	login(username, password) {
		return this.fetchAndGet("/login", "user", {
			method: "POST",
			body: JSON.stringify({ username, password }),
		});
	}

	logout() {
		return this.fetch("/logout");
	}

}
