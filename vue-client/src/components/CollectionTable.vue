<template>
	<table>
		<thead>
			<tr>
				<th v-for="field in fields" v-bind:key="field.id">
					{{ field.label }}
				</th>
			</tr>
		</thead>
		<tbody>
			<tr v-for="item in items" v-bind:key="item.id">
				<td v-for="field in fields" v-bind:key="field.id">
					{{ getField(item, field.field) }}
				</td>
			</tr>
		</tbody>
	</table>
</template>


<script>
export default{
	data() {
		return {
		}
	},
	props: ["items", "fields"],
	methods: {
		getField(item, field) {
			const path = field.split(".")
			for(const attr of path)
				item = item[attr]
			return item
		}
	},
}
</script>
