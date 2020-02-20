<template>
	<page>
		<h2>My collections</h2>
		<button v-on:click="update">
			Refresh
		</button>
		<button v-on:click="openNewCollectionPane">
			New collection
		</button>
		<ul>
			<li
				v-for="[user, collection] in linkedUserCollections"
				v-bind:key="collection.id"
			>
				<router-link v-bind:to="`/${user.username}/${collection.name}`">
					<span class="cdbCollectionPath">
						{{ user.username }} / {{ collection.name }}
					</span>
					<span class="cdbCollectionTitle">
						{{ collection.title }}
					</span>
				</router-link>
			</li>
		</ul>
	</page>
</template>

<script>
import store from '@/store'

import Page from '@/components/Page.vue'

export default {
	name: 'home',
	components: {
		Page,
	},
	data() {
		return {
			store,
		}
	},
	computed: {
		linkedUserCollections() {
			return this.store.user.linkedCollections
				.map(id => {
					const collection = this.store.collections[id]
					const user = this.store.users[collection.owner]
					return [user, collection]
				})
				.sort(([user, collection]) => `${user.username}:${collection.name}`)
		},
	},
	methods: {
		async update() {
			await this.store.fetchLinkedCollections(
				this.store.user.username,
			)
		},
		openNewCollectionPane() {
			this.$router.push('/new-collection')
		}
	},
	created() {
		this.update()
	},
}
</script>


<style lang="scss">
</style>
