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
			/>
			<label for="cdbPublic">
				Public collection
			</label>
			<div>
				Fields:
				<button v-on:click.prevent="addField">
					Add Field
				</button>
			</div>
			<field-form
				v-for="field in fields"
				v-bind:key="field.key"
				v-bind:value="field"
				v-on:delete="deleteField(field.key)"
				delete-button
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

import store from '@/store'

import Page from "@/components/Page.vue"
import MessageBox from "@/components/MessageBox.vue"
import FieldForm from "@/components/FieldForm.vue"

export default {
	name: "new-collection",
	components: {
		Page,
		MessageBox,
		FieldForm,
	},
	data() {
		return {
			store,
			title: "",
			name: "",
			isPublic: false,
			submitting: false,
			messages: [],
			fieldCounter: 0,
			fields: [],
		}
	},
	methods: {
		updateName() {
			this.name = toIdentifier(this.title)
		},
		async createCollection() {
			const fields = []
			for(const field of this.fields) {
				fields.push({
					name: field.name,
					type: field.type,
				})
			}

			const collection = {
				title: this.title,
				name: this.name,
				public: this.isPublic,
				std_fields: fields,
			}

			this.submitting = true
			try {
				await this.store.createCollection(collection)
				this.$router.push(`/${this.store.user.username}/${this.name}`)
			}
			catch(error) {
				console.log(error)
				this.messages = [{
					message: error.message,
					type: "negative",
				}]
				this.submitting = false
			}
		},
		addField() {
			this.fields.push({
				key: this.fieldCounter,
				name: "",
				type: "text",
			})
			this.fieldCounter += 1
		},
		deleteField(key) {
			const index = this.fields.findIndex(f => f.key == key)
			if (index >= 0)
				this.fields.splice(index, 1)
		},
	},
}
</script>


<style lang="scss">
</style>
