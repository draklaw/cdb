import Vue from 'vue'
import store from '@/store'
import App from '@/App.vue'
import router from '@/router'

import 'keen-ui/dist/keen-ui.css';

Vue.config.productionTip = false

// For debugging
window.store = store

new Vue({
	router,
	render: h => h(App)
}).$mount('#app')
