<template>
	<router-view/>
</template>

<script>
import store from '@/store/store.js'

export default {
	name: "app",
	components: {
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
		},
		newCollection() {
			this.$router.push("/new-collection")
		},
	},
}
</script>

<style lang="scss">
</style>
