<template>
	<form
		v-on:sumbit.prevent=""
		class="cdbHeaderForm"
	>
		<input
			v-model="value.label"
			v-on:input="updateName"
			class="cdbHeaderFormLabel"
			placeholder="Label"
			required
		>
		<input
			v-model="value.name"
			class="cdbHeaderFormName"
			placeholder="Name"
			pattern="\w*"
			required
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

		<button
			v-if="deleteButton"
			v-on:click="$emit('delete', value)"
		>
			Remove
		</button>
		<button
			v-else
			v-on:click="$emit('add', value)"
		>
			Add
		</button>
	</form>
</template>


<script>
import { toIdentifier } from '@/utils'

export default{
	components: {
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
</style>
