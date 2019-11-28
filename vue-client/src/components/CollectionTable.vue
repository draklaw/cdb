<template>
	<table>
		<thead>
			<tr>
				<th v-for="header in headers" v-bind:key="header.id">
					{{ header.label }}
				</th>
			</tr>
		</thead>
		<tbody>
			<tr v-for="item in collection.items" v-bind:key="item.id">
				<td v-for="header in headers" v-bind:key="header.id">
					{{ getField(item, header.field) }}
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
	props: ["collection", "headers"],
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
