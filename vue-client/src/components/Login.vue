<template>
	<form v-on:submit.prevent="submit">
		<div>
			<label for="login">Username:</label>
			<input
				id="username"
				v-model="username"
				placeholder="Username"
			>
		</div>
		<div>
			<label for="password">Password:</label>
			<input
				id="password"
				v-model="password"
				type="password"
				placeholder="Password"
			>
		</div>
		<div>
			<input type="submit" value="Login">
		</div>
	</form>
</template>

<script>
import store from "@/store/store.js"

export default {
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
