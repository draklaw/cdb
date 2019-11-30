<template>
	<input
		v-model="value"
		v-on:input="$emit('input', $event.target.value)"
		placeholder="Search"
	/>
</template>


<script>
export default {
	data() {
		return {
		}
	},
	props: {
		value: String,
	},
}
</script>
