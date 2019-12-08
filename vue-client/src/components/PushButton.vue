<template>
	<button
		v-bind:class="classes"
		v-on:click="!busy? $emit('click'): null"
		v-bind:type="type"
	>
		<slot></slot>
	</button>
</template>


<script>
import { capitalize } from "@/utils"

export default {
	props: {
		type: {
			default: "button",
			type: String,
		},
		look: {
			default: "neutral",
			type: String,
		},
		busy: {
			default: false,
			type: Boolean,
		},
	},
	computed: {
		classes() {
			const lookClass = `cdbButton${capitalize(this.look)}`
			return {
				cdbButton: true,
				[lookClass]: true,
				cdbButtonBusy: this.busy,
			}
		}
	},
}
</script>


<style lang="scss">
@import "@/style/globals.scss";

.cdbButton {
	padding: $small-margin $medium-margin;

	border: none;
	border-radius: $small-margin;

	&:hover {
		filter: brightness(1.1);
	}
}

.cdbButtonPositive {
	background-color: $positive-color;
}

.cdbButtonNegative {
	background-color: $negative-color;
}

.cdbButtonNeutral {
	background-color: $neutral-color;
}

$button-gradient-width: 1em;

.cdbButton.cdbButtonBusy {
	background:
		$positive-color
		repeating-linear-gradient(
			to right,
			$positive-color,
			adjust-color($positive-color, $lightness: 10%) $button-gradient-width,
			$positive-color 2 * $button-gradient-width,
		)
		repeat
		scroll
		0% 0%;
	animation: 0.5s linear 0s infinite normal none running cdbButtonBusyAnimation;
}

@keyframes cdbButtonBusyAnimation {
	from {
		background-position: -2 * $button-gradient-width 0%;
	}

	to {
		background-position: 0 0%;
	}
}

</style>
