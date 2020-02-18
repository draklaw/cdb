<template>
	<page>
		<h2>My collections</h2>
		<ul>
			<li
				v-for="[user, collection] in linkedUserCollections"
				v-bind:key="collection.id"
			>
				<router-link v-bind:to="`/${user.username}/${collection.name}`">
					{{ user.username }} / {{ collection.name }}
				</router-link>
			</li>
		</ul>
	</page>
</template>

<script>
import store from '@/store/store.js'

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
			const tmp = this.store.user.linkedCollections
				.map(id => {
					const collection = this.store.collections[id]
					const user = this.store.users[collection.owner]
					return [user, collection]
				})
				.sort(([user, collection]) => `${user.username}:${collection.name}`)
			console.log(tmp)
			return tmp
		},
	},
	methods: {
		async update() {
			this.store.loading = true
			await this.store.fetchLinkedCollections(
				this.store.user.username,
			)
			this.store.loading = false
		},
	},
	mounted() {
		this.update()
	},
}
</script>


<style lang="scss">
#cdbHome {
}
</style>
