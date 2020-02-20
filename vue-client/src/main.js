import Vue from 'vue'
import store from '@/store'
import App from '@/App.vue'
import router from '@/router'

Vue.config.productionTip = false

// For debugging
window.store = store

new Vue({
	router,
	render: h => h(App)
}).$mount('#app')
