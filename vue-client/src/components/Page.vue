<template>
	<div class="cdb">
		<ui-toolbar
			type="colored"
			text-color="white"
			remove-nav-icon
			class="cdb-toolbar"
		>
			<h1>{{ title }}</h1>

			<div
				v-if="user"
				slot="actions"
			>
				<slot name="toolbar"></slot>
				<ui-icon-button
					color="white"
					icon="person"
					size="large"
					type="secondary"
					ref="userMenu"
					has-dropdown
				>
					<ui-menu
						slot="dropdown"
						:options="userOptions"
						@select="userMenuClicked"
						@close="$refs.userMenu.closeDropdown()"
					>
					</ui-menu>
				</ui-icon-button>
			</div>
		</ui-toolbar>

		<main class="cdb-content">
			<login v-if="!user"/>
			<ui-progress-circular
				v-else-if="loading"
				:size="64"
				:stroke="4"
				class="cdb-page-progress"
			/>
			<slot v-else></slot>
		</main>
	</div>
</template>


<script>
import { UiIconButton, UiMenu, UiProgressCircular, UiToolbar } from 'keen-ui';

import store from '@/store/store.js'

import Login from '@/components/Login.vue'

export default {
	components: {
		UiIconButton,
		UiMenu,
		UiProgressCircular,
		UiToolbar,
		Login,
	},
	props: {
		title: {
			default: "CDB",
			type: String,
		},
	},
	data() {
		return {
			store,
			userOptions: [
				{
					label: "Logout",
					action(component) {
						component.logout()
					},
				},
			],
		}
	},
	computed: {
		user() {
			return this.store.user
		},
		loading() {
			return this.store.loading
		},
	},
	methods: {
		userMenuClicked(event) {
			const action = event.action
			if (action)
				action(this)
		},
		logout() {
			this.store.logout()
		},
	},
}
</script>


<style lang="scss">
@import "@/style/globals.scss";

.cdb {
	display: flex;
	align-items: center;
	flex-direction: column;

	min-height: 100vh;

	.cdb-toolbar {
		width: 100%;
		z-index: 1;
	}

	.cdb-content {
		@include cdb-shadow;

		position: relative;
		flex: 1;
		width: $normal-page-width;

		padding: $small-margin $medium-margin;

		background-color: $surface-color;

		.cdb-page-progress {
			position: absolute;
			top: calc(50% - 32px);
			left: calc(50% - 32px);
		}
	}
}

</style>
