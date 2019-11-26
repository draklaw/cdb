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
					{{ item[header.field] }}
				</td>
			</tr>
		</tbody>
	</table>
</template>


<script>
	export default{
		data(){
			return{}
		},
		props:["collection", "headers"],
	}
</script>
