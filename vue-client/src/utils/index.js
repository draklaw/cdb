

export function capitalize(string) {
	return string[0].toUpperCase() + string.slice(1).toLowerCase()
}

export function toIdentifier(string) {
	return string.toLowerCase().replace(/[^\w]/g, "_")
}
