<template>
	<page>
		<h2>Create a new collection</h2>
		<form v-on:submit.prevent="createCollection">
			<message-box v-bind:messages="messages" />
			<input
				id="cdbTitle"
				type="text"
				v-model="title"
				v-on:input="updateName"
				placeholder="Title"
				autofocus
				required
			/>
			<input
				id="cdbName"
				type="text"
				v-model="name"
				placeholder="Name"
				pattern="\w*"
				required
			/>
			<input
				id="cdbPublic"
				type="checkbox"
				v-model="isPublic"
				v-bind:busy="submitting"
				required
			/>
			<label for="cdbPublic">
				Public collection
			</label>
			<div>
				Headers:
			</div>
			<header-form
				v-for="[i, header] in headers.entries()"
				v-bind:key="i"
				v-bind:value="header"
				v-on:delete="deleteHeader(i)"
				delete-button
			/>
			<header-form
				v-bind:value="newHeader"
				v-on:add="addHeader"
			/>
			<button
				type="submit"
			>
				Create
			</button>
		</form>
	</page>
</template>

<script>
import { toIdentifier } from "@/utils"

import store from '@/store/store.js'

import Page from "@/components/Page.vue"
import MessageBox from "@/components/MessageBox.vue"
import HeaderForm from "@/components/HeaderForm.vue"

export default {
	name: "new-collection",
	components: {
		Page,
		MessageBox,
		HeaderForm,
	},
	data() {
		return {
			store,
			title: "",
			name: "",
			isPublic: false,
			submitting: false,
			messages: [],
			newHeader: {
				label: "",
				name: "",
				type: "text",
				columnIndex: -1,
			},
			headers: [],
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
				headers: this.headers,
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
		addHeader() {
			const header = Object.assign({}, this.newHeader)
			this.headers.push(header)
			this.newHeader = {
				label: "",
				name: "",
				type: "text",
				columnIndex: -1,
			}
		},
		deleteHeader(index) {
			this.headers.splice(index, 1)
		},
	},
}
</script>


<style lang="scss">
</style>
