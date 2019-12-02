<template>
	<table>
		<thead>
			<tr>
				<th
					v-for="field in fields"
					v-bind:key="field.id"
					v-bind:style="{
						minWidth: field.width > 0? field.width + 'em': null,
						width: field.width < 0? (-field.width / totalStretch * 100) + '%': null,
					}"
				>
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
	props: ["items", "fields"],
	computed: {
		totalStretch() {
			let totalStretch = 0
			for(const field of this.fields) {
				if(field.width < 0)
					totalStretch -= field.width
			}
			return totalStretch
		},
	},
	methods: {
		getField(item, field) {
			const path = field.split(".")
			for(const attr of path)
				item = item[attr]
			return item
		},
	},
}
</script>
