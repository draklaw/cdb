import Vue from 'vue'

import api from "@/api/api.js"

export class Store {
	constructor() {
		// For debugging
		window.store = this

		this.user = null
		this.users = {}
		this.usersByUsername = {}
		this.collections = {}

		this.tryGetSavedUser()
	}


	getUser(username) {
		const userId = this.usersByUsername[username]
		if(!userId)
			return null
		return this.users[userId]
	}

	getCollection(username, collectionName) {
		const user = this.getUser(username)
		if (!user)
			return null

		const colId = user.collectionsByName[collectionName]
		if (!colId)
			return null

		return this.collections[colId]
	}


	async login(username, password) {
		const tokenJson = await api.getToken(username, password)

		const token = tokenJson.access_token

		api.token = token

		this.user = await this.fetchUser(username)

		localStorage.setItem("user", JSON.stringify(this.user))
		localStorage.setItem("token", token)
	}

	logout() {
		localStorage.removeItem("user")
		localStorage.removeItem("token")

		this.user = null
		api.token = null
	}

	async fetchUser(username) {
		console.log(`fetchUser(${username})`)

		const user = await api.getUser(username)

		Vue.set(this.users, user.id, user)
		Vue.set(this.usersByUsername, user.username, user.id)

		return user
	}

	async fetchUsers() {
		console.log(`fetchUsers()`)

		const users = await api.getUsers()
		const usersById = {}
		const usersByUsername = {}

		for(const user of users) {
			usersById[user.id] = user
			usersByUsername[user.username] = user.id
		}

		Vue.set(this, "users", usersById)
		Vue.set(this, "usersByUsername", usersByUsername)
	}

	async fetchCollections(username) {
		console.log(`fetchCollections(${username})`)

		const user = await this.fetchUser(username)

		const collections = await api.getCollections(username)

		const collectionsIds = []
		const collectionsByName = {}

		for(const collection of collections) {
			Vue.set(this.collections, collection.id, collection)

			collectionsIds.push(collection.id)
			collectionsByName[collection.name] = collection.id
		}

		Vue.set(user, "collections", collectionsIds)
		Vue.set(user, "collectionsByName", collectionsByName)
	}

	async fetchCollection(username, collectionName) {
		console.log(`fetchCollection(${username}, ${collectionName})`)

		await this.fetchCollections(username)
		const collection = this.getCollection(username, collectionName)

		const [items, fields] = await Promise.all([
			api.getItems(username, collectionName),
			api.getFields(username, collectionName),
		])

		Vue.set(collection, "items", items)
		Vue.set(collection, "fields", fields)
	}

	async createCollection(collection) {
		console.log(`fetchCollection(${JSON.stringify(collection)})`)

		await api.createCollection(this.user.username, collection)
	}

	async tryGetSavedUser() {
		const user = JSON.parse(localStorage.getItem("user"))
		const token = localStorage.getItem("token")

		if(!user || !token) {
			this.logout()
			return
		}

		api.token = token
		this.user = user

		try {
			this.user = await this.fetchUser(this.user.username)
		}
		catch(error) {
			this.token = null
			this.user = null
		}
	}
}


export default new Store()
