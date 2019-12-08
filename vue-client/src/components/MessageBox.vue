<template>
	<div class="cdbMessageBox">
		<div
			v-for="[index, message] in messages.entries()"
			v-bind:key="index"
			v-bind:class="messageClasses(message)"
		>
			{{ message.message }}
		</div>
	</div>
</template>


<script>
import { capitalize } from "@/utils"

export default {
	props: {
		messages: Array,
	},
	methods: {
		messageClasses(message) {
			return [
				"cdbMessage",
				`cdbMessage${message.type? capitalize(message.type): 'Info'}`,
			]
		}
	}
}
</script>


<style lang="scss">
@import "@/style/globals.scss";

.cdbMessageBox {
	margin-bottom: $medium-margin;

	.cdbMessage {
		padding: $small-margin;

		background-color: $light-background-color;
		border: 1px solid $light-border-color;
		border-radius: $small-margin;
	}

	.cdbMessagePositive {
		background-color: $positive-background-color;
	}

	.cdbMessageNegative {
		background-color: $negative-background-color;
	}
}
</style>
