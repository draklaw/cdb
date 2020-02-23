<template>
	<div>
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

		<button
			v-on:click.prevent="$emit('delete', value)"
		>
			Remove
		</button>
	</div>
</template>


<script>
export default{
	components: {
	},
	props: {
		value: {
			default() {
				return {
					name: "",
					type: "text",
				}
			},
			type: Object,
		},
	},
	computed: {
	},
	methods: {
	},
}
</script>


<style lang="scss">
</style>
