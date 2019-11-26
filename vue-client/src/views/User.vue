<template>
	<div class="user">
		<template v-if="loaded && user">
			<h2>{{ user.username }}'s collections</h2>

			<ul>
				<li v-for="col in collections" v-bind:key="col.id">
					<router-link v-bind:to="`/${user.username}/${col.name}`">
						{{ col.name }}
					</router-link>
				</li>
			</ul>
		</template>
		<p v-else-if="loaded">Unknown user</p>
		<loading v-else />
	</div>
</template>

<script>
import store from '@/store/store.js'

import Loading from '@/components/Loading.vue'

export default {
	name: 'user',
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
			this.loaded = false
			await this.store.fetchCollections(this.username)
			this.loaded = true
		},
	},
	async created() {
		await this.update()
	},
}
</script>
