<template>
	<div class="cdb">
		<h1>{{ title }}</h1>

		<div v-if="user">
			Logged as {{ user.username }}.
			<button v-on:click="logout">
				Logout
			</button>
		</div>

		<main class="cdb-content">
			<div v-if="user && loading">
				Loading...
			</div>
			<slot v-else></slot>
		</main>
	</div>
</template>


<script>
import store from '@/store/store.js'

export default {
	components: {
	},
	props: {
		title: {
			default: "CDB",
			type: String,
		},
	},
	data() {
		return {
			store,
			userOptions: [
				{
					label: "Logout",
					action(component) {
						component.logout()
					},
				},
			],
		}
	},
	computed: {
		user() {
			return this.store.user
		},
		loading() {
			return this.store.loading
		},
	},
	methods: {
		userMenuClicked(event) {
			const action = event.action
			if (action)
				action(this)
		},
		logout() {
			this.store.logout()
		},
	},
}
</script>


<style lang="scss">
</style>
