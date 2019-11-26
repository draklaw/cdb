<template>
	<div id="app">
		<h1>CDB</h1>
		<div v-if="user">
			Logged as {{user.username}}
			<button v-on:click="logout">Logout</button>
		</div>

		<router-view  v-if="user" />
		<login v-else />
	</div>
</template>

<script>
import store from '@/store/store.js'

import Login from '@/components/Login.vue'

export default {
	name: "app",
	components: {
		Login,
	},
	data() {
		return {
			store,
		}
	},
	computed: {
		user() {
			return this.store.user
		}
	},
	methods: {
		logout() {
			this.store.logout()
		}
	},
}
</script>

<style lang="scss">
#app {
	font-family: 'Avenir', Helvetica, Arial, sans-serif;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
	color: #2c3e50;
}
</style>
