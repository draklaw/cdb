
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
