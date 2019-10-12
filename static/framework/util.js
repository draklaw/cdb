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


export function isString(obj) {
	return (typeof obj === "string") || (obj instanceof String);
}

export function removeAllChildren(element) {
	while(element.lastChild) {
		element.removeChild(element.lastChild);
	}
}

export function areObjectsEqual(obj0, obj1) {
	for(const [key, value0] of Object.entries(obj0)) {
		if(obj1[key] !== value0) {
			return false;
		}
	}

	for(const key of Object.entries(obj1)) {
		if(obj0[key] === undefined) {
			return false;
		}
	}

	return true;
}

export function* map(iterable, func) {
	for(const item of iterable) {
		yield func(item);
	}
}

export function* flatten(iterable) {
	if(iterable[Symbol.iterator] !== undefined && !isString(iterable)) {
		for(const item of iterable) {
			yield* flatten(item);
		}
	}
	else {
		yield iterable;
	}
}

export function* filter(iterable, predicate) {
	for(const item of iterable) {
		if(predicate(item)) {
			yield item;
		}
	}
}
