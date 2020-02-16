<template>
	<page>
		<h2>Home</h2>
		<ul>
			<li v-for="user in users" v-bind:key="user.id">
				<router-link v-bind:to="`/${user.username}`">
					{{ user.username }}
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
			fields: [
				{
					id: 0,
					width: -1,
					label: "User",
					field: "user.username",
				},
			],
		}
	},
	computed: {
		users() {
			return Object.values(this.store.users)
				.sort(user => user.username)
		},
		items() {
			const items = []
			for(const user of Object.values(this.store.users)) {
				items.push({
					user,
				})
			}
			return items
		},
	},
	methods: {
		async update() {
			this.store.loading = true
			await this.store.fetchUsers()
			this.store.loading = false
		},
	},
	async mounted() {
		await this.update()
	},
}
</script>


<style lang="scss">
#cdbHome {
}
</style>
