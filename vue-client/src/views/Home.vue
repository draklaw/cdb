<template>
	<div class="home">
		<h1>CDB</h1>
		<login></login>
		<collection></collection>
	</div>
</template>

<script>
// @ is an alias to /src
import Login from '@/components/login.vue'
import Collection from '@/views/collection.vue'

export default {
	name: 'home',
	components: {
		Login,
		Collection
	}
}
</script>
