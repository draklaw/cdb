<template>
	<div class="home">
		<h2>Home page</h2>

		<ul v-if="loaded">
			<li v-for="user in users" v-bind:key="user.id">
				<router-link v-bind:to="`/${user.username}`">
					{{ user.username }}
				</router-link>
			</li>
		</ul>
		<loading v-else />
	</div>
</template>

<script>
import store from '@/store/store.js'

import Loading from '@/components/Loading.vue'

export default {
	name: 'home',
	components: {
		Loading,
	},
	data() {
		return {
			store,
			loaded: false,
		}
	},
	computed: {
		users() {
			return Object.values(this.store.users)
				.sort(user => user.username)
		},
	},
	methods: {
		async update() {
			this.loaded = false
			await this.store.fetchUsers()
			this.loaded = true
		},
	},
	async created() {
		await this.update()
	},
}
</script>
