module.exports = {
	css: {
		loaderOptions: {
			sass: {
				prependData: `@import "@/style/colors.scss";`
			},
		},
	},
}
