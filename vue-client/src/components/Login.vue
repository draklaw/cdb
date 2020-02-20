<template>
	<form
		v-on:submit.prevent="submit"
		id="cdbLoginForm"
	>
		<message-box v-bind:messages="messages" />
		<input
			id="cdbUsername"
			type="text"
			v-model="username"
			placeholder="Username"
			autofocus
			required
		/>
		<input
			id="cdbPassword"
			type="password"
			v-model="password"
			placeholder="Password"
			required
		/>
		<button>
			Login
		</button>
	</form>
</template>

<script>
import store from "@/store"

import MessageBox from '@/components/MessageBox.vue'

export default {
	components: {
		MessageBox,
	},
	props: {
		redirectToUserPage: Boolean,
	},
	data(){
		return{
			username: "",
			password: "",
			busy: false,
			messages: [],
		}
	},
	methods:{
		async submit(){
			try {
				this.busy = true
				await store.login(this.username, this.password)
			}
			catch(error) {
				this.messages = [{
					message: error.message,
					type: "negative",
				}]
				this.busy = false
				return
			}

			if(store.user && this.redirectToUserPage)
				this.$router.push(`/${store.user.username}`)
		}
	}
}
</script>


<style lang="scss">
</style>
