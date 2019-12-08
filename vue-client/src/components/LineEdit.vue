<template>
	<div class="cdbFormField">
		<label v-bind:for="inputId">{{ label }}</label>
		<input
			v-bind:for="inputId"
			v-bind:value="value"
			v-on:input="$emit('input', $event.target.value)"
			v-bind:autofocus="autofocus"
			v-bind:placeholder="label"
			v-bind:type="password? 'password': 'text'"
			v-bind:required="required"
		>
	</div>
</template>


<script>
export default {
	data() {
		return {
		}
	},
	props: {
		id: String,
		label: String,
		value: String,
		autofocus: {
			default: false,
			type: Boolean,
		},
		password: {
			default: false,
			type: Boolean,
		},
		required: {
			default: false,
			type: Boolean,
		}
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

		background-color: rgb(255, 255, 255);

		&:focus {
			border-color: $medium-border-color;
		}
	}
}
</style>
