<template>
	<page>
		<header>
			<h2>{{ collection.title }}</h2>
			<input
				type="text"
				v-model="searchQuery"
				placeholder="Search"
			/>
			<router-link
				to="/new-collection"
			>
				+
			</router-link>
		</header>
		<!-- <cdb-table
			v-bind:items="filteredItems"
			v-bind:fields="collection.fields"
			class="cdbCollectionTable"
		/> -->
	</page>
</template>

<script>
import store from '@/store/store.js'

import Page from '@/components/Page.vue'
// import CdbTable from '@/components/CdbTable.vue'

export default {
	name: 'collection',
	components: {
		Page,
		// CdbTable,
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
			this.store.loading = true
			await this.store.fetchCollection(this.username, this.collectionName)
			this.store.loading = false
		},
		showNewItemPane() {

		},
	},
	async created() {
		await this.update()
	},
}
</script>



<style lang="scss">
</style>
