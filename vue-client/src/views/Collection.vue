<template>
	<div id="cdbCollection">
		<template v-if="loaded">
			<header>
				<h2>{{ collection.title }}</h2>
				<search-field v-model="searchQuery" />
				<push-button
					v-on:click="toggleNewItemPane"
					look="positive"
				>
					+
				</push-button>
			</header>
			<collection-table
				v-if="loaded"
				v-bind:items="filteredItems"
				v-bind:fields="collection.fields"
				class="cdbCollectionTable"
			/>
		</template>
		<loading v-else />
	</div>
</template>

<script>
import store from '@/store/store.js'

import Loading from '@/components/Loading.vue'
import CollectionTable from '@/components/CollectionTable.vue'
import { SearchField, PushButton } from '@/components/widgets'

export default {
	name: 'collection',
	components: {
		Loading,
		CollectionTable,
		SearchField,
		PushButton,
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
			this.loaded = false
			await this.store.fetchCollection(this.username, this.collectionName)
			this.loaded = true
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
@import "@/style/globals.scss";

#cdbCollection {
	flex: 1;

	width: $normal-page-width;

	background: $main-background-color;

	& > * {
		padding: 0 $medium-margin;
	}

	header {
		display: flex;
		align-items: center;

		padding: $small-margin $medium-margin;
		border-bottom: 1px solid $light-border-color;

		h2 {
			margin: $small-margin 0;
			flex-grow: 1;
		}

		.cdbSearchField {
			margin: 0 $small-margin;
		}
	}
}

.cdbCollectionTable{
	width: 100%;
}
</style>
