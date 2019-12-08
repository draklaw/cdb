<template>
	<div id="cdbNewCollection">
		<h2>Create a new collection</h2>
		<form v-on:submit.prevent="createCollection">
			<message-box v-bind:messages="messages" />
			<line-edit
				v-model="title"
				v-on:input="updateName"
				id="cdbTitle"
				label="Title"
				autofocus
				required
			/>
			<line-edit v-model="name" id="cdbName" label="Name" />
			<checkbox
				v-model="isPublic"
				v-bind:busy="submitting"
				id="cdbPublic"
				label="Public collection"
				required
			/>
			<push-button type="submit" look="positive">
				Create
			</push-button>
		</form>
	</div>
</template>

<script>
import { toIdentifier } from "@/utils"

import store from '@/store/store.js'

import LineEdit from "@/components/LineEdit.vue"
import Checkbox from "@/components/Checkbox.vue"
import PushButton from "@/components/PushButton.vue"
import MessageBox from "@/components/MessageBox.vue"

export default {
	components: {
		LineEdit,
		Checkbox,
		PushButton,
		MessageBox,
	},
	data() {
		return {
			store,
			title: "",
			name: "",
			isPublic: false,
			submitting: false,
			messages: [],
		}
	},
	methods: {
		updateName() {
			this.name = toIdentifier(this.title)
		},
		async createCollection() {
			const collection = {
				title: this.title,
				name: this.name,
				public: this.isPublic,
			}

			this.submitting = true
			try {
				await this.store.createCollection(collection)
				this.$router.push(`/${this.store.user.username}/${this.name}`)
			}
			catch(error) {
				this.messages = [{
					message: error.message,
					type: "negative",
				}]
				this.submitting = false
			}
		},
	},
}
</script>


<style lang="scss">
@import "@/style/globals.scss";

#cdbNewCollection {
	width: 40rem;
	margin: auto;
}
</style>
