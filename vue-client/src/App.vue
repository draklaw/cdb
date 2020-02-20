<template>
	<div>
		<router-view v-if="user"/>
		<page v-else>
			<div v-if="loading">
				Loading...
			</div>
			<login v-else/>
		</page>
	</div>
</template>

<script>
import store from '@/store'

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
		},
		loading() {
			return this.store.loading
		}
	},
	methods: {
	},
}
</script>

<style lang="scss">
</style>
