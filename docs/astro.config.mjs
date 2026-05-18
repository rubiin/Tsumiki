// @ts-check
import starlight from "@astrojs/starlight";
import { defineConfig } from "astro/config";

const repository = process.env.GITHUB_REPOSITORY?.split("/")[1];
const owner = process.env.GITHUB_REPOSITORY_OWNER;
const isActions = process.env.GITHUB_ACTIONS === "true";
const isUserSite =
	repository &&
	owner &&
	repository.toLowerCase() === `${owner.toLowerCase()}.github.io`;

// https://astro.build/config
export default defineConfig({
	...(isActions && owner
		? {
				site: `https://${owner}.github.io`,
				base: repository && !isUserSite ? `/${repository}` : "/",
			}
		: {}),
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
					href: "https://github.com/rubiin/Tsumiki",
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
					autogenerate: { directory: "getting-started" },
				},
				{
					label: "🛠️ Configuring",
					autogenerate: { directory: "configuring" },
				},

				{
					label: "🎨 Theming",
					autogenerate: { directory: "theming" },
				},
				{
					label: "📚 Resources",
					autogenerate: { directory: "resources" },
				},
				{
					label: "👥 Help",
					autogenerate: { directory: "help" },
				},
			],
		}),
	],
});
