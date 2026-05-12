// @ts-check
import starlight from "@astrojs/starlight";
import { defineConfig } from "astro/config";


// https://astro.build/config
export default defineConfig({
	site: "https://tsumikii.pages.dev",
	integrations: [
		starlight({
			title: "Tsumiki",
			customCss: [
				// Path to our custom CSS file
				"./src/styles/custom.css",
			],
			components: {
				LanguageSelect: "./src/components/LanguageSelect.astro",
			},
			defaultLocale: "en",
			locales: {
				en: { label: "English", lang: "en" },
				es: { label: "Español", lang: "es" },
			},
			social: [
				{
					icon: "github",
					label: "GitHub",
					href: "https://github.com/rubiin/tsumiki",
				},
				{
					icon: "discord",
					label: "Discord",
					href: "https://discord.gg/8nWbDC4SnP",
				},
			],
			sidebar: [
				{
					label: "🚀 Getting Started",
					items: [{ autogenerate: { directory: "getting-started" } }],
				},
				{
					label: "🛠️ Configuring",
					items: [{ autogenerate: { directory: "configuring" } }],
				},
				{
					label: "🎨 Theming",
					items: [{ autogenerate: { directory: "theming" } }],
				},
				{
					label: "📚 Resources",
					items: [{ autogenerate: { directory: "resources" } }],
				},
				{
					label: "👥 Help",
					items: [{ autogenerate: { directory: "help" } }],
				},
			],
		}),
	],
});
