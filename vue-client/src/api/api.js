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

export class ApiError extends Error {
	constructor(...args) {
		super(...args)
	}
}


export class Api {
	constructor(url) {
		this.url = url;
		this.token = null
	}

	getUrl(path) {
		return this.url + path;
	}

	async fetch(path, init={}) {
		const headers = (init.headers !== undefined)? init.headers: new Headers();

		if(this.token)
			headers.set("Authorization", "Bearer " + this.token)
		headers.set("Accept", "application/json")

		if(init.json)
			init.body = JSON.stringify(init.json)

		const url = this.getUrl(path);
		try {
			return await fetch(url, {
				...init,
				headers,
			});
		}
		catch(error) {
			throw new ApiError(`Network error: ${error.message}.`);
		}
	}

	async fetchJson(path, init = {}) {
		const response = await this.fetch(path, init);

		if(!response.ok) {
			if(response.status == 422)
				throw new ApiError("Unknown error")

			try {
				const json = await response.json()
				throw new ApiError(json.detail)
			}
			catch(error) {
				throw new ApiError(`${response.status} ${response.statusText}`)
			}
		}

		return await response.json();
	}

	getToken(username, password) {
		const body = new FormData()
		body.set("grant_type", "password")
		body.set("username", username)
		body.set("password", password)

		return this.fetchJson("/token", {
			method: "POST",
			body
		})
	}

	getUser(username) {
		return this.fetchJson(`/users/${username}`)
	}

	getUsers() {
		return this.fetchJson(`/users`)
	}

	getCollections(username, opts) {
		const {
			onlyOwned = true,
		} = opts

		return this.fetchJson(`/users/${username}/collections?only_owned=${onlyOwned}`)
	}

	createCollection(username, collection) {
		return this.fetchJson(`/users/${username}/collections`, {
			method: "POST",
			json: collection,
		})
	}

	getItems(username, collectionName) {
		return this.fetchJson(`/users/${username}/collections/${collectionName}/items`)
	}

	getFields(username, collectionName) {
		return this.fetchJson(`/users/${username}/collections/${collectionName}/fields`)
	}
}

export default new Api("http://localhost:8000/api")
