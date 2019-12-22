<template>
	<form
		v-on:sumbit.prevent=""
		class="cdbHeaderForm"
	>
		<input
			v-model="value.label"
			v-on:input="updateName"
			class="cdbHeaderFormLabel"
			required
		>
		<input
			v-model="value.name"
			class="cdbHeaderFormName"
			required
			pattern="\w*"
		>
		<select v-model="value.type" class="cdbHeaderFormType">
			<option>text</option>
			<option>number</option>
			<option>date</option>
		</select>
		<input
			v-model="value.columnIndex"
			type="number"
			class="cdbHeaderFormColumn"
			required
		>

		<push-button
			v-if="deleteButton"
			v-on:click="$emit('delete', value)"
			look="negative"
		>
			Remove
		</push-button>
		<push-button
			v-else
			v-on:click="$emit('add', value)"
			look="positive"
		>
			Add
		</push-button>
	</form>
</template>


<script>
import { toIdentifier } from '@/utils'
import PushButton from '@/components/PushButton.vue'

export default{
	components: {
		PushButton,
	},
	props: {
		value: {
			default() {
				return {
					label: "",
					name: "",
					type: "text",
					columnIndex: -1,
				}
			},
			type: Object,
		},
		deleteButton: {
			default: false,
			type: Boolean,
		},
	},
	computed: {
	},
	methods: {
		updateName() {
			this.value.name = toIdentifier(this.value.label)
		},
	},
}
</script>


<style lang="scss">

.cdbHeaderForm {
	display: flex;
	width: 100%;

	.cdbHeaderFormLabel {
		flex: 1;
	}

	.cdbHeaderFormName {
		flex: 1;
	}
}
</style>
