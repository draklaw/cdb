export function isString(obj) {
	return (typeof obj === "string") || (obj instanceof String);
}

export function removeAllChildren(element) {
	while(element.lastChild) {
		element.removeChild(element.lastChild);
	}
}
