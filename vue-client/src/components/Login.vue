<template>
	<form
		v-on:submit.prevent="submit"
		id="cdbLoginForm"
	>
		<message-box v-bind:messages="messages" />
		<line-edit
			id="cdbUsername"
			v-model="username"
			label="Username"
			autofocus
			required
		/>
		<line-edit
			id="cdbPassword"
			v-model="password"
			label="Password"
			password
			required
		/>
		<push-button
			v-bind:busy="busy"
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
import LineEdit from '@/components/LineEdit.vue'
import MessageBox from '@/components/MessageBox.vue'

export default {
	components: {
		PushButton,
		LineEdit,
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
