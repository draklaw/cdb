<template>
	<page>
		<template v-if="collection">
			<h2>{{ collection.title }}</h2>
			<input
				type="text"
				v-model="searchQuery"
				placeholder="Search"
			/>
			<button v-on:click="openNewItemPane">
				New item
			</button>
			<cdb-table
				v-bind:items="filteredItems"
				v-bind:fields="collection.fields"
				class="cdbCollectionTable"
			/>
		</template>
		<div v-else>
			Loading...
		</div>
	</page>
</template>

<script>
import store from '@/store'

import Page from '@/components/Page.vue'
import CdbTable from '@/components/CdbTable.vue'

export default {
	name: 'collection',
	components: {
		Page,
		CdbTable,
	},
	data() {
		return {
			store,
			loaded: false,
			searchQuery: "",
		}
	},
	computed: {
		username() {
			return this.$route.params.username
		},
		collectionName() {
			return this.$route.params.collection
		},
		collection() {
			return this.store.getCollection(this.username, this.collectionName)
		},
		filteredItems() {
			if(this.searchQuery === "")
				return this.collection.items

			const query = this.searchQuery.toLowerCase()
			return this.collection.items.filter(
				item => {
					const title = item.title.toLowerCase()
					return title.includes(query)
				}
			)
		},
	},
	methods: {
		async update() {
			await this.store.fetchCollection(this.username, this.collectionName)
		},
		openNewItemPane() {
			console.warn("openNewItemPane not implemented.")
		},
	},
	created() {
		this.update()
	},
}
</script>



<style lang="scss">
</style>
