<p align="center">
  <img src="assets/images/tsumiki.png" width="420" height="360" alt="Tsumiki" />
</p>
<h1 align="center">Tsumiki</h1>
<p align="center">
  <em>A modular status bar for Hyprland, built on Fabric.</em>
</p>

<p align="center">
  <a href="https://github.com/rubiin/tsumiki/blob/master/LICENSE"><img alt="License" src="https://img.shields.io/github/license/rubiin/tsumiki" /></a>
  <a href="http://makeapullrequest.com"><img alt="PRs Welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" /></a>
  <img alt="Commit activity" src="https://img.shields.io/github/commit-activity/m/rubiin/tsumiki" />
  <img alt="Closed issues" src="https://img.shields.io/github/issues-closed/rubiin/tsumiki" />
  <a href="https://discord.gg/8nWbDC4SnP"><img alt="Discord" src="https://img.shields.io/discord/1200448076620501063" /></a>
  <a href="https://tsumikii.pages.dev"><img alt="Docs" src="https://img.shields.io/badge/docs-tsumikii.pages.dev-blue" /></a>
</p>

<p align="center">
  <b><a href="#quick-start">Quick Start</a></b>
  ·
  <b><a href="https://tsumikii.pages.dev">Documentation</a></b>
  ·
  <b><a href="#contributing">Contributing</a></b>
  ·
  <b><a href="#license">License</a></b>
</p>

> _No, this isn't Waybar. Yes, it's written in Python. Yes, it's still fast._ 🐍

**Tsumiki** (積み木 — Japanese for "building blocks") is a modular status bar for the [Hyprland](https://hyprland.org) Wayland compositor. Built on [Fabric](https://github.com/Fabric-Development/fabric), it offers a flexible, widget-based architecture for creating custom desktop panels — lightweight, performant, and deeply configurable.

---

## Screenshots

<table align="center">
  <tr>
    <td colspan="4"><img src="assets/screenshots/main.png" alt="Main panel" /></td>
  </tr>
  <tr>
    <td colspan="4"><img src="assets/screenshots/notification_menu.png" alt="Notification menu" /></td>
  </tr>
  <tr>
    <td><img src="assets/screenshots/quick_settings.png" alt="Quick settings" /></td>
    <td><img src="assets/screenshots/notifications.png" alt="Notifications" /></td>
    <td align="center"><img src="assets/screenshots/logout.png" alt="Logout" /></td>
    <td align="center"><img src="assets/screenshots/weather.png" alt="Weather" /></td>
  </tr>
</table>

## Features

- **Hyprland-native** — Full integration with Hyprland's ecosystem and event model.
- **Modular widget system** — 45+ widgets: workspaces, system tray, media, battery, CPU, weather, dock, launcher, and more.
- **Fully themeable** — Customize every element with SCSS; generate dynamic [Material You](https://github.com/InioX/matugen) color schemes from your wallpaper.
- **Highly configurable** — TOML-based configuration with hot-reload. Control layout, behavior, and appearance of every widget.
- **Notification system** — Built-in notification daemon with Do Not Disturb, grouping, and history persistence.
- **On-screen displays** — OSD overlays for volume, brightness, microphone, and lock keys.
- **Lightweight & fast** — Designed for minimal memory and CPU overhead.

## Documentation

Full documentation is available at **[tsumikii.pages.dev](https://tsumikii.pages.dev)**:

| Section                                                                   | Description                             |
| ------------------------------------------------------------------------- | --------------------------------------- |
| [Getting Started](https://tsumikii.pages.dev/en/getting-started/overview) | Overview, installation, first steps     |
| [Configuration](https://tsumikii.pages.dev/en/configuring/config)         | Layout, widget options, modules         |
| [Widgets Reference](https://tsumikii.pages.dev/en/features/widgets)       | Complete widget configuration reference |
| [Modules Reference](https://tsumikii.pages.dev/en/features/modules)       | Bar, dock, notifications, launcher, OSD |
| [Theming](https://tsumikii.pages.dev/en/theming/making-themes)            | SCSS customization, Matugen, tips       |
| [FAQ & Troubleshooting](https://tsumikii.pages.dev/en/help/faq)           | Common issues and solutions             |
| [Post-Installation](https://tsumikii.pages.dev/en/resources/post-install) | Hyprland layer rules for effects        |

## Support the Project

<p align="center">
  <a href="https://ko-fi.com/rubiin" target="_blank">
    <img src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExc3N4NzlvZWs2Z2tsaGx4aHgwa3UzMWVpcmNwZTNraTM2NW84ZDlqbiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/PaF9a1MpqDzovyqVKj/giphy.gif" height="64" alt="Support on Ko-fi" />
  </a>
</p>

## Contributing

We welcome contributions of all sizes. Please see the [contributing guidelines](CONTRIBUTING.md) before opening a pull request.

## Acknowledgements

- **[Waybar](https://github.com/Alexays/Waybar)** — Initial inspiration.
- **[Hyprpanel](https://github.com/Jas-SinghFSU/HyprPanel)** — Design and feature inspiration.

Special thanks to [darsh](https://github.com/its-darsh) (creator of Fabric), [gummy bear album](https://github.com/muhchaudhary), [axenide](https://github.com/Axenide), [sankalp](https://github.com/S4NKALP) for code contributions, bug fixes, and design ideas.

## Contributors

Thanks to all contributors ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/PixelKhaos"><img src="https://avatars.githubusercontent.com/u/5213174?v=4?s=100" width="100px;" alt="Robin Seger"/><br /><sub><b>Robin Seger</b></sub></a><br /><a href="https://github.com/rubiin/tsumiki/commits?author=PixelKhaos" title="Code">💻</a> <a href="#design-PixelKhaos" title="Design">🎨</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://zaap.bio/Axenide"><img src="https://avatars.githubusercontent.com/u/66109459?v=4?s=100" width="100px;" alt="Adriano Tisera"/><br /><sub><b>Adriano Tisera</b></sub></a><br /><a href="https://github.com/rubiin/tsumiki/commits?author=Axenide" title="Code">💻</a> <a href="https://github.com/rubiin/tsumiki/issues?q=author%3AAxenide" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Anshul-007"><img src="https://avatars.githubusercontent.com/u/81582218?v=4?s=100" width="100px;" alt="Anshul J."/><br /><sub><b>Anshul J.</b></sub></a><br /><a href="https://github.com/rubiin/tsumiki/commits?author=Anshul-007" title="Code">💻</a> <a href="https://github.com/rubiin/tsumiki/issues?q=author%3AAnshul-007" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/S4NKALP"><img src="https://avatars.githubusercontent.com/u/98226895?v=4?s=100" width="100px;" alt="Sankalp Tharu"/><br /><sub><b>Sankalp Tharu</b></sub></a><br /><a href="https://github.com/rubiin/tsumiki/commits?author=S4NKALP" title="Code">💻</a> <a href="https://github.com/rubiin/tsumiki/issues?q=author%3AS4NKALP" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/keepo-dot"><img src="https://avatars.githubusercontent.com/u/201014163?v=4?s=100" width="100px;" alt="Keepo"/><br /><sub><b>Keepo</b></sub></a><br /><a href="https://github.com/rubiin/tsumiki/commits?author=keepo-dot" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://evrenos-dev.vercel.app/"><img src="https://avatars.githubusercontent.com/u/138004078?v=4?s=100" width="100px;" alt="Sayeed Mahmood Evrenos"/><br /><sub><b>Sayeed Mahmood Evrenos</b></sub></a><br /><a href="https://github.com/rubiin/tsumiki/issues?q=author%3AEvren-os" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://xeyossr.github.io"><img src="https://avatars.githubusercontent.com/u/113219171?v=4?s=100" width="100px;" alt="xeyossr"/><br /><sub><b>xeyossr</b></sub></a><br /><a href="https://github.com/rubiin/tsumiki/commits?author=xeyossr" title="Documentation">📖</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://dimflix-official.github.io/"><img src="https://avatars.githubusercontent.com/u/112165977?v=4?s=100" width="100px;" alt="DIMFLIX"/><br /><sub><b>DIMFLIX</b></sub></a><br /><a href="https://github.com/rubiin/tsumiki/issues?q=author%3ADIMFLIX-OFFICIAL" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jhakonen"><img src="https://avatars.githubusercontent.com/u/1950698?v=4?s=100" width="100px;" alt="Janne Hakonen"/><br /><sub><b>Janne Hakonen</b></sub></a><br /><a href="https://github.com/rubiin/tsumiki/commits?author=jhakonen" title="Code">💻</a> <a href="https://github.com/rubiin/tsumiki/issues?q=author%3Ajhakonen" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/fdev31"><img src="https://avatars.githubusercontent.com/u/238622?v=4?s=100" width="100px;" alt="Fabien Devaux"/><br /><sub><b>Fabien Devaux</b></sub></a><br /><a href="https://github.com/rubiin/tsumiki/issues?q=author%3Afdev31" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/sudo-Tiz"><img src="https://avatars.githubusercontent.com/u/72883092?v=4?s=100" width="100px;" alt="Tiz"/><br /><sub><b>Tiz</b></sub></a><br /><a href="https://github.com/rubiin/tsumiki/commits?author=sudo-Tiz" title="Code">💻</a> <a href="https://github.com/rubiin/tsumiki/issues?q=author%3Asudo-Tiz" title="Bug reports">🐛</a> <a href="https://github.com/rubiin/tsumiki/commits?author=sudo-Tiz" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/N1xev"><img src="https://avatars.githubusercontent.com/u/104609053?v=4?s=100" width="100px;" alt="Alaa Elsamouly"/><br /><sub><b>Alaa Elsamouly</b></sub></a><br /><a href="https://github.com/rubiin/tsumiki/commits?author=N1xev" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/muhchaudhary"><img src="https://avatars.githubusercontent.com/u/61593188?v=4?s=100" width="100px;" alt="Muhammad Ahmad Chaudhary"/><br /><sub><b>Muhammad Ahmad Chaudhary</b></sub></a><br /><a href="https://github.com/rubiin/tsumiki/issues?q=author%3Amuhchaudhary" title="Bug reports">🐛</a></td>
    </tr>
  </tbody>
</table>
<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## License

Distributed under the [GPL-3.0 License](https://github.com/rubiin/tsumiki/blob/master/LICENSE).

<p align="center">
  ⭐ <strong>Star the repo</strong> if you find it useful!
</p>
