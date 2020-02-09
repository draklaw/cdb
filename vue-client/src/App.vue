<template>
	<router-view/>
</template>

<script>
import store from '@/store/store.js'

import '@/style/main.scss'

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
	color: $text-color;
}

#cdbHeader {
	display: flex;
	align-items: center;

	width: 100%;

	background-color: $main-background-color;
	border-bottom: 1px solid $light-border-color;

	z-index: 1;
	box-shadow: 0ex .15ex .3ex rgba(0, 0, 0, .25);

	h1 {
		flex-grow: 1;
		font-size: 1.5em;
		margin: $small-margin;

		a {
			text-decoration: none;
			color: $text-color;
		}
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
