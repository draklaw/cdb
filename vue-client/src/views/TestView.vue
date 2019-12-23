<template>
	<div id="cdbTestView">
		<h2>Test title</h2>
		<line-edit v-model="lineEdit" id="cdbLineEdit" label="Title" />
		<checkbox v-model="checkbox" id="cdbCheckbox" label="A checkbox" />
		<div>
			<push-button
				look="positive"
				v-bind:busy="checkbox"
				v-on:click="clickCount += 1"
				style="display: inline-block;"
			>
				Button
			</push-button>
			Click count {{ clickCount }}
		</div>
	</div>
</template>

<script>
import { LineEdit, Checkbox, PushButton } from "@/components/widgets"

export default {
	components: {
		LineEdit,
		Checkbox,
		PushButton,
	},
	data() {
		return {
			lineEdit: "",
			checkbox: true,
			clickCount: 0,
		}
	},
	methods: {
	},
}
</script>


<style lang="scss">
@import "@/style/globals.scss";

#cdbTestView {
	width: 40rem;
	margin: auto;
}
</style>
