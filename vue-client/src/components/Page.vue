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
import store from '@/store'

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
		logout() {
			this.store.logout()
		},
	},
}
</script>


<style lang="scss">
</style>
