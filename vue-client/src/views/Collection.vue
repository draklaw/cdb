<template>
	<div>
		<template v-if="loaded">
			<h2>{{ collection.title }}</h2>
			<search-field v-model="searchQuery" />
			<collection-table
				v-if="loaded"
				v-bind:items="filteredItems"
				v-bind:fields="collection.fields"
			/>
		</template>
		<loading v-else />
	</div>
</template>

<script>
import store from '@/store/store.js'

import Loading from '@/components/Loading.vue'
import CollectionTable from '@/components/CollectionTable.vue'
import SearchField from '@/components/SearchField.vue'

export default {
	name: 'collection',
	components: {
		Loading,
		CollectionTable,
		SearchField,
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
		}
	},
	methods:{
		async update() {
			this.loaded = false
			await this.store.fetchCollection(this.username, this.collectionName)
			this.loaded = true
		}
	},
	async created() {
		await this.update()
	}
}
</script>
