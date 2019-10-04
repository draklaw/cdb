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
