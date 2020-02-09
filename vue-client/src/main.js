import Vue from 'vue'
import App from './App.vue'
import router from './router'

import 'keen-ui/dist/keen-ui.css';

Vue.config.productionTip = false

new Vue({
	router,
	render: h => h(App)
}).$mount('#app')
