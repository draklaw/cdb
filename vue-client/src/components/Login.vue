<template>
	<form
		v-on:submit.prevent="submit"
		id="cdbLoginForm"
	>
		<div class="cdbLoginFormField">
			<label for="cdbLogin">Username:</label>
			<input
				id="cdbUsername"
				v-model="username"
				placeholder="Username"
			>
		</div>
		<div class="cdbLoginFormField">
			<label for="cdbPassword">Password:</label>
			<input
				id="cdbPassword"
				v-model="password"
				type="password"
				placeholder="Password"
			>
		</div>
		<push-button
			type="submit"
			look="positive"
		>
			Login
		</push-button>
	</form>
</template>

<script>
import store from "@/store/store.js"

import PushButton from '@/components/PushButton.vue'

export default {
	components: {
		PushButton,
	},
	props: {
		redirectToUserPage: Boolean,
	},
	data(){
		return{
			username:"",
			password:"",
		}
	},
	methods:{
		async submit(){
			await store.login(this.username, this.password)
			if(store.user && this.redirectToUserPage)
				this.$router.push(`/${store.user.username}`)
		}
	}
}
</script>


<style lang="scss">
@import "@/style/globals.scss";

#cdbLoginForm {
	width: 20rem;
	margin: auto;
	margin-top: 4rem;
	padding: $large-margin;

	background-color: $light-background-color;
	border: 1px solid $light-border-color;
	border-radius: $medium-margin;

	label {
		display: block;
		font-size: 80%;
	}

	.cdbLoginFormField {
		margin-bottom: $medium-margin;

		input {
			width: 100%;
			padding: $small-margin;
			box-sizing: border-box;

			border: 1px solid $light-border-color;
			border-radius: $small-margin;

			background-color: rgb(255, 255, 255);
		}
	}

	.cdbPositiveButton {
		text-align: right;
	}
}
</style>
