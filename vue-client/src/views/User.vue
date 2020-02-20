<template>
	<page>
		<h2>{{ user.username }}'s collections</h2>

		<ul>
			<li v-for="col in collections" v-bind:key="col.id">
				<router-link v-bind:to="`/${user.username}/${col.name}`">
					{{ col.name }}
				</router-link>
			</li>
		</ul>
	</page>
</template>

<script>
import store from '@/store'

import Page from '@/components/Page.vue'

export default {
	name: 'user',
	components: {
		Page,
	},
	data() {
		return {
			store,
		}
	},
	computed: {
		username() {
			return this.$route.params.username
		},
		user() {
			return this.store.getUser(this.username)
		},
		collections() {
			return this.user.collections
				.map(id => this.store.collections[id])
				.sort(col => col.name)
		},
	},
	methods: {
		async update() {
			await this.store.fetchCollections(this.username)
		},
	},
	async created() {
		this.update()
	},
}
</script>


<style lang="scss">
</style>
