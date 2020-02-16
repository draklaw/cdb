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
</style>
