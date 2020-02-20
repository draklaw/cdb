import Vue from 'vue'

import api from "@/api/api.js"


function logCall(target, key, descriptor) {
	const func = descriptor.value
	if(typeof func === 'function') {
		descriptor.value = async function wrapper(...args) {
			const call = `${key}(${args.join(', ')})`
			console.log(`Call ${call}...`)
			try {
				const result = await func.apply(this, args)
				console.log(`Result ${call}:`, result)
				return result
			}
			catch(err) {
				console.error(`Error ${call}`, err)
				throw err
			}
		}
	}
	return descriptor
}


function loader(target, key, descriptor) {
	const func = descriptor.value
	if(typeof func === 'function') {
		descriptor.value = async function wrapper(...args) {
			this.loading += 1
			try {
				return await func.apply(this, args)
			}
			finally {
				this.loading -= 1
			}
		}
	}
	return descriptor
}


export class Store {
	constructor() {
		this.user = null
		this.users = {}
		this.usersByUsername = {}
		this.collections = {}

		this.loading = 0

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

		return this.collections[colId] || null
	}


	@logCall
	@loader
	async login(username, password) {
		const tokenJson = await api.getToken(username, password)

		const token = tokenJson.access_token

		api.token = token

		Vue.set(this, "user", await this.fetchUser(username))

		localStorage.setItem("user", JSON.stringify(this.user))
		localStorage.setItem("token", token)
	}

	logout() {
		localStorage.removeItem("user")
		localStorage.removeItem("token")

		Vue.set(this, "user", null)
		api.token = null
	}

	@logCall
	@loader
	async fetchUser(username) {
		const user = await api.getUser(username)
		user.collections = []
		user.collectionsByName = {}
		user.linkedCollections = []

		Vue.set(this.users, user.id, user)
		Vue.set(this.usersByUsername, user.username, user.id)

		if (this.user && user.id == this.user.id)
			Vue.set(this, "user", user)

		return user
	}

	@logCall
	@loader
	async fetchUsers() {
		const users = await api.getUsers()
		const usersById = {}
		const usersByUsername = {}

		for(const user of users) {
			user.collections = []
			user.collectionsByName = {}
			user.linkedCollections = []

			usersById[user.id] = user
			usersByUsername[user.username] = user.id

			if (this.user && user.id == this.user.id)
				Vue.set(this, "user", user)
		}

		Vue.set(this, "users", usersById)
		Vue.set(this, "usersByUsername", usersByUsername)
	}

	@logCall
	@loader
	async fetchCollections(username) {
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

	@logCall
	@loader
	async fetchLinkedCollections(username) {
		await this.fetchUsers()
		const user = this.getUser(username)

		const collections = await api.getCollections(username, {
			onlyOwned: false,
		})

		const collectionsIds = []
		const collectionsByName = {}
		const linkedCollections = []

		for(const collection of collections) {
			Vue.set(this.collections, collection.id, collection)

			if (collection.owner == user.id)
				collectionsIds.push(collection.id)
			collectionsByName[collection.name] = collection.id
			linkedCollections.push(collection.id)
		}

		Vue.set(user, "collections", collectionsIds)
		Vue.set(user, "collectionsByName", collectionsByName)
		Vue.set(user, "linkedCollections", linkedCollections)
	}

	@logCall
	@loader
	async fetchCollection(username, collectionName) {
		await this.fetchCollections(username)
		const collection = this.getCollection(username, collectionName)

		const [items, fields] = await Promise.all([
			api.getItems(username, collectionName),
			api.getFields(username, collectionName),
		])

		Vue.set(collection, "items", items)
		Vue.set(collection, "fields", fields)
	}

	@logCall
	@loader
	async createCollection(collection) {
		await api.createCollection(this.user.username, collection)
	}

	@logCall
	@loader
	async tryGetSavedUser() {
		const user = JSON.parse(localStorage.getItem("user"))
		const token = localStorage.getItem("token")

		if(!user || !token) {
			this.logout()
			return
		}

		api.token = token

		try {
			Vue.set(this, "user", await this.fetchUser(user.username))
		}
		catch(error) {
			api.token = null
			Vue.set(this, "user", null)
		}
	}
}


const store = new Store()
export default store
