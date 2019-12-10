<template>
	<div id="app">
		<header id="cdbHeader">
			<h1><router-link to="/">CDB</router-link></h1>
			<div v-if="user">
				<push-button
					v-on:click="newCollection"
				>
					+
				</push-button>
			</div>
			<div v-if="user">
				Logged as {{user.username}}
				<push-button
					v-on:click="logout"
				>
					Logout
				</push-button>
			</div>
			<div v-else>
				Not logged in
			</div>
		</header>

		<router-view  v-if="user" />
		<login v-else />
	</div>
</template>

<script>
import store from '@/store/store.js'

import PushButton from '@/components/PushButton.vue'
import Login from '@/components/Login.vue'

export default {
	name: "app",
	components: {
		PushButton,
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
		},
		newCollection() {
			this.$router.push("/new-collection")
		},
	},
}
</script>

<style lang="scss">
@import "@/style/globals.scss";

body {
	margin: 0px;
}

#app {
	display: flex;
	flex-direction: column;
	align-items: center;

	min-height: 100vh;

	background-color: $background-background-color;

	font-family: 'Avenir', Helvetica, Arial, sans-serif;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
	color: #2c3e50;
}

#cdbHeader {
	display: flex;
	align-items: center;

	width: 100%;

	background-color: $light-background-color;
	border-bottom: 1px solid $light-border-color;

	h1 {
		flex-grow: 1;
		font-size: 1.5em;
		margin: $small-margin;
	}

	div {
		margin: $small-margin;

		.cdbNeutralButton {
			font-size: 80%;
			margin-left: 0.5rem;
			padding: .25rem .5rem;
		}
	}
}
</style>
