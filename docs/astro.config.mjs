// @ts-check
import starlight from "@astrojs/starlight";
import { defineConfig } from "astro/config";


// https://astro.build/config
export default defineConfig({
	site: "https://tsumikii.pages.dev",
	server: {
		port: 3000
	},
	integrations: [
		starlight({
			title: "Tsumiki",
			customCss: [
				// Path to our custom CSS file
				"./src/styles/custom.css",
			],

			defaultLocale: "en",
			locales: {
				en: { label: "English", lang: "en" },
				es: { label: "Español", lang: "es" },
				ar: { label: "العربية", lang: "ar", dir: "rtl" },
				de: { label: "Deutsch", lang: "de" },
				fr: { label: "Français", lang: "fr" },
				nl: { label: "Nederlands", lang: "nl" },
			"pt-br": { label: "Português (Brasil)", lang: "pt-BR" },
			tr: { label: "Türkçe", lang: "tr" },
			"zh-cn": { label: "简体中文", lang: "zh-CN" },
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
					collapsed: false,
					items: [{ autogenerate: { directory: "getting-started" } }],
				},
				{
					label: "🛠️ Configuring",
					collapsed: true,
					items: [{ autogenerate: { directory: "configuring" } }],
				},
				{
					label: "🧩 Features",
					collapsed: true,
					items: [{ autogenerate: { directory: "features" } }],
				},
				{
					label: "🎨 Theming",
					collapsed: true,
					items: [{ autogenerate: { directory: "theming" } }],
				},
				{
					label: "📚 Resources",
					collapsed: true,
					items: [{ autogenerate: { directory: "resources" } }],
				},
				{
					label: "👥 Help",
					collapsed: true,
					items: [{ autogenerate: { directory: "help" } }],
				},
			],
		}),
	],
});
