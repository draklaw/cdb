import Vue from 'vue'
import VueRouter from 'vue-router'

import Home from '@/views/Home.vue'
import About from '@/views/About.vue'
import NotFound from '@/views/NotFound.vue'
import User from '@/views/User.vue'
import Collection from '@/views/Collection.vue'
import NewCollection from '@/views/NewCollection.vue'

Vue.use(VueRouter)

const routes = [
	{
		path: '/',
		name: 'home',
		component: Home
	},
	{
		path: '/about',
		name: 'about',
		component: About
	},
	{
		path: '/new-collection',
		name: 'new-collection',
		component: NewCollection
	},
	{
		path: '/:username',
		name: 'user',
		component: User
	},
	{
		path: '/:username/:collection',
		name: 'collection',
		component: Collection
	},
	{
		path: '*',
		name: 'not-found',
		component: NotFound
	},
]

const router = new VueRouter({
	mode: 'history',
	base: process.env.BASE_URL,
	routes
})

export default router
