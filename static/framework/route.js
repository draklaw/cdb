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


const _fragmentRe = /^<(?:(\w*):)?(\w*)>$/u;

const _typePatterns = {
	string: "([^/]*)",
};

export class Route {
	constructor(route) {
		if(route.length === 0) {
			throw Error("Empty route.");
		}
		if(route[0] !== "/") {
			throw Error("Route must start with a /.");
		}

		const fragments = route.split("/").slice(1);

		const reParts = [ "^" ];
		this._ids = [];
		for(const frag of fragments) {
			const match = frag.match(_fragmentRe);
			if(!match) {
				reParts.push(frag);
			}
			else {
				const [, type = "string", id] = match;
				const pattern = _typePatterns[type];
				if(!pattern) {
					throw Error(`Unsupported type "${type}."`);
				}
				reParts.push(pattern);
				this._ids.push(id);
			}
		}

		this._routeRe = new RegExp(reParts.join("/") + "$", "u");
	}

	match(path) {
		const match = path.match(this._routeRe);
		if(!match) {
			return null;
		}

		const kwargs = {};
		for(const [i, arg] of match.slice(1).entries()) {
			kwargs[this._ids[i]] = arg;
		}

		return kwargs;
	}
}

export class RouteMapping {
	constructor() {
		this._routes = [];
	}

	addRoute(route, value) {
		this._routes.push([ new Route(route), value ]);
	}

	get(path) {
		for(const [route, value] of this._routes) {
			const match = route.match(path);
			if(match !== null) {
				return {
					value,
					args: match,
				};
			}
		}
		return {
			value: null,
			args: {},
		};
	}
}
