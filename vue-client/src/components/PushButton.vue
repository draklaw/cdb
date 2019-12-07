<template>
	<button
		v-bind:class="['cdbButton', lookClass]"
		v-on:click="$emit('click')"
		v-bind:type="type"
	>
		<slot></slot>
	</button>
</template>


<script>
export default {
	props: {
		type: {
			default: "button",
			type: String,
		},
		look: {
			default: "neutral",
			type: String,
		},
	},
	computed: {
		lookClass() {
			return "cdb" + this.look[0].toUpperCase() + this.look.slice(1) + "Button"
		}
	},
}
</script>


<style lang="scss">
@import "@/style/globals.scss";

.cdbButton {
	padding: $small-margin $medium-margin;

	border: none;
	border-radius: $small-margin;

	&:hover {
		filter: brightness(1.1);
	}
}

.cdbPositiveButton {
	background-color: $positive-color;
}

.cdbNegativeButton {
	background-color: $negative-color;
}

.cdbNeutralButton {
	background-color: $neutral-color;
}
</style>
