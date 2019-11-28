<template>
	<div>
		<template v-if="loaded">
			<h2>{{ collection.title }}</h2>
			<collection-table
				v-if="loaded"
				v-bind:collection="collection"
				v-bind:headers="headers"
			/>
		</template>
		<loading v-else />
	</div>
</template>

<script>
import store from '@/store/store.js'

import Loading from '@/components/Loading.vue'
import CollectionTable from '@/components/CollectionTable.vue'

export default {
	name: 'collection',
	components: {
		Loading,
		CollectionTable,
	},
	data() {
		return {
			store,
			loaded: false,
			headers:[
				{ id:1, label:"Nom", field:"title" },
				{ id:2, label:"Index", field:"properties.index" },
			],
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
