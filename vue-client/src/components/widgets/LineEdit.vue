<template>
	<div class="cdbFormField">
		<label v-bind:for="inputId">{{ label }}</label>
		<input
			v-bind:for="inputId"
			v-bind:value="value"
			v-on:input="$emit('input', $event.target.value)"
			v-bind:placeholder="label"
			v-bind="$attrs"
		>
	</div>
</template>


<script>
export default {
	inheritAttrs: false,
	data() {
		return {
		}
	},
	props: {
		id: String,
		label: String,
		value: String,
	},
	computed: {
		inputId() {
			return `${this.id}Input`
		}
	},
}
</script>


<style lang="scss">
@import "@/style/globals.scss";

.cdbFormField {
	margin-bottom: $medium-margin;

	label {
		display: block;
		font-size: 80%;
	}

	input {
		width: 100%;
		padding: $small-margin;
		box-sizing: border-box;

		border: 1px solid $light-border-color;
		border-radius: $small-margin;

		&:focus {
			border-color: $medium-border-color;
		}
	}
}
</style>
