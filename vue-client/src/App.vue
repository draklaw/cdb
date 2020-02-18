<template>
	<div>
		<router-view v-if="user"/>
		<page v-else>
			<login/>
		</page>
	</div>
</template>

<script>
import store from '@/store/store.js'

import Login from '@/components/Login.vue'
import Page from '@/components/Page.vue'

export default {
	name: "app",
	components: {
		Login,
		Page,
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
