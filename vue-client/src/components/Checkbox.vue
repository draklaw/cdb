<template>
	<div class="cdbCheckbox">
		<input
			v-bind:id="inputId"
			v-on:change="$emit('input', $event.target.checked)"
			v-bind:checked="value"
			type="checkbox"
		>
		<label v-bind:for="inputId">
			{{ label }}
		</label>
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
		value: Boolean,
	},
	computed: {
		inputId() {
			return `${this.id}Input`
		},
	},
}
</script>


<style lang="scss">
@import "@/style/globals.scss";

.cdbCheckbox {
	margin-bottom: $medium-margin;

	input {
		position: absolute;
	}

	label {
		&::before {
			position: relative;
			bottom: 0.1em;

			display: inline-block;
			min-width: 1.2em;
			min-height: 1.2em;

			margin-right: $small-margin;

			background-color: $light-background-color;
			border: 1px solid $light-border-color;
			border-radius: $small-margin;

			text-align: center;
			vertical-align: middle;

			content: "";
		}

		&:hover::before {
			background-color: $light-background-color;
		}
	}

	input:focus ~ label::before {
		border-color: $medium-border-color;
	}

	input:checked ~ label::before {
		content: "\2713";
	}
}
</style>
