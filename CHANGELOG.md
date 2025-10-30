# Changelog

## [2.5.0](https://github.com/rubiin/Tsumiki/compare/v2.5.0...v2.5.0) (2025-10-30)


### ⚠ BREAKING CHANGES

* power profile
* no longer supports json5 on json, use json

### 🚀 New Features

* add 'show_when_no_windows' option to dock configuration and schema ([#148](https://github.com/rubiin/Tsumiki/issues/148)) ([cf77c12](https://github.com/rubiin/Tsumiki/commit/cf77c12f0b0a1195708463e44ae67deb0bc43ab8))
* add animation support to popover implementation ([540e625](https://github.com/rubiin/Tsumiki/commit/540e625054ff4bc63c285e13fa943d1c93da0838))
* add auto-hide option to updates widget and update related configurations ([4189dde](https://github.com/rubiin/Tsumiki/commit/4189ddebb8ad71ad30fae85253ceb0f210fd0f89))
* add auto-hide option to updates widget and update related configurations ([dd42c82](https://github.com/rubiin/Tsumiki/commit/dd42c825f6c45434481bfc1086e7a834038faf46))
* Add Auto-Reload Configuration Feature ([#156](https://github.com/rubiin/Tsumiki/issues/156)) ([55620f3](https://github.com/rubiin/Tsumiki/commit/55620f3da7f721dcd1da867897e2067a04b6d7a0))
* Add Auto-Reload Configuration Feature ([#156](https://github.com/rubiin/Tsumiki/issues/156)) ([7371b62](https://github.com/rubiin/Tsumiki/commit/7371b62e1ba5c99636e2a2fbd0352ce64a9f3834))
* add available_icon and no_updates_icon to updates configuration and refactor command building ([031d31f](https://github.com/rubiin/Tsumiki/commit/031d31f881b42f1bb54e52c530cc436f0f0c234c))
* add available_icon and no_updates_icon to updates configuration and refactor command building ([ada3758](https://github.com/rubiin/Tsumiki/commit/ada37587cf85757c9fe716897d0f613e6919ec2a))
* add BaseWindow class for custom window extensions ([cdd2c20](https://github.com/rubiin/Tsumiki/commit/cdd2c201fc33f18ebc0294ce606c1f1b71504693))
* add behavior configuration for dock widget and update related settings ([59a4bf4](https://github.com/rubiin/Tsumiki/commit/59a4bf4d7412ca93f6c4e9cd88d5d6cce4dfd3f9))
* add ClippingBox and LimitBox classes for enhanced widget functionality ([f38b06e](https://github.com/rubiin/Tsumiki/commit/f38b06e4d2855d1ae839f206109e86c548cf0c56))
* add close functionality for running apps in the dock ([43003a4](https://github.com/rubiin/Tsumiki/commit/43003a43f7a907cd93b7f7a60a57819bc368db37))
* Add collapsible group widget with popup menu ([#110](https://github.com/rubiin/Tsumiki/issues/110)) ([b361f00](https://github.com/rubiin/Tsumiki/commit/b361f007964355f5d96a58c97e121d6cfb5830d3))
* add configurable terminal support for updates widget ([#115](https://github.com/rubiin/Tsumiki/issues/115)) ([dedb63f](https://github.com/rubiin/Tsumiki/commit/dedb63f80130dd1224f87611007d38c53d526848))
* add confirmation option to power button actions and update related configurations ([c3baab6](https://github.com/rubiin/Tsumiki/commit/c3baab6a008f5c445b48abea8932d197ff5438b6))
* add custom button schema with properties for command, icon, label, and tooltip ([b8cfecd](https://github.com/rubiin/Tsumiki/commit/b8cfecd7c43279d007fe057b5cc286f1aab6a3fd))
* Add CustomButtonGroup Widget ([#114](https://github.com/rubiin/Tsumiki/issues/114)) ([1fae564](https://github.com/rubiin/Tsumiki/commit/1fae56496c40af54d9920e915e46d806b6a16fc6))
* Add CustomButtonGroup Widget ([#114](https://github.com/rubiin/Tsumiki/issues/114)) ([f853e05](https://github.com/rubiin/Tsumiki/commit/f853e05aa09448006b30a4994092716b125d7cac))
* Add CustomButtonGroup Widget ([#114](https://github.com/rubiin/Tsumiki/issues/114)) ([b880383](https://github.com/rubiin/Tsumiki/commit/b880383050dbd8e15abbc570832bb5fea1061578))
* add delayed recording options for recorder and screenshot widgets ([fbf1d9a](https://github.com/rubiin/Tsumiki/commit/fbf1d9a673d41ca7471908b4ab32b2dcf94db59e))
* add delayed recording options for recorder and screenshot widgets ([3c26ba0](https://github.com/rubiin/Tsumiki/commit/3c26ba057406ce347c3da976c7104af700fb20c0))
* add delayed recording options for recorder and screenshot widgets ([bf314d7](https://github.com/rubiin/Tsumiki/commit/bf314d784b35db4d21da5fb07be53673e666e5bb))
* add desktop quotes and activate Linux widgets with configuration options ([2ec78f1](https://github.com/rubiin/Tsumiki/commit/2ec78f19aadcc58cec58e602385f2a8328f7018f))
* add desktop quotes configuration and update activate Linux settings ([154e05e](https://github.com/rubiin/Tsumiki/commit/154e05edfc33ca701841703b637ba38b7d0dfc5c))
* add exclusive keyboard mode to OverViewOverlay popup ([dc3d05e](https://github.com/rubiin/Tsumiki/commit/dc3d05e4501734e2ce0afe70693408c1ad7fc100))
* add fallback option for window title configuration and logging ([9cd0a9b](https://github.com/rubiin/Tsumiki/commit/9cd0a9b9f7c752865d5791ad4b38b5f717391ddb))
* add force reinstall option to init.sh for updating python dependencies ([#208](https://github.com/rubiin/Tsumiki/issues/208)) ([9faa47a](https://github.com/rubiin/Tsumiki/commit/9faa47ad125a628e1bc2b5c121db60003b0b4102))
* add glace-git to installation script and remove unused app ID handling in dock ([31e0110](https://github.com/rubiin/Tsumiki/commit/31e01106624e7aefa3f728710b29b26dde8eee8f))
* add hide_on_default option to widgets and update submap behavior ([8d33143](https://github.com/rubiin/Tsumiki/commit/8d33143e05c8830d27ab1bcaaf4707fe27e4419c))
* add hover reveal and reveal duration properties for weather and updates widgets ([179dae4](https://github.com/rubiin/Tsumiki/commit/179dae4ad088ed86abccdea19a369e65415a4ad2))
* add hover reveal functionality for updates widget and adjust configuration options ([98dada2](https://github.com/rubiin/Tsumiki/commit/98dada298f6a0e4241e37246f02a8d2be8c4f870))
* add hover_reveal and reveal_duration options to DateTimeMenu and update transition_duration in widgets ([662df5d](https://github.com/rubiin/Tsumiki/commit/662df5ddcb431620e289e55fe0c63dafdda69fe3))
* add initial Renovate configuration for Python dependencies ([b09b819](https://github.com/rubiin/Tsumiki/commit/b09b81960cc9cfc2bba74b1106ab58c6c895094d))
* add instructions for installing extra stubs in CONTRIBUTING.md ([03943a5](https://github.com/rubiin/Tsumiki/commit/03943a597707aaec30ac3c77af2b841a976bd81c))
* add kb_digits and mb_digits options to network_usage in schema ([#125](https://github.com/rubiin/Tsumiki/issues/125)) ([dc0dabd](https://github.com/rubiin/Tsumiki/commit/dc0dabd49e53417404a2030fc76608a3b4ff4f57))
* add label formatting for weather widget and update humidity display ([113f1a8](https://github.com/rubiin/Tsumiki/commit/113f1a8cbe0d856c49116a828b218794471f4262))
* add label formatting for weather widget and update humidity display ([8843115](https://github.com/rubiin/Tsumiki/commit/88431158aa07aa514d05939c71848b42188b15a6))
* add mappings option to window title configuration and update related components ([#186](https://github.com/rubiin/Tsumiki/issues/186)) ([74b3e6d](https://github.com/rubiin/Tsumiki/commit/74b3e6dded52390ce85560d33d08372b16d22206))
* Add multi-monitor support ([#195](https://github.com/rubiin/Tsumiki/issues/195)) ([8804a73](https://github.com/rubiin/Tsumiki/commit/8804a733682c1c8a6586dd445beb3ef58c498dc3))
* add new sound assets and update documentation with unit and hover reveal properties ([7ebb90a](https://github.com/rubiin/Tsumiki/commit/7ebb90a6a0346862b580121d6f918164a9ae5c25))
* add option to hide battery widget when missing and disable quotes ([b6d8afd](https://github.com/rubiin/Tsumiki/commit/b6d8afd46b4a7b3c2265c79fcd1c8bb741680605))
* add option to hide systray when empty ([#105](https://github.com/rubiin/Tsumiki/issues/105)) ([f2132b7](https://github.com/rubiin/Tsumiki/commit/f2132b7f43a7fe84d1a6e18b87410f2217540735))
* add option to hide systray when empty ([#105](https://github.com/rubiin/Tsumiki/issues/105)) ([bf06ff9](https://github.com/rubiin/Tsumiki/commit/bf06ff9029ee0bcd1574c114c7717f447a21712f))
* add option to hide systray when empty ([#105](https://github.com/rubiin/Tsumiki/issues/105)) ([091ad00](https://github.com/rubiin/Tsumiki/commit/091ad00ef8516d23e745d0e8dc6759f55a6cbacc))
* add pad_zero option to updates and configuration for zero-padding updates ([2ddaef7](https://github.com/rubiin/Tsumiki/commit/2ddaef72ecfdd8aefd8224aa9eba38eab1657069))
* add pad_zero option to updates and configuration for zero-padding updates ([eb20f6b](https://github.com/rubiin/Tsumiki/commit/eb20f6b0e207a73daeb2d6fb2d43c6190e44515c))
* add pinned apps on Dock ([03943a5](https://github.com/rubiin/Tsumiki/commit/03943a597707aaec30ac3c77af2b841a976bd81c))
* add preview_apps option for dock functionality ([1750fe0](https://github.com/rubiin/Tsumiki/commit/1750fe0f37680e2bd8f7faa9316558a60335ebf5))
* add release workflow for automated changelog generation ([e4f0c72](https://github.com/rubiin/Tsumiki/commit/e4f0c72f8e6bb0a0a8e1edc09b26c7f71ce6812e))
* add reveal_duration option on date_time ([b9aee3f](https://github.com/rubiin/Tsumiki/commit/b9aee3f889859707aeaf2d3a952cbb4a55b8e62c))
* add screenshot widget configuration and styling options ([867e969](https://github.com/rubiin/Tsumiki/commit/867e9696cf772d0117ff827c668b3c93f0487b74))
* add search entry icons and clear functionality in app launcher and clip history menu ([681c4a9](https://github.com/rubiin/Tsumiki/commit/681c4a9477f59a20d64801abcfff80aaeac7c9dd))
* add setup_venv function for virtual environment management  ([#106](https://github.com/rubiin/Tsumiki/issues/106)) ([e1d69f6](https://github.com/rubiin/Tsumiki/commit/e1d69f629c6030b5757006c2ab6a686140d8fce7))
* add show_numbered option for workspaces configuration and widget display ([2186064](https://github.com/rubiin/Tsumiki/commit/2186064322f355492e350a3a4c109865ac851d1f))
* add support for customizable OSDs in configuration ([2406603](https://github.com/rubiin/Tsumiki/commit/2406603fc9694761b5c90d4a549ea5276e98ca15))
* add TeamSpeak to the window title map ([43dcb48](https://github.com/rubiin/Tsumiki/commit/43dcb48894ec917ac843640c78a5526880b12f31))
* add tooltip support for application buttons in AppBar ([03943a5](https://github.com/rubiin/Tsumiki/commit/03943a597707aaec30ac3c77af2b841a976bd81c))
* add tooltip support to window title widget ([781d5ae](https://github.com/rubiin/Tsumiki/commit/781d5ae60497cb9898ec23d87213965c4d42a1c2))
* add transition for OSD and notifications ([8228cb4](https://github.com/rubiin/Tsumiki/commit/8228cb4f059255b3dfe3fb79ae85ab14c6369082))
* add visual distinction for occupied workspaces ([#108](https://github.com/rubiin/Tsumiki/issues/108)) ([70a1a88](https://github.com/rubiin/Tsumiki/commit/70a1a8862fe8dd9807294fd34900b0c64476817c))
* add wallpaper widget with configuration options for icon, label, and tooltip ([947895b](https://github.com/rubiin/Tsumiki/commit/947895b7a3682ca012fc5e491738cf9419cdead5))
* add wallpaper widget with configuration options for icon, label, and tooltip ([947895b](https://github.com/rubiin/Tsumiki/commit/947895b7a3682ca012fc5e491738cf9419cdead5))
* add wallpaper widget with configuration options for icon, label, and tooltip ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* add wallpaper widget with configuration options for icon, label, and tooltip ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* add workflow to close stale issues and PRs automatically ([345dc02](https://github.com/rubiin/Tsumiki/commit/345dc025df06c3a793a9bed59ea15cfc11849167))
* allow delayed option on screenrecord and screenshot ([f3196c2](https://github.com/rubiin/Tsumiki/commit/f3196c2ebcb0d0c616c2a3c3eb3d0d0dcbd0593d))
* allow hiding the battery widget if none is present ([#103](https://github.com/rubiin/Tsumiki/issues/103)) ([b8f41cc](https://github.com/rubiin/Tsumiki/commit/b8f41ccee913a26f13c1fe398e431f4ecdfc97df))
* App launcher button and usable menu ([#197](https://github.com/rubiin/Tsumiki/issues/197)) ([d7f74eb](https://github.com/rubiin/Tsumiki/commit/d7f74eb8615f2e00dda81a757744480863801087))
* auto-copy config files from examples ([#107](https://github.com/rubiin/Tsumiki/issues/107)) ([225c292](https://github.com/rubiin/Tsumiki/commit/225c29287e6f9d4c400800c8dedd3c0163d7daa4))
* dynamically populate power profiles from available profiles ([9e8889f](https://github.com/rubiin/Tsumiki/commit/9e8889f6df2cbaf0e69520e8069856d72b2497ae))
* enhance app launcher with tooltip and icon size adjustments; set process name in GLib ([72128c4](https://github.com/rubiin/Tsumiki/commit/72128c4ecab1ae2df14f2be4016b3b0d26f184e6))
* enhance context menu to support pinning and unpinning applications ([00b7d49](https://github.com/rubiin/Tsumiki/commit/00b7d49e1a9c1e080a814640923b35fc046c738c))
* enhance init script with multiple arguments support ([#112](https://github.com/rubiin/Tsumiki/issues/112)) ([6b21b4a](https://github.com/rubiin/Tsumiki/commit/6b21b4a2b7db280bad47bbceafcef6221e2947ed))
* enhance widget configuration with unit support for memory and storage ([283a75e](https://github.com/rubiin/Tsumiki/commit/283a75e26bbdf63f75ae52ecd91228579f38cfa6))
* establish Hyprland connection in HyprSunsetSubMenu for dynamic command execution ([62cb3be](https://github.com/rubiin/Tsumiki/commit/62cb3be111ee46bc154ec694cb3cd97ef497ca8e))
* implement battery notifications ([#144](https://github.com/rubiin/Tsumiki/issues/144)) ([25bdc8f](https://github.com/rubiin/Tsumiki/commit/25bdc8fe50bd589eb2895a99c0e39dcfd362a97b))
* implement hover reveal functionality for weather widget with configurable reveal duration ([251e3de](https://github.com/rubiin/Tsumiki/commit/251e3debeb018ef6029dbe1f0aa306fd00274b8c))
* implement overview button widget and related configuration ([cf1b547](https://github.com/rubiin/Tsumiki/commit/cf1b54706f3b5ac0615fe4ebf2a8cbf677ba7d8c))
* implement overview button widget and update configuration for overview functionality ([1c48dc1](https://github.com/rubiin/Tsumiki/commit/1c48dc1ba7bfa036916f9340ea306b555156d5d4))
* implement process name setting and improve notification sound handling ([0d09bb6](https://github.com/rubiin/Tsumiki/commit/0d09bb64d40939d6516f07b3e138800f3da8c5a5))
* new dock ([947895b](https://github.com/rubiin/Tsumiki/commit/947895b7a3682ca012fc5e491738cf9419cdead5))
* new dock ([947895b](https://github.com/rubiin/Tsumiki/commit/947895b7a3682ca012fc5e491738cf9419cdead5))
* refactor AppBar to improve pinned apps handling and app lookup efficiency ([886da76](https://github.com/rubiin/Tsumiki/commit/886da76e693510274239614662b20e5015e6897e))
* refactor init script and add detached option ([#157](https://github.com/rubiin/Tsumiki/issues/157)) ([b5a0743](https://github.com/rubiin/Tsumiki/commit/b5a074310db05eda2cff16f0e9440e509b66090f))
* refactor popover implementation to remove animation support and simplify code ([1574b67](https://github.com/rubiin/Tsumiki/commit/1574b67c4a32080516c6d440f37fb66b56ad88ea))
* require Gtk 3.0 version in multiple files for compatibility ([06bed98](https://github.com/rubiin/Tsumiki/commit/06bed988e2f0fc6a457384c3a148781a430dc474))
* update battery and storage widget configurations in schema and example config ([fd3d677](https://github.com/rubiin/Tsumiki/commit/fd3d67736fd5a56b2ff3dd821ce648a35e153bb8))
* update stubs_gen command to include additional dependencies ([5c228fa](https://github.com/rubiin/Tsumiki/commit/5c228fa44543e87ba181c3d690345c1bbd52310c))
* **utils:** add Matugen palette generator ([79beab2](https://github.com/rubiin/Tsumiki/commit/79beab26086f89ff0210de6f0fbcc11ca1fab7e6))


### 🐛 Bug Fixes

* :Modified power button styles in power.scss to adjust padding and label font size. ([eb7c647](https://github.com/rubiin/Tsumiki/commit/eb7c647da4cfb129153bbdcb6fde09a5bda5805c))
* add 'autorelease: pending' to exempt-issue-labels in lock.yml ([ecee420](https://github.com/rubiin/Tsumiki/commit/ecee420ee64ffc0488b5547b9a3671eb6990e00c))
* add check for screen device before updating brightness values ([def75ab](https://github.com/rubiin/Tsumiki/commit/def75abc3cc168ecc032100c9a286c5e3f3a79cb))
* add check for screen device before updating brightness values ([a618f49](https://github.com/rubiin/Tsumiki/commit/a618f490a4a298ba8bfa26046bde39b23bc0979f))
* add check for screen device before updating brightness values ([3b4389b](https://github.com/rubiin/Tsumiki/commit/3b4389b55db3a61e7cac2622cab4e0e71b90dd53))
* add check for screen device before updating brightness values ([7f2e758](https://github.com/rubiin/Tsumiki/commit/7f2e758838c82f3181a63f69b2bb667bdc8cf78e))
* add circular progress bar to notification widget and implement timeout animation ([3b81fca](https://github.com/rubiin/Tsumiki/commit/3b81fca7ff6703d5136b4a34bc662aa12592940a))
* add Custom_Button_Group and Collapsible_Group TypedDicts for enhanced widget configuration ([0b4f82c](https://github.com/rubiin/Tsumiki/commit/0b4f82cf2d26c55d8228221782f15935fb005949))
* add default values to various properties in schema for improved configuration ([52e62b0](https://github.com/rubiin/Tsumiki/commit/52e62b029576f5130d95d4bb38223aa0c4068dcd))
* add default values to various properties in schema for improved configuration ([8bcfc53](https://github.com/rubiin/Tsumiki/commit/8bcfc536440927244a7083b4b324078203ea3f2c))
* add delay before starting Tsumiki ([729ed95](https://github.com/rubiin/Tsumiki/commit/729ed95b775a0335c4b0f18cd27f68e3d9ac1171))
* add ellipsization to WiFi SSID button for better text handling ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* add ellipsization to WiFi SSID button for better text handling ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* add ellipsization to WiFi SSID button for better text handling ([d2153b5](https://github.com/rubiin/Tsumiki/commit/d2153b532d7868feefb073798ca682daeccac890))
* add error handling and logging for monitor and keyboard layout retrieval ([5beca69](https://github.com/rubiin/Tsumiki/commit/5beca69e7e57327cee7fa6c422041c93847d4747))
* add error handling and logging for monitor and keyboard layout retrieval ([02ebed4](https://github.com/rubiin/Tsumiki/commit/02ebed4e50b25475d40c741849c2e2edeab78b2e))
* add file monitoring for CSS changes and improve debug logging condition ([2940a7c](https://github.com/rubiin/Tsumiki/commit/2940a7c8ffe689291e8a49e1a2ad060616a86e34))
* add font size to panel-font-icon in quicksettings styles ([d2d321f](https://github.com/rubiin/Tsumiki/commit/d2d321fcfb81b714d80870bd722b346697844e00))
* add icon size to app launcher button and update layout sections ([a59d183](https://github.com/rubiin/Tsumiki/commit/a59d18391215df21ddfea08efbcda54a14fdfeef))
* add icon to uptime ([#219](https://github.com/rubiin/Tsumiki/issues/219)) ([1217566](https://github.com/rubiin/Tsumiki/commit/1217566600ef7080d29e96c8a93fcd8834b25300))
* add mappings option to window_title widget and disable monitor_styles in general settings ([23b9da1](https://github.com/rubiin/Tsumiki/commit/23b9da1e7db6552f82e9b9dc2d79cb29edf95cae))
* add missing import of Iterable in widget_container.py ([dd5cee9](https://github.com/rubiin/Tsumiki/commit/dd5cee916d4f5d51789a901c45e0470a10a6021e))
* add missing newlines and improve SVG structure for consistency across icon files ([8f09e47](https://github.com/rubiin/Tsumiki/commit/8f09e472f1289d6ab1461931bd629a01772f21a4))
* add more operations on doc menu ([19444bd](https://github.com/rubiin/Tsumiki/commit/19444bd502df65fd8b88811de20df881d96015aa))
* add name attribute to dock and osd modules for better identification ([3ff5ddb](https://github.com/rubiin/Tsumiki/commit/3ff5ddb6927604479632ca9680b77913b3fddb58))
* add name parameter to PopupWindow for better identification in PowerMenuPopup ([1395e48](https://github.com/rubiin/Tsumiki/commit/1395e48414f4401912b45d84d23d24541bebe9ac))
* add separator to AppBar and update visibility logic based on pinned apps ([5ae6623](https://github.com/rubiin/Tsumiki/commit/5ae66231e94b65e89b25bca69bb6fc36a3e29362))
* add type hint for config attribute in ButtonWidget class ([afcab11](https://github.com/rubiin/Tsumiki/commit/afcab11cf099a8b4602ef8aa49e46ac7923cbb1c))
* add type hint for config parameter in PowerMenuPopup constructor ([e03e5b4](https://github.com/rubiin/Tsumiki/commit/e03e5b4c03fae720decd9b975acd86a2d20c1063))
* add type hints for config parameter in multiple widget constructors ([61f51a4](https://github.com/rubiin/Tsumiki/commit/61f51a41159725a62247b2dc786ebb1f1010b1b5))
* adjust bluetooth icon size and update chevron icon styling ([6e9f754](https://github.com/rubiin/Tsumiki/commit/6e9f75400623aba4947496bb3209c92866f2d6c0))
* adjust margin for activate_linux box in widgets styles ([b157e2c](https://github.com/rubiin/Tsumiki/commit/b157e2cd47e3686966666d663bc182fa899ac002))
* adjust max character width for notification widget and enhance opacity in media styles for better visibility ([69a36a9](https://github.com/rubiin/Tsumiki/commit/69a36a9ba12b6291661ceba31da0adf4e403d3d7))
* adjust truncation size and disable mappings in window title configuration ([e5f1de4](https://github.com/rubiin/Tsumiki/commit/e5f1de49d1b573f803ec0e590b6a8871b84d3686))
* align close button to the start in notification and datetime menu widgets ([c563f67](https://github.com/rubiin/Tsumiki/commit/c563f6795dacadcdd784149891628f126630b12f))
* allow customizable size for DotIndicator and simplify app launcher toggle logic ([465e0ed](https://github.com/rubiin/Tsumiki/commit/465e0ed5654c71b8feb803c175b8be40ab0e18be))
* call check_for_windows method in Dock class to ensure window checks are performed on start ([202b369](https://github.com/rubiin/Tsumiki/commit/202b36999f1aa0e09d452179ddf728b45647509e))
* center align close button in notification and datetime menu widgets ([50402a2](https://github.com/rubiin/Tsumiki/commit/50402a2be02c54fc5c863d47ba0cd4ce190a86ec))
* center align close button in NotificationWidget overlay ([025d4df](https://github.com/rubiin/Tsumiki/commit/025d4df2c72a5af7fbc8b2250c327512781d3e8e))
* Centralize Signal Connections in HyprSunset Widget ([#111](https://github.com/rubiin/Tsumiki/issues/111)) ([ee5744f](https://github.com/rubiin/Tsumiki/commit/ee5744fcc125368a0237725d61b21054768c5057))
* Centralize Signal Connections in HyprSunset Widget ([#111](https://github.com/rubiin/Tsumiki/issues/111)) ([8791abb](https://github.com/rubiin/Tsumiki/commit/8791abb92890d784914607ebe2a6433cd4ca3ce1))
* change desktop clock label color to white for better visibility ([1f91ee5](https://github.com/rubiin/Tsumiki/commit/1f91ee59b72144e6fb346414cf6e16b27b643642))
* change OSD transition type from slide-right to slide-up ([52e28fc](https://github.com/rubiin/Tsumiki/commit/52e28fcef6a872389821d5bddfafe55113eec890))
* change OSD transition type from slide-right to slide-up ([2de9027](https://github.com/rubiin/Tsumiki/commit/2de9027196b53543ee4126a8efb041013fc187f6))
* change transition type to slide-down for dialog and power menu popups ([b9972bf](https://github.com/rubiin/Tsumiki/commit/b9972bf7ca631a7744521851d483f48b3d1c55b8))
* clean up default configuration by removing unnecessary comments and duplicate icon entry ([999889c](https://github.com/rubiin/Tsumiki/commit/999889ce1bca9ef471085633d1324c97f94d1a90))
* clear memory ([4281fb6](https://github.com/rubiin/Tsumiki/commit/4281fb6d2ce5f5061c234d9bd77fbfa6d8cae15f))
* clipboard manager UTF-8 encoding ([fcd8156](https://github.com/rubiin/Tsumiki/commit/fcd8156a21dc5162cd2b952b332292968a74e045))
* close active submenus when QuickSettingsButtonBox is unmapped ([174dd67](https://github.com/rubiin/Tsumiki/commit/174dd672bc15aa6ebbf77acf7a79738f6ed8c9f4))
* close popover when overlay is clicked ([#99](https://github.com/rubiin/Tsumiki/issues/99)) ([85a2023](https://github.com/rubiin/Tsumiki/commit/85a202331b028ed0da9c3b6ca79c2a53b25f30f5))
* comment out handler block/unblock calls in update_volume method ([abee03d](https://github.com/rubiin/Tsumiki/commit/abee03d70d785554e0bdc0f1270e6cc1863948b3))
* connect action button click event directly in initialization for improved readability ([234a16b](https://github.com/rubiin/Tsumiki/commit/234a16ba599d3a7551dafead9a288fa866b8eb35))
* connect button click events directly in button initialization for improved readability ([d40a845](https://github.com/rubiin/Tsumiki/commit/d40a845727fa89b4e5ceff6518c1529f8e8a3cb7))
* consolidate transition styles into scrolledwindow and remove redundant button hover styles ([aaa5ecf](https://github.com/rubiin/Tsumiki/commit/aaa5ecf07d541c989c919e24992cd91fee284b0b))
* correct formatting in installation message and simplify app ID change handling in AppBar ([8ebb6c9](https://github.com/rubiin/Tsumiki/commit/8ebb6c92fb41cc4da1c0761284d998d7cd77cbca))
* correct formatting of dotfiles link in README ([8299fc7](https://github.com/rubiin/Tsumiki/commit/8299fc790e91fe1e366b7acbc80e55a16c3156b1))
* correct GLib idle_add usage for update_status_once ([238929a](https://github.com/rubiin/Tsumiki/commit/238929a0ee77116742e282120f75570a3220cf01))
* correct method signature for on_shuffle_update in PlayerBox ([1932704](https://github.com/rubiin/Tsumiki/commit/193270433c5c41d4161541fe54952c345695095a))
* correct pin action to use _pin_running_app method ([e64c0b6](https://github.com/rubiin/Tsumiki/commit/e64c0b627e83215613e0d5d6a9c970e4b60a9afd))
* correct syntax in configuration and battery widget initialization ([56fdf4e](https://github.com/rubiin/Tsumiki/commit/56fdf4e25879494639bd9130d15bbfe6aac12c45))
* Correct terminal command execution for multiple terminal types ([65ef1be](https://github.com/rubiin/Tsumiki/commit/65ef1be4a90bde53a5acfd35c3afb25c4fe8d627))
* correct typo in config attribute access in WindowTitleWidget class ([c232920](https://github.com/rubiin/Tsumiki/commit/c232920f5e5d2a484e47e7a86eca733c98ad4fac))
* disable desktop clock and add configuration for desktop quotes ([81d9ffd](https://github.com/rubiin/Tsumiki/commit/81d9ffde8e71c64d04c22262c4525ea444b31eb7))
* disable overview widget by default ([1d8c346](https://github.com/rubiin/Tsumiki/commit/1d8c34682f6cb3ae5d4619721a9484ca6a56323b))
* disable tooltip feature in default configuration ([310084c](https://github.com/rubiin/Tsumiki/commit/310084cf5049a35b27f430b73ea2ecf7832fb52c))
* disable tooltip feature in default configuration ([845b774](https://github.com/rubiin/Tsumiki/commit/845b77487e4169a08d5b6c0f047a71f5cb07881b))
* do not disturb toggle functionality in DateNotificationMenu ([c0eaa7b](https://github.com/rubiin/Tsumiki/commit/c0eaa7bdd150edc1253bbae0388f257c9580cb44))
* don't use get_relative_path multiple times if you can freaking avoid it ([690b39a](https://github.com/rubiin/Tsumiki/commit/690b39a80badd79113925bd79f4c462584fa39e0))
* downgrade pygobject ([d5b8c3d](https://github.com/rubiin/Tsumiki/commit/d5b8c3d4323f88f349d7056939bc0779ef9e9b4f))
* emoji picker close popup issue ([be8ab0e](https://github.com/rubiin/Tsumiki/commit/be8ab0e158a5aa6e29ab5316060a5bd553df2165))
* emoji picker close popup issue ([20e95fb](https://github.com/rubiin/Tsumiki/commit/20e95fb574b0ee1fce9f783162c4703a4a664410))
* enhance app ID notification handling to include tooltip updates for client buttons ([5521cac](https://github.com/rubiin/Tsumiki/commit/5521cac4626555345c6226b6da1e70a00feb7438))
* enhance config auto-reload functionality and improve logger messages ([8b236db](https://github.com/rubiin/Tsumiki/commit/8b236db559a62cf32263d11c9af5fac4812653e6))
* enhance config auto-reload functionality and improve logger messages ([2c71b10](https://github.com/rubiin/Tsumiki/commit/2c71b10c3c9a41c4e8b8aa6075cfd276923c76a8))
* enhance forecast box cleanup by destroying child widgets when removed ([5488bd0](https://github.com/rubiin/Tsumiki/commit/5488bd079e4fc88f0858e6c0b934e8a8bbd67494))
* enhance JSON handling and error logging in various widgets ([2b821be](https://github.com/rubiin/Tsumiki/commit/2b821be6f43c72a5aabba55a54aa303a0840880e))
* enhance notification and app widget text wrapping and character limits for improved readability ([fbac91e](https://github.com/rubiin/Tsumiki/commit/fbac91e2535ae64e99c3323194ddd50ae81cccf1))
* enhance notification box hover effect with transition and background color ([322d4cb](https://github.com/rubiin/Tsumiki/commit/322d4cb21c4a048c1769acef7c47e0049b871a76))
* enhance workspace movement functionality by converting client address to hex format ([b1e82a6](https://github.com/rubiin/Tsumiki/commit/b1e82a6be601f86b951fdd1c798868d756be6450))
* ensure dialog popup toggles after executing command ([90f43c5](https://github.com/rubiin/Tsumiki/commit/90f43c52bb48739cb000ca3ff44960228a5e072a))
* ensure fallback title is consistently lowercased in WindowTitleWidget ([cab291e](https://github.com/rubiin/Tsumiki/commit/cab291ea1c85bcb959c70199d44733078481ca1b))
* ensure proper cleanup of app bar items by destroying the box on close ([c40c9dd](https://github.com/rubiin/Tsumiki/commit/c40c9dd1fbaf72f361d474791f4601f8ae70bcd3))
* ensure proper cleanup of Bluetooth device rows by destroying the row on removal ([5488bd0](https://github.com/rubiin/Tsumiki/commit/5488bd079e4fc88f0858e6c0b934e8a8bbd67494))
* ensure rebase occurs when conflicts are detected ([c3b0950](https://github.com/rubiin/Tsumiki/commit/c3b095054d5eb485dac83a715de79b306a6b7fb6))
* ensure truncation behavior respects configuration in WindowTitleWidget ([30533af](https://github.com/rubiin/Tsumiki/commit/30533af94a2424a36fa7bb83cab885078e0f83cc))
* format JSON schema for better readability and update enum values in definitions ([3029405](https://github.com/rubiin/Tsumiki/commit/302940532c57a7b0e38f4aaa201edd95e81747fc))
* format wallpaper properties in schema for consistency ([9ab35ac](https://github.com/rubiin/Tsumiki/commit/9ab35acb21c3d4ae1f00ace9186038a996920be2))
* format wallpaper properties in schema for consistency ([05682b4](https://github.com/rubiin/Tsumiki/commit/05682b4fffd0b284f79faa7d87be56b2432c979a))
* get client data method ([dc28a8b](https://github.com/rubiin/Tsumiki/commit/dc28a8b5cc2a21c39d95d2d7eb61c30111933f10))
* hyprsunset slider functionality ([#109](https://github.com/rubiin/Tsumiki/issues/109)) ([b0722bc](https://github.com/rubiin/Tsumiki/commit/b0722bcd2cdca15d5c041b04fd2734b09fbce5f7))
* hyprsunset slider functionality ([#109](https://github.com/rubiin/Tsumiki/issues/109)) ([ca39938](https://github.com/rubiin/Tsumiki/commit/ca399383af640cef6831cc2d23d262f2590c1823))
* hyprsunset slider functionality ([#109](https://github.com/rubiin/Tsumiki/issues/109)) ([ae12cf4](https://github.com/rubiin/Tsumiki/commit/ae12cf43a6b22e5e84bea6ce27114005d95422e1))
* hyprsunset slider functionality ([#109](https://github.com/rubiin/Tsumiki/issues/109)) ([c536475](https://github.com/rubiin/Tsumiki/commit/c5364751dfd11609dbe20472ff2b0c506f216735))
* hyprsunset slider functionality ([#109](https://github.com/rubiin/Tsumiki/issues/109)) ([cfbf745](https://github.com/rubiin/Tsumiki/commit/cfbf74537da83eae835986346f8c519bf10a5408))
* implement app launcher toggle functionality in AppBar and update dock style reference ([7a9e854](https://github.com/rubiin/Tsumiki/commit/7a9e854d5692fb39b3298beb8218dc4fdbd71aad))
* implement sound capture option in screen recording and screenshot methods ([7c51470](https://github.com/rubiin/Tsumiki/commit/7c51470748d4b127fa260a21bc80c49cfde037a5))
* improve alignment and spacing in notification and datetime menu widgets for better layout ([df53f47](https://github.com/rubiin/Tsumiki/commit/df53f4716bfaa8b79a92b6d9934ca0f785432bde))
* improve app preview handling on mouse enter and leave events ([39ab33b](https://github.com/rubiin/Tsumiki/commit/39ab33b84d76b48fbcc4af522fec8c921e6e0cd4))
* improve notification loading and validation process in CustomNotifications ([cac5b44](https://github.com/rubiin/Tsumiki/commit/cac5b44b272e3d85c61deefef0137d5455a32017))
* improve notification validation and persistence in CustomNotifications ([6809882](https://github.com/rubiin/Tsumiki/commit/680988207a37df9d14143e2e16ab08bfbfe3df4e))
* Improve output formatting and error messages in init.sh; refactor collapsible_group.py and stats.py for better readability ([78ba872](https://github.com/rubiin/Tsumiki/commit/78ba8725e1b1d623919bb64ff92fd14936d134bc))
* improve path handling and error logging in screen recording and screenshot methods ([66ef283](https://github.com/rubiin/Tsumiki/commit/66ef2834dfdb2f135bfd587a09cdb419a7af5c4c))
* increase max character width for notification summary and body for better readability ([2e03b76](https://github.com/rubiin/Tsumiki/commit/2e03b76cd5feb564b8972b9cfaeb8b74a5580698))
* init.sh to work from any directory ([#113](https://github.com/rubiin/Tsumiki/issues/113)) ([3e235e4](https://github.com/rubiin/Tsumiki/commit/3e235e4f9bdbaeaa6594a7a084fe5d68861f62b0))
* install packages command ([af74941](https://github.com/rubiin/Tsumiki/commit/af749410a3c2f92365f79d12b80bd5f18c3c6a03))
* integrate BaseWidget into various widget classes for consistency ([27c87ee](https://github.com/rubiin/Tsumiki/commit/27c87ee79c909a684db5b61f2302ca72be310ec2))
* integrate CircularImage into AppBar and update related styles and schema ([d908d66](https://github.com/rubiin/Tsumiki/commit/d908d66c056cb2346e540081a24845ad8baf434b))
* make animated scale more robust ([#221](https://github.com/rubiin/Tsumiki/issues/221)) ([afd7b76](https://github.com/rubiin/Tsumiki/commit/afd7b760491b6da064c482dc092174b648f1e3ab))
* move application start logging before running the app for better clarity ([f9dff5f](https://github.com/rubiin/Tsumiki/commit/f9dff5f8e54fa6691784a74973dc5e4d5a3949ea))
* nested ([bd86a51](https://github.com/rubiin/Tsumiki/commit/bd86a5168f3b8d22458387b798dad6825ed14ab7))
* network initialisation when no network available ([#209](https://github.com/rubiin/Tsumiki/issues/209)) ([15fc47b](https://github.com/rubiin/Tsumiki/commit/15fc47bbacf4c3f0da8df219c353b7eb3a2b51e9))
* **network-usage:** auto unit (B/s, KB/s, MB/s) with 2 digits ([#116](https://github.com/rubiin/Tsumiki/issues/116)) ([37f1aa5](https://github.com/rubiin/Tsumiki/commit/37f1aa54a80428da5062b59ec0d7ea49f91a8962))
* **network-usage:** update speed formatting to use whole numbers for KB/s and MB/s ([5b56a91](https://github.com/rubiin/Tsumiki/commit/5b56a91acf068af6b251ccbbdbfaa33e801fe38a))
* new version with client capture ([886da76](https://github.com/rubiin/Tsumiki/commit/886da76e693510274239614662b20e5015e6897e))
* optimize notification validation and deserialization process ([82a8422](https://github.com/rubiin/Tsumiki/commit/82a8422d1ef41ecee1f17f11d742beb4aae72ca7))
* osd style class names ([54f7d36](https://github.com/rubiin/Tsumiki/commit/54f7d36abcd2c6d023234e3114d65ad7e5125927))
* overview widget ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* overview widget fixes ([#135](https://github.com/rubiin/Tsumiki/issues/135)) ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* overview widget fixes ([#135](https://github.com/rubiin/Tsumiki/issues/135)) ([6f207fb](https://github.com/rubiin/Tsumiki/commit/6f207fb9cade144342a579084a0f8e84db9e2e06))
* pass widget_config to OverViewOverlay for proper initialization ([f7e0d46](https://github.com/rubiin/Tsumiki/commit/f7e0d46a647543aefe069b0054bcd37376b2ba34))
* pin PyGObject version to 3.50.0 for compatibility ([65f4382](https://github.com/rubiin/Tsumiki/commit/65f438208dfe3553bad0a10927f94393b5640eb1))
* power profile ([9810cc8](https://github.com/rubiin/Tsumiki/commit/9810cc81e9ab7e2beb2a50f229c2b9a742cfe702))
* prevent displaying '0' in label when total updates are zero and pad_zero is enabled ([ebcc2ce](https://github.com/rubiin/Tsumiki/commit/ebcc2ce7174a51ac4898e4570dd2fb4c213cb2cf))
* prevent multiple simultaneous wallpaper loads in WallpaperPickerBox ([b89cff4](https://github.com/rubiin/Tsumiki/commit/b89cff41680d87ef4edccf4175e637d4b2e8dac1))
* prevent unnecessary removal of muted style class in AudioOSDContainer ([7671ff9](https://github.com/rubiin/Tsumiki/commit/7671ff91e77093c56a777953f201cc4749cc244b))
* prevent unnecessary removal of muted style class in AudioOSDContainer ([d1be0e8](https://github.com/rubiin/Tsumiki/commit/d1be0e89a7d0b3f9809d2b0a95bb0c5f30a36072))
* reduce vertical padding in dock and app launcher settings for improved layout consistency ([150333d](https://github.com/rubiin/Tsumiki/commit/150333d8f6e148a15cd5c3e5e68b4fc623ee5eed))
* redundant icon size ([947895b](https://github.com/rubiin/Tsumiki/commit/947895b7a3682ca012fc5e491738cf9419cdead5))
* redundant icon size ([947895b](https://github.com/rubiin/Tsumiki/commit/947895b7a3682ca012fc5e491738cf9419cdead5))
* redundant icon size ([947895b](https://github.com/rubiin/Tsumiki/commit/947895b7a3682ca012fc5e491738cf9419cdead5))
* redundant icon size ([947895b](https://github.com/rubiin/Tsumiki/commit/947895b7a3682ca012fc5e491738cf9419cdead5))
* redundant icon size ([947895b](https://github.com/rubiin/Tsumiki/commit/947895b7a3682ca012fc5e491738cf9419cdead5))
* redundant icon size ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* redundant icon size ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* redundant icon size ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* redundant icon size ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* redundant icon size ([528e2f2](https://github.com/rubiin/Tsumiki/commit/528e2f2b90facb7bac6e98366d04f177e4cbc290))
* redundant icon size ([db88bd5](https://github.com/rubiin/Tsumiki/commit/db88bd5c7396d201397d98e864aa5a60ff312a3e))
* refactor AppBar initialization and clean up unused styles in dock ([d66b247](https://github.com/rubiin/Tsumiki/commit/d66b2475a243fb04885e0e8e1c6395cc5971e1cd))
* refactor AppLauncher viewport initialization and add CheatSheet and KeybindLoader classes ([ccaf9cf](https://github.com/rubiin/Tsumiki/commit/ccaf9cfbeb1e295b52aa7ac75f7ce9a315a1c7e7))
* refactor init_device_audio method for clarity and remove nested function ([b1ad892](https://github.com/rubiin/Tsumiki/commit/b1ad8929c89884063871b431f61a135cf6204579))
* refactor submenu handling in QuickSettingsButtonBox ([27443ec](https://github.com/rubiin/Tsumiki/commit/27443ecb2e6c65491eed234cfd7c2ab443cc82bd))
* refactor update_arch function to improve aur_helper assignment and add ASCII art ([c683503](https://github.com/rubiin/Tsumiki/commit/c683503794859a18fc5df272c0b31b4e212a8643))
* refactor update_arch function to improve aur_helper assignment and add ASCII art ([ef24eba](https://github.com/rubiin/Tsumiki/commit/ef24ebabac7557aeaed52d16cc0f7db839d4e4ac))
* regression on collapisble_groups ([#128](https://github.com/rubiin/Tsumiki/issues/128)) ([bbfc2d5](https://github.com/rubiin/Tsumiki/commit/bbfc2d52f05f17f893eb75126c5806b66e5cfffb))
* remove debug print statement from on_scroll method in DateNotificationMenu ([f6d6457](https://github.com/rubiin/Tsumiki/commit/f6d645791f1fbd9230c140f6f3d3c57920c36924))
* remove default theme configuration from constants ([0d5306b](https://github.com/rubiin/Tsumiki/commit/0d5306bb56236b7536a761925926b6b7d8e86c9d))
* remove ellipsize property from application widget label for improved text display ([065476a](https://github.com/rubiin/Tsumiki/commit/065476a85672c2597ca1d14b150d47ca859051a6))
* remove horizontal alignment from ButtonWidget container box ([026d893](https://github.com/rubiin/Tsumiki/commit/026d893f38b37d33e5d8c9c349df40f3b8b6acf9))
* remove logging of command toggle state in CommandSwitcher ([530275f](https://github.com/rubiin/Tsumiki/commit/530275f754af2f460b694c2e61d7e56dd8ca4aaf))
* remove outdated instructions for hiding the bar on keypress ([947895b](https://github.com/rubiin/Tsumiki/commit/947895b7a3682ca012fc5e491738cf9419cdead5))
* remove outdated instructions for hiding the bar on keypress ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* remove outdated instructions for hiding the bar on keypress ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* remove pin option from Renovate configuration ([1e04466](https://github.com/rubiin/Tsumiki/commit/1e04466493dba69e27c42433760bdb93e8062ae4))
* remove redundant icon_size property from bluetooth, recorder, and screenshot widgets ([9ed5dc1](https://github.com/rubiin/Tsumiki/commit/9ed5dc12694dd6d6db8667de0fae039e6f112ae4))
* remove the weird ass pblm that somtimes caused the popup to not get closed, yipee ([82d640b](https://github.com/rubiin/Tsumiki/commit/82d640bde4c4851326310d49ce095998cc3d8c7e))
* remove unnecessary 'all_visible' parameter from widget initialization in multiple modules ([321a335](https://github.com/rubiin/Tsumiki/commit/321a33535cc59884d9624cad55fdf627571a4504))
* remove unnecessary blank line in BluetoothSubMenu class ([947895b](https://github.com/rubiin/Tsumiki/commit/947895b7a3682ca012fc5e491738cf9419cdead5))
* remove unnecessary comments and improve code clarity in widget initializations ([4183b3a](https://github.com/rubiin/Tsumiki/commit/4183b3ad5c54e50d01b09485ebcd8aa04683ad76))
* remove unnecessary conditional checks in setup_venv function ([b1858e3](https://github.com/rubiin/Tsumiki/commit/b1858e31af75420e1e14c9fd4f6de9c1a611cc26))
* remove unused import and clean up label handling in AudioSlider and BluetoothDeviceBox ([89231ed](https://github.com/rubiin/Tsumiki/commit/89231edcf322ca42e027184b4a3abf77b7a47e90))
* remove unused import of Iterable in widget_container.py ([5f5664b](https://github.com/rubiin/Tsumiki/commit/5f5664bddac62f79571d9b76b9821243adc97fc1))
* remove unused spacing configuration from constants ([d568a24](https://github.com/rubiin/Tsumiki/commit/d568a24e0168dfb9e35fe0711a7023d412c27b9b))
* remove unused style properties and improve label handling in popover and bluetooth submenu ([6b26a56](https://github.com/rubiin/Tsumiki/commit/6b26a56291849468870581c20db8e2dc6929c920))
* remove unused widgets from collapsible groups and center align button container ([af32895](https://github.com/rubiin/Tsumiki/commit/af328956ce29f431109a7044a82c34067e3c2f03))
* remove VSCode settings file to streamline configuration ([1f31551](https://github.com/rubiin/Tsumiki/commit/1f315510869a17f5c963aa5da1fccffff26d6529))
* rename CircleImage to CircularImage across multiple modules ([d6ba3a3](https://github.com/rubiin/Tsumiki/commit/d6ba3a37ef8ce05d1cf5eb1f8f15938d0c7a9b52))
* rename update methods to use a consistent naming convention across multiple widgets ([10c4864](https://github.com/rubiin/Tsumiki/commit/10c486407154c0e3b5fe83c513c53e3b10cd69e1))
* reorder battery settings and add overview to middle section in layout ([79f15da](https://github.com/rubiin/Tsumiki/commit/79f15da8a6f0c269bb1bb8a333ca805eb92c329e))
* reorder dependencies for consistency and clarity ([a25c272](https://github.com/rubiin/Tsumiki/commit/a25c2728a6171aad53859594e52f14042ae89036))
* reorder dependencies for consistency and clarity ([f3a5120](https://github.com/rubiin/Tsumiki/commit/f3a51201374886aa76f6e2367db8ea994b690c0e))
* reorder dependencies for consistency and clarity ([ad00171](https://github.com/rubiin/Tsumiki/commit/ad0017168f17e049d9f0a4ea5c834e458c60b8b7))
* replace HyprlandWithMonitors with get_hyprland_connection for improved connection handling ([ef880d4](https://github.com/rubiin/Tsumiki/commit/ef880d403eab0e44153c2cd13970e2222071389c))
* replace Image widget with Svg for weather icons ([f35c08f](https://github.com/rubiin/Tsumiki/commit/f35c08ff508dcfe2ce08aefdeeb8d7275dee1b1e))
* replace print statements with logger.exception for improved error handling across multiple modules ([52f79fd](https://github.com/rubiin/Tsumiki/commit/52f79fdbff7c064e4da4d82ade73cdfcce0acd0c))
* scale image when setting new size in CircularImage ([1aefc8a](https://github.com/rubiin/Tsumiki/commit/1aefc8a388b2ca3a6bb46d211c67c6c3b5db7545))
* **scripts:** use -Su for AUR helper in arch update (avoid forced DB refresh) ([608421f](https://github.com/rubiin/Tsumiki/commit/608421f0a17e09a8c3b799a4fc44e3b6def42577))
* **scripts:** use -Syu for AUR helper in arch update command (perform full system + AUR upgrade) ([777110c](https://github.com/rubiin/Tsumiki/commit/777110c79840cacbdb1ad206624c6ced075c7713))
* show Bluetooth paired devices in quick settings submenu ([#137](https://github.com/rubiin/Tsumiki/issues/137)) ([947895b](https://github.com/rubiin/Tsumiki/commit/947895b7a3682ca012fc5e491738cf9419cdead5))
* show Bluetooth paired devices in quick settings submenu ([#137](https://github.com/rubiin/Tsumiki/issues/137)) ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* show Bluetooth paired devices in quick settings submenu ([#137](https://github.com/rubiin/Tsumiki/issues/137)) ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* show Bluetooth paired devices in quick settings submenu ([#137](https://github.com/rubiin/Tsumiki/issues/137)) ([4c503ff](https://github.com/rubiin/Tsumiki/commit/4c503ff504bb4a18793810cbc16b8a8c814a5bab))
* simplify pinned apps initialization in AppBar by using a fallback for None ([7752fe5](https://github.com/rubiin/Tsumiki/commit/7752fe5179f84b96bca76ff4f8aec61580f9f2f9))
* simplify pixel size initialization in AudioSlider ([e4b250f](https://github.com/rubiin/Tsumiki/commit/e4b250f357e10c84bc034c3c8dc6ffb7e2177ac7))
* simplify singleton implementation in NetworkSpeed class ([e2b4f96](https://github.com/rubiin/Tsumiki/commit/e2b4f96ca73294cb0734ad7cb0ece0d3bbde33f5))
* streamline app ID handling in AppBar to manage ignored apps and tooltip visibility ([b44babe](https://github.com/rubiin/Tsumiki/commit/b44babe5c77e8cacc076c59728da6c0190b279cb))
* streamline app ID handling in AppBar to manage ignored apps and tooltip visibility ([ba00c1f](https://github.com/rubiin/Tsumiki/commit/ba00c1fcda6d497347d080f8525da87f3e723d40))
* streamline brightness update logic and enhance error handling in BrightnessService ([5fecc7e](https://github.com/rubiin/Tsumiki/commit/5fecc7e76b3ee2a36fd52d88934b0c5ca8654a29))
* streamline brightness update logic and enhance error handling in BrightnessService ([3fbb2fe](https://github.com/rubiin/Tsumiki/commit/3fbb2fefb6419ee23fe06f05455640e4cf5229fb))
* streamline brightness update logic and enhance error handling in BrightnessService ([8e71b8b](https://github.com/rubiin/Tsumiki/commit/8e71b8b7d1031d3b2551e2ee1bb1fa2085209dea))
* streamline brightness update logic and enhance error handling in BrightnessService ([3092df4](https://github.com/rubiin/Tsumiki/commit/3092df459846aaafe8eb2be13ad7b983c05da9cb))
* streamline enum formatting and required properties in schema ([d9956e3](https://github.com/rubiin/Tsumiki/commit/d9956e3392233d5ac7115ab782b0e567bdf6b42e))
* streamline muted style class handling in AudioOSDContainer ([a000141](https://github.com/rubiin/Tsumiki/commit/a000141903263b8f6efa00c108c331fed0da6408))
* streamline muted style class handling in AudioOSDContainer ([2e85ea9](https://github.com/rubiin/Tsumiki/commit/2e85ea9be334594f9919525a4b8d65b9ff466ba6))
* streamline ScanButton initialization for improved readability ([4b78376](https://github.com/rubiin/Tsumiki/commit/4b7837633a006b23ba12bbc27f0f689293d84ac6))
* streamline screen recording and screenshot methods by removing redundant path parameter ([94090c2](https://github.com/rubiin/Tsumiki/commit/94090c2634380ba03be3963886083aef3b185575))
* **system_tray:** track SystemTrayItem instances and properly remove them ([7c7eb1d](https://github.com/rubiin/Tsumiki/commit/7c7eb1d262d2a59e4b9dad6cdc7034ff8da54acf))
* toggle dialog popup after executing command in the dialog class ([1c806dd](https://github.com/rubiin/Tsumiki/commit/1c806dd3a94d320c5bc1e9f9211136d280a09a9b))
* truncate action button label to improve UI clarity ([9290a30](https://github.com/rubiin/Tsumiki/commit/9290a3005d8130dc08e05090c4951ea384c3347c))
* update address handling in AppBar and improve menu display logic ([18bbbfc](https://github.com/rubiin/Tsumiki/commit/18bbbfcc2dc42884fd3cc9fd6b67ebbc6dc1cac3))
* update AppWidgetFactory style to use style classes and adjust icon margin in common styles ([a575206](https://github.com/rubiin/Tsumiki/commit/a575206ff5d634282ea3c7b89b2c1b5a0206d104))
* update audio icon handling to streamline volume state representation on slider ([9363040](https://github.com/rubiin/Tsumiki/commit/93630404d1f223d518e3777853d5381a2e581ae7))
* update auto_hide option in updates widget to false and add pad_zero option ([5ea10eb](https://github.com/rubiin/Tsumiki/commit/5ea10ebb1f6d66191322717638085278464dc68f))
* update banner and tsumiki images ([8728071](https://github.com/rubiin/Tsumiki/commit/87280718ec12928cfffa95f1b776c4e8484e8aa3))
* update battery widget configuration ([a5551bf](https://github.com/rubiin/Tsumiki/commit/a5551bf9412c3a401de108bb2af43ef3c500258e))
* update battery widget to use correct time formatting function ([3fd830c](https://github.com/rubiin/Tsumiki/commit/3fd830cc90deb4cd05550a0391cc8698f87c4fb5))
* update border-radius for power control button and adjust hover border width ([bf17340](https://github.com/rubiin/Tsumiki/commit/bf17340d821ff05ec15dd83b374891a6168066cf))
* update box-shadow color mixing for hover effect in scrolledwindow ([bc9284b](https://github.com/rubiin/Tsumiki/commit/bc9284b2287473709026604bc09c65430c9bcd79))
* update box-shadow for power button menu and adjust focus styles for better visibility ([2dfc068](https://github.com/rubiin/Tsumiki/commit/2dfc068410b7d0128c50b1776aea73f8f5e3b7ab))
* update brightness slider to use screen brightness percentage ([c133174](https://github.com/rubiin/Tsumiki/commit/c1331749a1a600f124801201e57cd58cc30e5e23))
* update button styles in common and dock for improved UI consistency ([d010355](https://github.com/rubiin/Tsumiki/commit/d010355f31c0e30a697b8b03ae6af6fcee273796))
* update config access patterns to use get() for safer retrieval ([13ffd98](https://github.com/rubiin/Tsumiki/commit/13ffd98e2ffa479724b17e77c0a3cbfb8293a689))
* update connection handling in WindowCountWidget and MonitorWatcher classes ([e37f232](https://github.com/rubiin/Tsumiki/commit/e37f2329050afc532d0c03dd710981f5ffaf4bc6))
* update contributor contributions to include code and doc categories ([3131c32](https://github.com/rubiin/Tsumiki/commit/3131c32c124a88ea1c0ba9439bf2c682cbcf02ee))
* update contributor section to include code contributions for several contributors ([68f1f3e](https://github.com/rubiin/Tsumiki/commit/68f1f3ebe63556c0840b5d575f025f98a57b1f74))
* update CPU tooltip to handle unknown clock speeds and adjust GPU progress bar value ([41e9980](https://github.com/rubiin/Tsumiki/commit/41e99809630d187ac279f3278ae0102ad96dbdfb))
* update daemon kill command for improved clarity and accuracy ([1c5aee9](https://github.com/rubiin/Tsumiki/commit/1c5aee90801b63351fb1f1a84535943ae30b87e6))
* update default icon for custom button and clipboard history widgets ([d7fd76c](https://github.com/rubiin/Tsumiki/commit/d7fd76ca1f04c5eff15a34958e74deecdb422b17))
* update default workspace count to 10 and icon size to 40 ([6b6c420](https://github.com/rubiin/Tsumiki/commit/6b6c420c91ebf2c4e9347b27e6844fc64b32aa67))
* update default workspace count to 10 and icon size to 40 ([9ada758](https://github.com/rubiin/Tsumiki/commit/9ada7587acf4a8caacccff2f5af9c485a4c0ad6c))
* update dock opacity for improved visibility ([31d5381](https://github.com/rubiin/Tsumiki/commit/31d5381d49ec449aa50470d5786c863e65045cbd))
* update exempt-issue-labels to include enhancement and bug labels ([f130556](https://github.com/rubiin/Tsumiki/commit/f130556181cabdae7f715b7f52927ba69e4b81ac))
* update font size for date menu notification summary and body ([36d719d](https://github.com/rubiin/Tsumiki/commit/36d719d78f94e10c2fb422e33a44e40033942999))
* update GI version requirements across multiple modules ([cf9a70e](https://github.com/rubiin/Tsumiki/commit/cf9a70e700a0f35a967df8751a9b07ac5bffe0d4))
* update GI version requirements across multiple modules ([cddf0e3](https://github.com/rubiin/Tsumiki/commit/cddf0e3b3f88385057f00161088910af64ad1744))
* update json schema ([98684b7](https://github.com/rubiin/Tsumiki/commit/98684b7c9acd9daf2f25ad2b051ebe528c303734))
* update label padding logic to right-align total updates ([9387520](https://github.com/rubiin/Tsumiki/commit/9387520e05d03e042dbf84db3e7a006ef7d33eb9))
* update layout configuration by removing app_launcher_button from left_section and cleaning up middle_section ([45d1799](https://github.com/rubiin/Tsumiki/commit/45d1799d8170186eba16d9e6103ceb54d313e9b6))
* update layout sections and enhance weather widget day/night logic ([a4ca7c8](https://github.com/rubiin/Tsumiki/commit/a4ca7c8a0716e7e188d21bd6a3ff60d6f5ebf26b))
* update method name for finding desktop applications ([a59e96b](https://github.com/rubiin/Tsumiki/commit/a59e96b32ef4d7e6416750c2112f222291153da5))
* Update modules/osd.py ([9dd83f9](https://github.com/rubiin/Tsumiki/commit/9dd83f9f4d9bbdfc990f8d0a32944d30c311d057))
* update monitor data retrieval to use json parsing ([f1eba38](https://github.com/rubiin/Tsumiki/commit/f1eba38576a8b63348ec31c09782b823215c69c6))
* update notification image size for improved display in DateMenuNotification widget ([44028f4](https://github.com/rubiin/Tsumiki/commit/44028f44e9d4715148744acddf95303b43ced628))
* update panel button hover color for better visibility ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* update panel layout by rearranging middle section widgets  ([#134](https://github.com/rubiin/Tsumiki/issues/134)) ([947895b](https://github.com/rubiin/Tsumiki/commit/947895b7a3682ca012fc5e491738cf9419cdead5))
* update panel layout by rearranging middle section widgets  ([#134](https://github.com/rubiin/Tsumiki/issues/134)) ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* update panel layout by rearranging middle section widgets  ([#134](https://github.com/rubiin/Tsumiki/issues/134)) ([32c9fb2](https://github.com/rubiin/Tsumiki/commit/32c9fb23bf82838699bd9dfc52880a226dffffee))
* update panel layout by rearranging middle section widgets and adjusting widget group spacing ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* update permissions in release workflow to include issues ([7c2c753](https://github.com/rubiin/Tsumiki/commit/7c2c7533000c2f19cb6ddf42ddd69332d10e6fd7))
* update pinned apps handling and improve separator visibility logic ([902ee92](https://github.com/rubiin/Tsumiki/commit/902ee9253eb0a26458ef734246f6768d35773133))
* update power button menu structure and improve transition duration ([ea8109c](https://github.com/rubiin/Tsumiki/commit/ea8109c19ff8b993c9124b40c8b49fdd672ded0e))
* update power control button styles for improved focus and hover effects ([fcbd71d](https://github.com/rubiin/Tsumiki/commit/fcbd71d051faa9843f114ae0e6bae85cb02cfc68))
* update power profile setting to use the correct profile attribute ([c265fae](https://github.com/rubiin/Tsumiki/commit/c265faeb5103857a2ea74f25ea809177d0a629a3))
* update quotes configuration to disable and increase update interval ([9e73104](https://github.com/rubiin/Tsumiki/commit/9e7310456e8e2dcd6ad375c76d1844963610230e))
* update README with post-installation instructions for hyprland.conf ([69a5410](https://github.com/rubiin/Tsumiki/commit/69a541081923bf49cceb62259c82bdf2ae72f875))
* update reference for custom_button in schema to correct path ([6f7c4f3](https://github.com/rubiin/Tsumiki/commit/6f7c4f367a188ddc40f8d163766809607a669ff0))
* update release type to python in release workflow ([8a0873c](https://github.com/rubiin/Tsumiki/commit/8a0873cfa6be93c2e2a260fb1ea2290c0e86e461))
* update Renovate configuration to set range strategy and add labels ([da45d99](https://github.com/rubiin/Tsumiki/commit/da45d993c4ed8b7b8413443b054731a82e24ac33))
* update scale value and improve workspace label styling in overview ([60d5d86](https://github.com/rubiin/Tsumiki/commit/60d5d861a0169d385af6e52e2a22375ce32f6854))
* update schedule time to 2pm on Monday in renovate configuration ([b0f559a](https://github.com/rubiin/Tsumiki/commit/b0f559a7a7752642cce2b0b77db107b274170bae))
* update screenshots in README and add new notification images ([a04d00b](https://github.com/rubiin/Tsumiki/commit/a04d00b6c69995085c5d940ba81d0d552dd6a3fd))
* update screenshots in README and add new notification images ([7072d3b](https://github.com/rubiin/Tsumiki/commit/7072d3b7be8d5d9c18a3e49ca6b2993993969894))
* update set_active method to correctly manage active state styling ([#129](https://github.com/rubiin/Tsumiki/issues/129)) ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* update set_active method to correctly manage active state styling ([#129](https://github.com/rubiin/Tsumiki/issues/129)) ([528e2f2](https://github.com/rubiin/Tsumiki/commit/528e2f2b90facb7bac6e98366d04f177e4cbc290))
* update set_active method to correctly manage active state styling ([#129](https://github.com/rubiin/Tsumiki/issues/129)) ([dc0ce69](https://github.com/rubiin/Tsumiki/commit/dc0ce6935ab23bdea7e25791b02399f910891b73))
* update sound capture setting to false and enable hover reveal in weather widget ([864b9a8](https://github.com/rubiin/Tsumiki/commit/864b9a8d1ddd4da3a3c0554839c4ed9dab074f12))
* update stubs generation command to use fabric-cli instead of gengir ([95aa767](https://github.com/rubiin/Tsumiki/commit/95aa767ea1ebbb7058244828d5ca7fe65bfedc55))
* update style classes and layout properties in AppWidgetFactory and AppLauncher ([aca9be1](https://github.com/rubiin/Tsumiki/commit/aca9be14b361f024631a8ca7a48324a371eaa564))
* update submap handling to correctly process string input and fix command string ([1733028](https://github.com/rubiin/Tsumiki/commit/1733028fd1fd11d6206f5230c62f67fc513a1f79))
* update titles for various UI components to improve consistency ([42bfa45](https://github.com/rubiin/Tsumiki/commit/42bfa457da1ae2d822226d3c8cb5d7399ffd7dac))
* update Tsumiki image dimensions for better visibility ([1e0cbfd](https://github.com/rubiin/Tsumiki/commit/1e0cbfde1616e4e207a66493efeca770abc8f268))
* update user avatar path handling in QuickSettingsMenu ([#193](https://github.com/rubiin/Tsumiki/issues/193)) ([5556f03](https://github.com/rubiin/Tsumiki/commit/5556f0356066a0c8d862ac169fe4fa83e08799d6))
* update version retrieval method in start_bar function ([273a51b](https://github.com/rubiin/Tsumiki/commit/273a51b65b18253f60b7e3ace85207fa7b26b071))
* update version to 1.0.1 in pyproject.toml ([6ccb3b0](https://github.com/rubiin/Tsumiki/commit/6ccb3b0014398e1d2fd33cc844b93df6fea0b4b7))
* update version to 1.0.2 in pyproject.toml ([5c80bcd](https://github.com/rubiin/Tsumiki/commit/5c80bcdd190903cfd188d66eafdd5e147ceacf8f))
* update version to 1.0.2 in pyproject.toml ([b21b17a](https://github.com/rubiin/Tsumiki/commit/b21b17a78d681105f3850ab1f74e518b61485974))
* update visibility of revert and add dependency updates section ([cf13f2f](https://github.com/rubiin/Tsumiki/commit/cf13f2fd90536c4e96649ac12f987bffdded91d5))
* update volume handling in AudioOSDContainer to ignore missing signals ([2584404](https://github.com/rubiin/Tsumiki/commit/25844044812b1410b1ef9bc68d34656192aebab3))
* update volume handling in AudioOSDContainer to remove ignore_missing flag ([d86c49b](https://github.com/rubiin/Tsumiki/commit/d86c49b493637f029f5128dcdba0bd2df1d0ec93))
* update weather icon to use a specific icon character ([07a00f8](https://github.com/rubiin/Tsumiki/commit/07a00f8f5c6b1913489ad90e54a5f028e54fdd0c))
* update widget item type to reference definitions in schema ([cd6e034](https://github.com/rubiin/Tsumiki/commit/cd6e03446a0f8f112ff83747822e75d06ffe0ea0))
* update workspace count and icon size in configuration ([ff04bb8](https://github.com/rubiin/Tsumiki/commit/ff04bb88a0473c33444e0f19318a60b3707f43cd))
* update workspace count and icon size in configuration ([a204cd2](https://github.com/rubiin/Tsumiki/commit/a204cd25879beb8943dc309de839f13f91c097c8))
* use clear ([f46b48d](https://github.com/rubiin/Tsumiki/commit/f46b48d0b6dc928dc66e907882ae2a1b434e19d6))
* version ([fde84ce](https://github.com/rubiin/Tsumiki/commit/fde84cebc0bd3bad8fea640a48270d47c3fa51b0))
* WiFi Network List Filtering and Deduplication ([#142](https://github.com/rubiin/Tsumiki/issues/142)) ([e324a7f](https://github.com/rubiin/Tsumiki/commit/e324a7f21b9c8bf59a38195134cd860464c353e4))


### ⚡️ Performance Improvements

* simplify DND switch handling and improve notification removal logic ([58905ab](https://github.com/rubiin/Tsumiki/commit/58905abc9f3de7f2d249a4857bdf08a4ace470e1))


### 📚 Documentation

* add fdev31 as a contributor for bug ([#104](https://github.com/rubiin/Tsumiki/issues/104)) ([f911f03](https://github.com/rubiin/Tsumiki/commit/f911f03b0f4d4abe180c06e0473003faba542e77))
* add jhakonen as a contributor for bug ([#100](https://github.com/rubiin/Tsumiki/issues/100)) ([2880dea](https://github.com/rubiin/Tsumiki/commit/2880dea4830bbe6027c235f7a0c1b24c705ccd8b))
* add N1xev as a contributor for doc ([#192](https://github.com/rubiin/Tsumiki/issues/192)) ([07cf6fe](https://github.com/rubiin/Tsumiki/commit/07cf6fe842fd96cbf132d5b45bb803af479d625b))
* add sudo-Tiz as a contributor for bug ([#149](https://github.com/rubiin/Tsumiki/issues/149)) ([8197401](https://github.com/rubiin/Tsumiki/commit/819740170fb7c81972cd0a48a44e549edfe10387))
* update installation section to getting started and add troubleshooting information ([68ad175](https://github.com/rubiin/Tsumiki/commit/68ad175eebcd382a2dafd2957f518e588cc21814))
* update README ([#133](https://github.com/rubiin/Tsumiki/issues/133)) ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* update README ([#133](https://github.com/rubiin/Tsumiki/issues/133)) ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* update README ([#133](https://github.com/rubiin/Tsumiki/issues/133)) ([b07dd0f](https://github.com/rubiin/Tsumiki/commit/b07dd0fff737411f02645f6988ad45b54d5dda44))


### 🎨 Code Style

* format JSON files for consistent indentation ([ffcb90f](https://github.com/rubiin/Tsumiki/commit/ffcb90faa2182e8579f0c752b09098115894adb8))


### ⚙️ Chores

* add renovate configuration for grouping Python packages ([33b7289](https://github.com/rubiin/Tsumiki/commit/33b72890dd632069203e1b051c6662da6d2a5628))
* clean up config.json by removing unnecessary comments and unused options ([453e5d6](https://github.com/rubiin/Tsumiki/commit/453e5d6f69cdbbec2f5fb590ca49cd1adf291e26))
* DEFAULT_CONFIG in constants.py: remove unused options for layer, auto_hide, and location ([c273625](https://github.com/rubiin/Tsumiki/commit/c273625deba3d5a943e75af5a76a52110843492b))
* **deps:** update all non-major dependencies ([#178](https://github.com/rubiin/Tsumiki/issues/178)) ([a57942e](https://github.com/rubiin/Tsumiki/commit/a57942e3cba3774c4436a16577e4e3d5cb8fc7f0))
* **deps:** update all non-major dependencies ([#187](https://github.com/rubiin/Tsumiki/issues/187)) ([75ce690](https://github.com/rubiin/Tsumiki/commit/75ce690fe35f929c4da746745f66757c90950c6f))
* **deps:** update dependency pillow to v12 ([#227](https://github.com/rubiin/Tsumiki/issues/227)) ([3d21e5d](https://github.com/rubiin/Tsumiki/commit/3d21e5d6e80ade045f96314d568deaa304fa1f41))
* **deps:** update dependency psutil to v7 ([#179](https://github.com/rubiin/Tsumiki/issues/179)) ([794b87a](https://github.com/rubiin/Tsumiki/commit/794b87ae80806127b66fddd6e52d49cc8a95f66f))
* **deps:** update dependency rlottie-python to v1.3.8 ([#188](https://github.com/rubiin/Tsumiki/issues/188)) ([51a826e](https://github.com/rubiin/Tsumiki/commit/51a826e48a4f1257d662cac5186045653fd7e57f))
* **master:** release 1.3.0 ([#153](https://github.com/rubiin/Tsumiki/issues/153)) ([2a28e5e](https://github.com/rubiin/Tsumiki/commit/2a28e5e3717355e86edc4a28ea1329b5fe233465))
* **master:** release 1.4.0 ([#155](https://github.com/rubiin/Tsumiki/issues/155)) ([80116b3](https://github.com/rubiin/Tsumiki/commit/80116b30c9d253610abc0f6e321a295292aa3452))
* **master:** release 2.0.0 ([#158](https://github.com/rubiin/Tsumiki/issues/158)) ([69eeb90](https://github.com/rubiin/Tsumiki/commit/69eeb90d5b1fef366a5c2dc95a421bb737de1bf5))
* **master:** release 2.0.1 ([#161](https://github.com/rubiin/Tsumiki/issues/161)) ([4f2068e](https://github.com/rubiin/Tsumiki/commit/4f2068e162a63aae5bb1c1ddbef2537f8c20ba1b))
* **master:** release 2.0.2 ([#162](https://github.com/rubiin/Tsumiki/issues/162)) ([aebfd09](https://github.com/rubiin/Tsumiki/commit/aebfd092f5cbf8d9b323d1620f321a549a10209c))
* **master:** release 2.1.0 ([#183](https://github.com/rubiin/Tsumiki/issues/183)) ([069fcfd](https://github.com/rubiin/Tsumiki/commit/069fcfda88ca4222a94ddcd44b52731694d8bab4))
* **master:** release 2.2.0 ([#190](https://github.com/rubiin/Tsumiki/issues/190)) ([7bd1f1c](https://github.com/rubiin/Tsumiki/commit/7bd1f1cbc2a5b27f650c69e5a327de2190af7eed))
* **master:** release 2.3.0 ([#194](https://github.com/rubiin/Tsumiki/issues/194)) ([1a42802](https://github.com/rubiin/Tsumiki/commit/1a42802cd14e0f131d3b011d01ffb08238115a0b))
* **master:** release 2.4.0 ([#200](https://github.com/rubiin/Tsumiki/issues/200)) ([75c77fb](https://github.com/rubiin/Tsumiki/commit/75c77fb27013f7813c12c509cf52edfee9de5ec2))
* **master:** release 2.4.1 ([#203](https://github.com/rubiin/Tsumiki/issues/203)) ([3cf3e53](https://github.com/rubiin/Tsumiki/commit/3cf3e53af688d5adb4b96473521bf7051c9403e6))
* **master:** release 2.5.0 ([#204](https://github.com/rubiin/Tsumiki/issues/204)) ([e5f0ebe](https://github.com/rubiin/Tsumiki/commit/e5f0ebef8bd2c62c2c1b925a2da280a0b536f8e5))
* move release-please configuration files to .github ([67cd0f1](https://github.com/rubiin/Tsumiki/commit/67cd0f1cd9a64a1918576966c59409adba71e65c))
* release 2.5.0 ([f1bab66](https://github.com/rubiin/Tsumiki/commit/f1bab66fa9cf99f14e58db7a613f95708ff1a9db))
* remove author and license comments from swipingbutton.py ([84edba0](https://github.com/rubiin/Tsumiki/commit/84edba07251354605961dd0909cac26f31cb5c06))
* streamline enum and required fields in tsumiki.schema.json ([4bf3e7d](https://github.com/rubiin/Tsumiki/commit/4bf3e7d4889ee8929f16e560cfe2445b75adfeb5))
* update click and psutil versions in requirements.txt ([019e40a](https://github.com/rubiin/Tsumiki/commit/019e40a949c6251f0893779020150b6c94862575))
* update fabric ([38dc718](https://github.com/rubiin/Tsumiki/commit/38dc7186fe78f26713f6d5f759c7665395a81dff))
* update fabric ([47ea0c9](https://github.com/rubiin/Tsumiki/commit/47ea0c9abe82877a0b75be063512e487e41fa4e8))
* update Python version to 3.13.5, improve contribution guidelines, and enhance project metadata ([466774f](https://github.com/rubiin/Tsumiki/commit/466774f33fb2ea30ee67c9b5ffd0ca8e6bb5113a))


### ♻️ Code Refactoring

* add active style class to button widgets and manage popover state ([3cc603a](https://github.com/rubiin/Tsumiki/commit/3cc603a6263644463dbf938b61e553d745771c28))
* add anchor property to Dock initialization for improved positioning ([1213a09](https://github.com/rubiin/Tsumiki/commit/1213a0945d9cdbd331c019eb107387cf1013ce5e))
* add separator only if pinned exists ([409b295](https://github.com/rubiin/Tsumiki/commit/409b295c3f58c16566530f2614347a842a290920))
* add type hints for better code clarity and maintainability ([ba2e38e](https://github.com/rubiin/Tsumiki/commit/ba2e38ec0ac4240fd465bd8a952a7d42384c5c75))
* add type hints to function signatures for improved clarity ([94699e3](https://github.com/rubiin/Tsumiki/commit/94699e3c5dfa7970a65e83ca3bb72d727cb5d584))
* adjust thumbnail size and cropping method in ImageButton; update column size in WallpaperPickerBox ([f8c7e2f](https://github.com/rubiin/Tsumiki/commit/f8c7e2fae46177e2dd692f13fe7d11d5749a51ff))
* **animator:** consolidate bezier helpers into shared.animator and update Animator internals ([534f959](https://github.com/rubiin/Tsumiki/commit/534f959f868ac9133830a2409fc21e516800f7a7))
* change thread function to submit tasks to a thread pool instead of creating new threads ([97bf0c9](https://github.com/rubiin/Tsumiki/commit/97bf0c98954310b8dd85785e84d33d3928b71397))
* clean up app launcher styles and remove unused focus styles ([b46fc61](https://github.com/rubiin/Tsumiki/commit/b46fc61bb4432460a10e598ad6639cfce92fbd44))
* clean up imports and remove unnecessary whitespace in button and power profile modules ([947895b](https://github.com/rubiin/Tsumiki/commit/947895b7a3682ca012fc5e491738cf9419cdead5))
* clean up imports and remove unnecessary whitespace in button and power profile modules ([947895b](https://github.com/rubiin/Tsumiki/commit/947895b7a3682ca012fc5e491738cf9419cdead5))
* clean up imports and remove unnecessary whitespace in button and power profile modules ([947895b](https://github.com/rubiin/Tsumiki/commit/947895b7a3682ca012fc5e491738cf9419cdead5))
* clean up imports and remove unnecessary whitespace in button and power profile modules ([947895b](https://github.com/rubiin/Tsumiki/commit/947895b7a3682ca012fc5e491738cf9419cdead5))
* clean up imports and remove unnecessary whitespace in button and power profile modules ([947895b](https://github.com/rubiin/Tsumiki/commit/947895b7a3682ca012fc5e491738cf9419cdead5))
* clean up imports and remove unnecessary whitespace in button and power profile modules ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* clean up imports and remove unnecessary whitespace in button and power profile modules ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* clean up imports and remove unnecessary whitespace in button and power profile modules ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* clean up imports and remove unnecessary whitespace in button and power profile modules ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* clean up imports and remove unnecessary whitespace in button and power profile modules ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* clean up imports and remove unnecessary whitespace in button and power profile modules ([a0282f0](https://github.com/rubiin/Tsumiki/commit/a0282f0996c96120b2bd878dbeac27fccfcf8ab3))
* clean up wallpaper module by removing user-specific paths and simplifying thumbnail generation ([947895b](https://github.com/rubiin/Tsumiki/commit/947895b7a3682ca012fc5e491738cf9419cdead5))
* clean up wallpaper module by removing user-specific paths and simplifying thumbnail generation ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* clean up wallpaper module by removing user-specific paths and simplifying thumbnail generation ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* **collapsible:** lazy-import Popover and clear active state; remove panel margin ([c4e1139](https://github.com/rubiin/Tsumiki/commit/c4e1139a3ef027eef85c3923de311de2c69acdc7))
* **collapsible:** tidy popup.connect indentation and reorganize collapsible_group SCSS; use #collapsible_group nesting for active/hover rules and clean up whitespace ([cf83aae](https://github.com/rubiin/Tsumiki/commit/cf83aaeebd67f00f465be153454ca6972986bf0a))
* consolidate application retrieval into AppUtils for improved maintainability ([fcb2a4f](https://github.com/rubiin/Tsumiki/commit/fcb2a4faa0f75aa3386741fbdf170942708375d7))
* **core:** streamline services and utilities, replace loguru with fabric logger ([#223](https://github.com/rubiin/Tsumiki/issues/223)) ([eba8c3b](https://github.com/rubiin/Tsumiki/commit/eba8c3bb9bcef016a841c1eab46c9a4bbad16887))
* disable annotation for screenshot widget and remove location property from general settings ([b6df5df](https://github.com/rubiin/Tsumiki/commit/b6df5df6321982b0aee68e35aa7cbdc14e275f00))
* **dock:** use CenterBox to center revealer and add side spacers for larger hover area ([7d1b06f](https://github.com/rubiin/Tsumiki/commit/7d1b06f8484e967b622b02db209201c26a21b83d))
* eliminate nested functions for improved readability ([88d346c](https://github.com/rubiin/Tsumiki/commit/88d346c7686d3e26d2c450b2ca2923846a7d9cbb))
* enhance Arch-based distro check and improve Python detection logic ([a046798](https://github.com/rubiin/Tsumiki/commit/a046798c9622000cb1d3b64b0aa8f466f3d791d0))
* enhance logging messages with emojis for better user feedback ([4572961](https://github.com/rubiin/Tsumiki/commit/457296169014bd8aa853b73be1f7b45de9b5263c))
* enhance tooltip construction for update functions in systemupdates.sh ([62cb3be](https://github.com/rubiin/Tsumiki/commit/62cb3be111ee46bc154ec694cb3cd97ef497ca8e))
* expand Arch-based distro check to include additional distributions ([f5defcd](https://github.com/rubiin/Tsumiki/commit/f5defcd74cdc5138d2067b4457a03a1843ffc480))
* goodbye gray ([042c17b](https://github.com/rubiin/Tsumiki/commit/042c17bfda8b325a8ee8bffe8368288582951caa))
* improve dialog and power menu popup initialization and transition handling ([14dd13a](https://github.com/rubiin/Tsumiki/commit/14dd13a011a8af81a8c3ec32f139365746447bd7))
* initialize menu as None and create it on demand in show_menu method ([f532a04](https://github.com/rubiin/Tsumiki/commit/f532a046d0f69fa0f7cc5aba376e463504ad10e1))
* **logging:** enhance logging control by adding config option for disabling logs in non-debug mode ([#224](https://github.com/rubiin/Tsumiki/issues/224)) ([f3c4acf](https://github.com/rubiin/Tsumiki/commit/f3c4acfab3afae2957b5e510fb85d348caa73ea0))
* manage pinned apps with a dedicated separator and cleanup logic ([89430aa](https://github.com/rubiin/Tsumiki/commit/89430aa1ff5275e69b3846b961db3f45a1a1e09f))
* move Animator import statements inside relevant methods for better encapsulation ([a164c2c](https://github.com/rubiin/Tsumiki/commit/a164c2c254df6a496349d00115aec463f208ba38))
* move CollapsibleGroupWidget and CustomButtonWidget to shared module for better organization ([9d19744](https://github.com/rubiin/Tsumiki/commit/9d1974407048af3c6e7355313c254f8b6505f736))
* move hover logic to base class ([a64f041](https://github.com/rubiin/Tsumiki/commit/a64f04174586ddc60c813e47b977410e6105ebcb))
* move Hyprland connection initialization into class constructors ([dbfede0](https://github.com/rubiin/Tsumiki/commit/dbfede02498eae0700f9f037497cdd7ef4231893))
* move imports for AppLauncher and widget_config into the _get_or_create_launcher method ([2a43900](https://github.com/rubiin/Tsumiki/commit/2a43900579438be3934498f4f3afaa776ea89f19))
* move NetworkManager import and exception handling to the top of the file ([181c4fc](https://github.com/rubiin/Tsumiki/commit/181c4fc098bb4fcd02d532fdbf1109a53c33d425))
* move Popover import statements inside show_popover methods for better encapsulation ([d1fd8cf](https://github.com/rubiin/Tsumiki/commit/d1fd8cf8a212ccabbbebe55956b727e051833b44))
* pass popup parameter to QuickSettingsButtonBox and related toggles ([#220](https://github.com/rubiin/Tsumiki/issues/220)) ([f37cf91](https://github.com/rubiin/Tsumiki/commit/f37cf91fdce09d6934626df66cc83c46f6a6ddbf))
* remove anchor property from dock configuration and schema ([f955c09](https://github.com/rubiin/Tsumiki/commit/f955c094a9c26808d8154dbb703760450ac0250a))
* remove ignored_apps configuration from AppLauncher and related schema ([384d904](https://github.com/rubiin/Tsumiki/commit/384d9048bf27f0640fd619bbdf6910fb34abd981))
* remove Popover class implementation from popv1.py ([6b12541](https://github.com/rubiin/Tsumiki/commit/6b125417d0449105cd38edef5c6a1cba4b91fc47))
* remove pyjson5 dependency, and json5 ([f74c95f](https://github.com/rubiin/Tsumiki/commit/f74c95f5a31e60c5388fd46ad7c9fb38fa9d9327))
* remove redundant docstring from BaseWidget class ([a1a3f1c](https://github.com/rubiin/Tsumiki/commit/a1a3f1c33f450b0b44ae84543405d0535d8965a0))
* remove redundant initialization of Glace.Manager in TaskBarWidget ([0ba59fc](https://github.com/rubiin/Tsumiki/commit/0ba59fc441ce6961647e05a3bcfbb7581a646eb1))
* remove redundant set_has_class method from HoverButton and update CommandSwitcher to directly manage active state ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* remove redundant set_has_class method from HoverButton and update CommandSwitcher to directly manage active state ([df805b9](https://github.com/rubiin/Tsumiki/commit/df805b95247d3fbf407e0c9b7ddf024c3560c745))
* remove unused Gtk.IconTheme initialization in TaskBarWidget ([ef09d3c](https://github.com/rubiin/Tsumiki/commit/ef09d3ca88963996ea068c04163686723eb2e211))
* remove unused layout and general properties from schema ([bd745aa](https://github.com/rubiin/Tsumiki/commit/bd745aaedd99693ee7ceef22b2322fc22010c9b2))
* rename get_hyprland_connection variable for clarity and consistency ([1b8afc4](https://github.com/rubiin/Tsumiki/commit/1b8afc4ab00826e66178f0721a9d193b001efe1b))
* rename load_more_items to _load_next_batch for consistency ([cd5e87c](https://github.com/rubiin/Tsumiki/commit/cd5e87cbe30ed7927a0f5f912d8fa70e73f31b25))
* rename methods for consistency by prefixing with an underscore for private ([53589f4](https://github.com/rubiin/Tsumiki/commit/53589f42f5218166261bc6591605f2c6e9efee8f))
* rename PopupWindow to PopOverWindow for consistency ([5cfd028](https://github.com/rubiin/Tsumiki/commit/5cfd028e10733b5e11619ddda877e3caa6acd828))
* rename private methods to public in various modules for consistency ([dcd57d8](https://github.com/rubiin/Tsumiki/commit/dcd57d894bffaceae0030443ce4417c6b49b8d52))
* reorganize TypedDict definitions and add missing fields for consistency ([b001ed2](https://github.com/rubiin/Tsumiki/commit/b001ed2f8fcd94ebd853ef261fed775cef3c42e7))
* replace 'box' with 'container_box' in widget classes for consistency ([53aece5](https://github.com/rubiin/Tsumiki/commit/53aece5a9450261609a40676ad925488b58f66f5))
* replace APP_CACHE_DIRECTORY with APP_DATA_DIRECTORY for consistency across modules ([2df7044](https://github.com/rubiin/Tsumiki/commit/2df704429df57f59d2ad8713e748457dafc235dc))
* replace exec_shell_command_async with hyprland_connection methods in various widgets ([a27e00e](https://github.com/rubiin/Tsumiki/commit/a27e00ec1b525a393b764f43db0955c63e2f0dd4))
* replace get_relative_path with ASSETS_DIR for asset path management ([8da0623](https://github.com/rubiin/Tsumiki/commit/8da0623637e5a3c847b8d1754b7fc773ddfef3b3))
* replace GLib.source_remove with remove_handler for consistency ([2967706](https://github.com/rubiin/Tsumiki/commit/2967706555630487f3eb913b5a6ad07ce5762bc9))
* replace hardcoded username with dynamic home directory for wallpaper paths ([947895b](https://github.com/rubiin/Tsumiki/commit/947895b7a3682ca012fc5e491738cf9419cdead5))
* replace hardcoded username with dynamic home directory for wallpaper paths ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* replace hardcoded username with dynamic home directory for wallpaper paths ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* replace Hyprland connection initialization and improve icon resolution handling ([16b0f66](https://github.com/rubiin/Tsumiki/commit/16b0f66bcd735e46565fe479d14cce62007f53c3))
* replace json file handling with utility function for improved error handling ([4346325](https://github.com/rubiin/Tsumiki/commit/4346325520b18d752b227e1cf2c47be50b342ba4))
* replace json file handling with utility function for improved error handling ([6452c45](https://github.com/rubiin/Tsumiki/commit/6452c45fa9cc686122082e03bc4d17f606fbc331))
* replace List with built-in list for type hints consistency ([639b9c8](https://github.com/rubiin/Tsumiki/commit/639b9c8d2a477e67e8da1b233479087fc335a211))
* replace read_json_file with load_json and update related function names for consistency ([3ff23dd](https://github.com/rubiin/Tsumiki/commit/3ff23dd3f94368fc5d3c51fde92f051738f910e4))
* replace reusable_fabricator with invoke_repeater for period… ([#218](https://github.com/rubiin/Tsumiki/issues/218)) ([2c9ba20](https://github.com/rubiin/Tsumiki/commit/2c9ba20c1d84e8d9a305e5e948413e05415e8654))
* replace set_has_class with toggle_css_class for consistency in widget state management ([7ae0bed](https://github.com/rubiin/Tsumiki/commit/7ae0beded1e6162b8483dc9fbbe64dfacecf73d4))
* replace set_reveal_child with reveal/unreveal methods in various modules for consistency ([67975c0](https://github.com/rubiin/Tsumiki/commit/67975c06483a737c3569cdc77c594a8422302675))
* simplify icon handling by integrating IconResolver and removing redundant methods ([57d8ea1](https://github.com/rubiin/Tsumiki/commit/57d8ea1920fdc9cc12e0701c213aac9ad10bb030))
* simplify menu item handling in AppBar and consolidate pinning logic ([7991887](https://github.com/rubiin/Tsumiki/commit/79918875b8bc49b7b0acfbbcbace98db88644d11))
* simplify TaskBarWidget by removing Hyprland integration and unused code ([cd3fb36](https://github.com/rubiin/Tsumiki/commit/cd3fb36a265997e5ac6e961021da396117cc65ed))
* simplify window management in main application initialization ([947895b](https://github.com/rubiin/Tsumiki/commit/947895b7a3682ca012fc5e491738cf9419cdead5))
* simplify window management in main application initialization ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* simplify window management in main application initialization ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* streamline animation setup in AnimatedCircularProgressBar ([a4e2c3e](https://github.com/rubiin/Tsumiki/commit/a4e2c3ef0fb7903c4edd0b616a7e1f2ff0898735))
* streamline application initialization and status bar creation ([947895b](https://github.com/rubiin/Tsumiki/commit/947895b7a3682ca012fc5e491738cf9419cdead5))
* streamline application initialization and status bar creation ([947895b](https://github.com/rubiin/Tsumiki/commit/947895b7a3682ca012fc5e491738cf9419cdead5))
* streamline application initialization and status bar creation ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* streamline application initialization and status bar creation ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* streamline enum and required properties formatting in schema ([a6d6bad](https://github.com/rubiin/Tsumiki/commit/a6d6baddda553cfdd3e641af945f254ce8a7b427))
* streamline enum and required properties formatting in schema ([606a516](https://github.com/rubiin/Tsumiki/commit/606a516b016260f74a3f1a152ddd27a1b122a95f))
* streamline menu item creation and management in AppBar ([503bb2c](https://github.com/rubiin/Tsumiki/commit/503bb2c64d49ce6abce95bc039de9bd8e87ef924))
* streamline StatusBar bar recreation logic and remove unused process name setting ([2e23419](https://github.com/rubiin/Tsumiki/commit/2e23419cbf42f9e68a997b0ee4a1dd26b68fc851))
* streamline WiFi network handling and improve connection managemen ([#136](https://github.com/rubiin/Tsumiki/issues/136)) ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* streamline WiFi network handling and improve connection managemen ([#136](https://github.com/rubiin/Tsumiki/issues/136)) ([fbdf046](https://github.com/rubiin/Tsumiki/commit/fbdf0469cae5cfcbd09200ef66285533304aca08))
* streamline WiFi network handling and improve connection managemen ([#136](https://github.com/rubiin/Tsumiki/issues/136)) ([28f7131](https://github.com/rubiin/Tsumiki/commit/28f7131fb8e0e0b160dc639199b993b123e41c8e))
* streamline workspace button setup and state management in WorkSpacesWidget ([3027096](https://github.com/rubiin/Tsumiki/commit/30270966874176901dcfec731548e09f13da6a7f))
* streamline workspace handling in Dock and WindowCountWidget ([e4aea5f](https://github.com/rubiin/Tsumiki/commit/e4aea5f19dc6922c31dea367196801d4a7444a91))
* **styles:** centralize popover styling and enable popover shadow; update popovers and clean up duplicated includes ([24db1ec](https://github.com/rubiin/Tsumiki/commit/24db1ec86eefe576d090f1d05f05deeac3e97933))
* **styles:** reduce bar menus popover padding to 0.5em / 0.2em ([5207892](https://github.com/rubiin/Tsumiki/commit/52078929fcb24a73a1bd3449a32a0e031ec4bf8c))
* **styles:** remove blur/spread and set full opacity for bar menus popover shadow ([92e32f9](https://github.com/rubiin/Tsumiki/commit/92e32f966b4c3532cba37c8ad1366a475d710fb5))
* **styles:** set quick_settings slider height to 7px and enable slider in theme & settings ([8c1c570](https://github.com/rubiin/Tsumiki/commit/8c1c57009380b929662ab226179d1faa43db30d3))
* **system_tray:** extract BaseSystemTray and use SystemTray service ([b441bc4](https://github.com/rubiin/Tsumiki/commit/b441bc44b1efb410e2a8c1a3a2e8f7bf3966d052))
* **ui:** add icon padding, use HoverButton for power profiles, and tidy whitespace ([504c8ce](https://github.com/rubiin/Tsumiki/commit/504c8ce0d8b2cc6cd21ef726d910eae3650ade53))
* **ui:** set pointer cursor on ButtonWidget state change and remove stray blank line in window_title ([094bf91](https://github.com/rubiin/Tsumiki/commit/094bf911161f5734fa6c579430b4413be6e67508))
* unified widget resolver system ([84d7d94](https://github.com/rubiin/Tsumiki/commit/84d7d948569e2c5a1d7090a4dcfa806661c23b0f))
* update AppUtils to use properties for applications and identifiers, enhancing encapsulation ([bc54d4a](https://github.com/rubiin/Tsumiki/commit/bc54d4a269ce8021d55aa6da373d2b3cc8ea2232))
* update client added handling in AppBar for improved clarity and functionality ([09d34b9](https://github.com/rubiin/Tsumiki/commit/09d34b9cc962e7b904c719349cec9de917fa7f5c))
* update configuration documentation and remove unused fields from constants ([561304d](https://github.com/rubiin/Tsumiki/commit/561304d465e2063823218c01fac112f20086cea4))
* update constructor signatures to use dict type hints for config ([4d11c84](https://github.com/rubiin/Tsumiki/commit/4d11c844f78e3bd6635ff0158f825904f538040f))
* update LauncherConfig to use BarConfig type hint in app_launcher.py ([62cb3be](https://github.com/rubiin/Tsumiki/commit/62cb3be111ee46bc154ec694cb3cd97ef497ca8e))
* update OSDContainer to use BarConfig type hint in osd.py ([62cb3be](https://github.com/rubiin/Tsumiki/commit/62cb3be111ee46bc154ec694cb3cd97ef497ca8e))
* update Python checks and fix PyGObject version in requirements ([6802725](https://github.com/rubiin/Tsumiki/commit/6802725a449e9d09a20e5cd81dfa4a6386cedb9f))
* update style_classes to use list format for consistency across widgets ([9f76ff5](https://github.com/rubiin/Tsumiki/commit/9f76ff52de88a6a745c68476207b4b01d931a6d6))
* update thumbnail generation to use PIL and run in thread pool ([466becc](https://github.com/rubiin/Tsumiki/commit/466becc0835c0cdf32980694026f0019aa1ab8a0))
* update widget type hints for improved clarity and consistency ([13ce89d](https://github.com/rubiin/Tsumiki/commit/13ce89d0a3f79ad55159692a9ea2dd12e66b4ee5))
* update Widget_Groups definition to use a list of TypedDict for improved structure ([1925e57](https://github.com/rubiin/Tsumiki/commit/1925e57f40e5f8751e6768be575a40955b893ab2))


### 🚀 CI Improvements

* add GitHub Actions workflow to auto-update Wiki from doc.md on push ([e641c10](https://github.com/rubiin/Tsumiki/commit/e641c104ad73bd710c7a67fc3e5cacca26544bbb))
* Update and rename changelog.yml to release.yml ([aa19c3a](https://github.com/rubiin/Tsumiki/commit/aa19c3a0278a14e2fa7ab0000825a88cfb78de03))
* Update checkout action version from v5 to v4 ([d66a6ee](https://github.com/rubiin/Tsumiki/commit/d66a6ee7d5e06a21903f332df2c61e9ad84212ad))
* update release please ([3ef4d9c](https://github.com/rubiin/Tsumiki/commit/3ef4d9cc6e4a7f67d2ef223e1fe23a65ee49d8bb))

## [2.5.0](https://github.com/rubiin/Tsumiki/compare/v2.4.1...v2.5.0) (2025-10-30)


### ⚠ BREAKING CHANGES

* power profile

### 🚀 New Features

* add behavior configuration for dock widget and update related settings ([59a4bf4](https://github.com/rubiin/Tsumiki/commit/59a4bf4d7412ca93f6c4e9cd88d5d6cce4dfd3f9))
* add ClippingBox and LimitBox classes for enhanced widget functionality ([f38b06e](https://github.com/rubiin/Tsumiki/commit/f38b06e4d2855d1ae839f206109e86c548cf0c56))
* add desktop quotes and activate Linux widgets with configuration options ([2ec78f1](https://github.com/rubiin/Tsumiki/commit/2ec78f19aadcc58cec58e602385f2a8328f7018f))
* add desktop quotes configuration and update activate Linux settings ([154e05e](https://github.com/rubiin/Tsumiki/commit/154e05edfc33ca701841703b637ba38b7d0dfc5c))
* add fallback option for window title configuration and logging ([9cd0a9b](https://github.com/rubiin/Tsumiki/commit/9cd0a9b9f7c752865d5791ad4b38b5f717391ddb))
* add force reinstall option to init.sh for updating python dependencies ([#208](https://github.com/rubiin/Tsumiki/issues/208)) ([9faa47a](https://github.com/rubiin/Tsumiki/commit/9faa47ad125a628e1bc2b5c121db60003b0b4102))
* add show_numbered option for workspaces configuration and widget display ([2186064](https://github.com/rubiin/Tsumiki/commit/2186064322f355492e350a3a4c109865ac851d1f))
* establish Hyprland connection in HyprSunsetSubMenu for dynamic command execution ([62cb3be](https://github.com/rubiin/Tsumiki/commit/62cb3be111ee46bc154ec694cb3cd97ef497ca8e))
* implement overview button widget and related configuration ([cf1b547](https://github.com/rubiin/Tsumiki/commit/cf1b54706f3b5ac0615fe4ebf2a8cbf677ba7d8c))
* implement overview button widget and update configuration for overview functionality ([1c48dc1](https://github.com/rubiin/Tsumiki/commit/1c48dc1ba7bfa036916f9340ea306b555156d5d4))
* **utils:** add Matugen palette generator ([79beab2](https://github.com/rubiin/Tsumiki/commit/79beab26086f89ff0210de6f0fbcc11ca1fab7e6))


### 🐛 Bug Fixes

* :Modified power button styles in power.scss to adjust padding and label font size. ([eb7c647](https://github.com/rubiin/Tsumiki/commit/eb7c647da4cfb129153bbdcb6fde09a5bda5805c))
* add Custom_Button_Group and Collapsible_Group TypedDicts for enhanced widget configuration ([0b4f82c](https://github.com/rubiin/Tsumiki/commit/0b4f82cf2d26c55d8228221782f15935fb005949))
* add delay before starting Tsumiki ([729ed95](https://github.com/rubiin/Tsumiki/commit/729ed95b775a0335c4b0f18cd27f68e3d9ac1171))
* add file monitoring for CSS changes and improve debug logging condition ([2940a7c](https://github.com/rubiin/Tsumiki/commit/2940a7c8ffe689291e8a49e1a2ad060616a86e34))
* add icon to uptime ([#219](https://github.com/rubiin/Tsumiki/issues/219)) ([1217566](https://github.com/rubiin/Tsumiki/commit/1217566600ef7080d29e96c8a93fcd8834b25300))
* add mappings option to window_title widget and disable monitor_styles in general settings ([23b9da1](https://github.com/rubiin/Tsumiki/commit/23b9da1e7db6552f82e9b9dc2d79cb29edf95cae))
* add missing newlines and improve SVG structure for consistency across icon files ([8f09e47](https://github.com/rubiin/Tsumiki/commit/8f09e472f1289d6ab1461931bd629a01772f21a4))
* add more operations on doc menu ([19444bd](https://github.com/rubiin/Tsumiki/commit/19444bd502df65fd8b88811de20df881d96015aa))
* add name parameter to PopupWindow for better identification in PowerMenuPopup ([1395e48](https://github.com/rubiin/Tsumiki/commit/1395e48414f4401912b45d84d23d24541bebe9ac))
* add type hint for config attribute in ButtonWidget class ([afcab11](https://github.com/rubiin/Tsumiki/commit/afcab11cf099a8b4602ef8aa49e46ac7923cbb1c))
* add type hint for config parameter in PowerMenuPopup constructor ([e03e5b4](https://github.com/rubiin/Tsumiki/commit/e03e5b4c03fae720decd9b975acd86a2d20c1063))
* add type hints for config parameter in multiple widget constructors ([61f51a4](https://github.com/rubiin/Tsumiki/commit/61f51a41159725a62247b2dc786ebb1f1010b1b5))
* adjust bluetooth icon size and update chevron icon styling ([6e9f754](https://github.com/rubiin/Tsumiki/commit/6e9f75400623aba4947496bb3209c92866f2d6c0))
* adjust margin for activate_linux box in widgets styles ([b157e2c](https://github.com/rubiin/Tsumiki/commit/b157e2cd47e3686966666d663bc182fa899ac002))
* adjust max character width for notification widget and enhance opacity in media styles for better visibility ([69a36a9](https://github.com/rubiin/Tsumiki/commit/69a36a9ba12b6291661ceba31da0adf4e403d3d7))
* align close button to the start in notification and datetime menu widgets ([c563f67](https://github.com/rubiin/Tsumiki/commit/c563f6795dacadcdd784149891628f126630b12f))
* allow customizable size for DotIndicator and simplify app launcher toggle logic ([465e0ed](https://github.com/rubiin/Tsumiki/commit/465e0ed5654c71b8feb803c175b8be40ab0e18be))
* center align close button in notification and datetime menu widgets ([50402a2](https://github.com/rubiin/Tsumiki/commit/50402a2be02c54fc5c863d47ba0cd4ce190a86ec))
* center align close button in NotificationWidget overlay ([025d4df](https://github.com/rubiin/Tsumiki/commit/025d4df2c72a5af7fbc8b2250c327512781d3e8e))
* change desktop clock label color to white for better visibility ([1f91ee5](https://github.com/rubiin/Tsumiki/commit/1f91ee59b72144e6fb346414cf6e16b27b643642))
* correct method signature for on_shuffle_update in PlayerBox ([1932704](https://github.com/rubiin/Tsumiki/commit/193270433c5c41d4161541fe54952c345695095a))
* correct typo in config attribute access in WindowTitleWidget class ([c232920](https://github.com/rubiin/Tsumiki/commit/c232920f5e5d2a484e47e7a86eca733c98ad4fac))
* disable desktop clock and add configuration for desktop quotes ([81d9ffd](https://github.com/rubiin/Tsumiki/commit/81d9ffde8e71c64d04c22262c4525ea444b31eb7))
* disable overview widget by default ([1d8c346](https://github.com/rubiin/Tsumiki/commit/1d8c34682f6cb3ae5d4619721a9484ca6a56323b))
* don't use get_relative_path multiple times if you can freaking avoid it ([690b39a](https://github.com/rubiin/Tsumiki/commit/690b39a80badd79113925bd79f4c462584fa39e0))
* enhance JSON handling and error logging in various widgets ([2b821be](https://github.com/rubiin/Tsumiki/commit/2b821be6f43c72a5aabba55a54aa303a0840880e))
* enhance notification and app widget text wrapping and character limits for improved readability ([fbac91e](https://github.com/rubiin/Tsumiki/commit/fbac91e2535ae64e99c3323194ddd50ae81cccf1))
* enhance notification box hover effect with transition and background color ([322d4cb](https://github.com/rubiin/Tsumiki/commit/322d4cb21c4a048c1769acef7c47e0049b871a76))
* enhance workspace movement functionality by converting client address to hex format ([b1e82a6](https://github.com/rubiin/Tsumiki/commit/b1e82a6be601f86b951fdd1c798868d756be6450))
* ensure fallback title is consistently lowercased in WindowTitleWidget ([cab291e](https://github.com/rubiin/Tsumiki/commit/cab291ea1c85bcb959c70199d44733078481ca1b))
* improve alignment and spacing in notification and datetime menu widgets for better layout ([df53f47](https://github.com/rubiin/Tsumiki/commit/df53f4716bfaa8b79a92b6d9934ca0f785432bde))
* improve app preview handling on mouse enter and leave events ([39ab33b](https://github.com/rubiin/Tsumiki/commit/39ab33b84d76b48fbcc4af522fec8c921e6e0cd4))
* increase max character width for notification summary and body for better readability ([2e03b76](https://github.com/rubiin/Tsumiki/commit/2e03b76cd5feb564b8972b9cfaeb8b74a5580698))
* make animated scale more robust ([#221](https://github.com/rubiin/Tsumiki/issues/221)) ([afd7b76](https://github.com/rubiin/Tsumiki/commit/afd7b760491b6da064c482dc092174b648f1e3ab))
* move application start logging before running the app for better clarity ([f9dff5f](https://github.com/rubiin/Tsumiki/commit/f9dff5f8e54fa6691784a74973dc5e4d5a3949ea))
* network initialisation when no network available ([#209](https://github.com/rubiin/Tsumiki/issues/209)) ([15fc47b](https://github.com/rubiin/Tsumiki/commit/15fc47bbacf4c3f0da8df219c353b7eb3a2b51e9))
* pass widget_config to OverViewOverlay for proper initialization ([f7e0d46](https://github.com/rubiin/Tsumiki/commit/f7e0d46a647543aefe069b0054bcd37376b2ba34))
* power profile ([9810cc8](https://github.com/rubiin/Tsumiki/commit/9810cc81e9ab7e2beb2a50f229c2b9a742cfe702))
* remove ellipsize property from application widget label for improved text display ([065476a](https://github.com/rubiin/Tsumiki/commit/065476a85672c2597ca1d14b150d47ca859051a6))
* remove horizontal alignment from ButtonWidget container box ([026d893](https://github.com/rubiin/Tsumiki/commit/026d893f38b37d33e5d8c9c349df40f3b8b6acf9))
* remove unnecessary 'all_visible' parameter from widget initialization in multiple modules ([321a335](https://github.com/rubiin/Tsumiki/commit/321a33535cc59884d9624cad55fdf627571a4504))
* remove unused import and clean up label handling in AudioSlider and BluetoothDeviceBox ([89231ed](https://github.com/rubiin/Tsumiki/commit/89231edcf322ca42e027184b4a3abf77b7a47e90))
* remove unused style properties and improve label handling in popover and bluetooth submenu ([6b26a56](https://github.com/rubiin/Tsumiki/commit/6b26a56291849468870581c20db8e2dc6929c920))
* remove unused widgets from collapsible groups and center align button container ([af32895](https://github.com/rubiin/Tsumiki/commit/af328956ce29f431109a7044a82c34067e3c2f03))
* reorder battery settings and add overview to middle section in layout ([79f15da](https://github.com/rubiin/Tsumiki/commit/79f15da8a6f0c269bb1bb8a333ca805eb92c329e))
* scale image when setting new size in CircularImage ([1aefc8a](https://github.com/rubiin/Tsumiki/commit/1aefc8a388b2ca3a6bb46d211c67c6c3b5db7545))
* **scripts:** use -Su for AUR helper in arch update (avoid forced DB refresh) ([608421f](https://github.com/rubiin/Tsumiki/commit/608421f0a17e09a8c3b799a4fc44e3b6def42577))
* **scripts:** use -Syu for AUR helper in arch update command (perform full system + AUR upgrade) ([777110c](https://github.com/rubiin/Tsumiki/commit/777110c79840cacbdb1ad206624c6ced075c7713))
* simplify pixel size initialization in AudioSlider ([e4b250f](https://github.com/rubiin/Tsumiki/commit/e4b250f357e10c84bc034c3c8dc6ffb7e2177ac7))
* streamline enum formatting and required properties in schema ([d9956e3](https://github.com/rubiin/Tsumiki/commit/d9956e3392233d5ac7115ab782b0e567bdf6b42e))
* update address handling in AppBar and improve menu display logic ([18bbbfc](https://github.com/rubiin/Tsumiki/commit/18bbbfcc2dc42884fd3cc9fd6b67ebbc6dc1cac3))
* update audio icon handling to streamline volume state representation on slider ([9363040](https://github.com/rubiin/Tsumiki/commit/93630404d1f223d518e3777853d5381a2e581ae7))
* update banner and tsumiki images ([8728071](https://github.com/rubiin/Tsumiki/commit/87280718ec12928cfffa95f1b776c4e8484e8aa3))
* update border-radius for power control button and adjust hover border width ([bf17340](https://github.com/rubiin/Tsumiki/commit/bf17340d821ff05ec15dd83b374891a6168066cf))
* update box-shadow color mixing for hover effect in scrolledwindow ([bc9284b](https://github.com/rubiin/Tsumiki/commit/bc9284b2287473709026604bc09c65430c9bcd79))
* update box-shadow for power button menu and adjust focus styles for better visibility ([2dfc068](https://github.com/rubiin/Tsumiki/commit/2dfc068410b7d0128c50b1776aea73f8f5e3b7ab))
* update brightness slider to use screen brightness percentage ([c133174](https://github.com/rubiin/Tsumiki/commit/c1331749a1a600f124801201e57cd58cc30e5e23))
* update config access patterns to use get() for safer retrieval ([13ffd98](https://github.com/rubiin/Tsumiki/commit/13ffd98e2ffa479724b17e77c0a3cbfb8293a689))
* update daemon kill command for improved clarity and accuracy ([1c5aee9](https://github.com/rubiin/Tsumiki/commit/1c5aee90801b63351fb1f1a84535943ae30b87e6))
* update font size for date menu notification summary and body ([36d719d](https://github.com/rubiin/Tsumiki/commit/36d719d78f94e10c2fb422e33a44e40033942999))
* update monitor data retrieval to use json parsing ([f1eba38](https://github.com/rubiin/Tsumiki/commit/f1eba38576a8b63348ec31c09782b823215c69c6))
* update notification image size for improved display in DateMenuNotification widget ([44028f4](https://github.com/rubiin/Tsumiki/commit/44028f44e9d4715148744acddf95303b43ced628))
* update power button menu structure and improve transition duration ([ea8109c](https://github.com/rubiin/Tsumiki/commit/ea8109c19ff8b993c9124b40c8b49fdd672ded0e))
* update power control button styles for improved focus and hover effects ([fcbd71d](https://github.com/rubiin/Tsumiki/commit/fcbd71d051faa9843f114ae0e6bae85cb02cfc68))
* update power profile setting to use the correct profile attribute ([c265fae](https://github.com/rubiin/Tsumiki/commit/c265faeb5103857a2ea74f25ea809177d0a629a3))
* update README with post-installation instructions for hyprland.conf ([69a5410](https://github.com/rubiin/Tsumiki/commit/69a541081923bf49cceb62259c82bdf2ae72f875))
* update submap handling to correctly process string input and fix command string ([1733028](https://github.com/rubiin/Tsumiki/commit/1733028fd1fd11d6206f5230c62f67fc513a1f79))
* update titles for various UI components to improve consistency ([42bfa45](https://github.com/rubiin/Tsumiki/commit/42bfa457da1ae2d822226d3c8cb5d7399ffd7dac))
* update Tsumiki image dimensions for better visibility ([1e0cbfd](https://github.com/rubiin/Tsumiki/commit/1e0cbfde1616e4e207a66493efeca770abc8f268))


### ⚙️ Chores

* **deps:** update dependency pillow to v12 ([#227](https://github.com/rubiin/Tsumiki/issues/227)) ([3d21e5d](https://github.com/rubiin/Tsumiki/commit/3d21e5d6e80ade045f96314d568deaa304fa1f41))
* release 2.5.0 ([f1bab66](https://github.com/rubiin/Tsumiki/commit/f1bab66fa9cf99f14e58db7a613f95708ff1a9db))
* remove author and license comments from swipingbutton.py ([84edba0](https://github.com/rubiin/Tsumiki/commit/84edba07251354605961dd0909cac26f31cb5c06))
* update click and psutil versions in requirements.txt ([019e40a](https://github.com/rubiin/Tsumiki/commit/019e40a949c6251f0893779020150b6c94862575))


### ♻️ Code Refactoring

* add active style class to button widgets and manage popover state ([3cc603a](https://github.com/rubiin/Tsumiki/commit/3cc603a6263644463dbf938b61e553d745771c28))
* add type hints for better code clarity and maintainability ([ba2e38e](https://github.com/rubiin/Tsumiki/commit/ba2e38ec0ac4240fd465bd8a952a7d42384c5c75))
* **animator:** consolidate bezier helpers into shared.animator and update Animator internals ([534f959](https://github.com/rubiin/Tsumiki/commit/534f959f868ac9133830a2409fc21e516800f7a7))
* **collapsible:** lazy-import Popover and clear active state; remove panel margin ([c4e1139](https://github.com/rubiin/Tsumiki/commit/c4e1139a3ef027eef85c3923de311de2c69acdc7))
* **collapsible:** tidy popup.connect indentation and reorganize collapsible_group SCSS; use #collapsible_group nesting for active/hover rules and clean up whitespace ([cf83aae](https://github.com/rubiin/Tsumiki/commit/cf83aaeebd67f00f465be153454ca6972986bf0a))
* **core:** streamline services and utilities, replace loguru with fabric logger ([#223](https://github.com/rubiin/Tsumiki/issues/223)) ([eba8c3b](https://github.com/rubiin/Tsumiki/commit/eba8c3bb9bcef016a841c1eab46c9a4bbad16887))
* **dock:** use CenterBox to center revealer and add side spacers for larger hover area ([7d1b06f](https://github.com/rubiin/Tsumiki/commit/7d1b06f8484e967b622b02db209201c26a21b83d))
* enhance tooltip construction for update functions in systemupdates.sh ([62cb3be](https://github.com/rubiin/Tsumiki/commit/62cb3be111ee46bc154ec694cb3cd97ef497ca8e))
* goodbye gray ([042c17b](https://github.com/rubiin/Tsumiki/commit/042c17bfda8b325a8ee8bffe8368288582951caa))
* **logging:** enhance logging control by adding config option for disabling logs in non-debug mode ([#224](https://github.com/rubiin/Tsumiki/issues/224)) ([f3c4acf](https://github.com/rubiin/Tsumiki/commit/f3c4acfab3afae2957b5e510fb85d348caa73ea0))
* move imports for AppLauncher and widget_config into the _get_or_create_launcher method ([2a43900](https://github.com/rubiin/Tsumiki/commit/2a43900579438be3934498f4f3afaa776ea89f19))
* pass popup parameter to QuickSettingsButtonBox and related toggles ([#220](https://github.com/rubiin/Tsumiki/issues/220)) ([f37cf91](https://github.com/rubiin/Tsumiki/commit/f37cf91fdce09d6934626df66cc83c46f6a6ddbf))
* remove redundant initialization of Glace.Manager in TaskBarWidget ([0ba59fc](https://github.com/rubiin/Tsumiki/commit/0ba59fc441ce6961647e05a3bcfbb7581a646eb1))
* rename private methods to public in various modules for consistency ([dcd57d8](https://github.com/rubiin/Tsumiki/commit/dcd57d894bffaceae0030443ce4417c6b49b8d52))
* reorganize TypedDict definitions and add missing fields for consistency ([b001ed2](https://github.com/rubiin/Tsumiki/commit/b001ed2f8fcd94ebd853ef261fed775cef3c42e7))
* replace exec_shell_command_async with hyprland_connection methods in various widgets ([a27e00e](https://github.com/rubiin/Tsumiki/commit/a27e00ec1b525a393b764f43db0955c63e2f0dd4))
* replace get_relative_path with ASSETS_DIR for asset path management ([8da0623](https://github.com/rubiin/Tsumiki/commit/8da0623637e5a3c847b8d1754b7fc773ddfef3b3))
* replace GLib.source_remove with remove_handler for consistency ([2967706](https://github.com/rubiin/Tsumiki/commit/2967706555630487f3eb913b5a6ad07ce5762bc9))
* replace read_json_file with load_json and update related function names for consistency ([3ff23dd](https://github.com/rubiin/Tsumiki/commit/3ff23dd3f94368fc5d3c51fde92f051738f910e4))
* replace reusable_fabricator with invoke_repeater for period… ([#218](https://github.com/rubiin/Tsumiki/issues/218)) ([2c9ba20](https://github.com/rubiin/Tsumiki/commit/2c9ba20c1d84e8d9a305e5e948413e05415e8654))
* simplify menu item handling in AppBar and consolidate pinning logic ([7991887](https://github.com/rubiin/Tsumiki/commit/79918875b8bc49b7b0acfbbcbace98db88644d11))
* streamline enum and required properties formatting in schema ([a6d6bad](https://github.com/rubiin/Tsumiki/commit/a6d6baddda553cfdd3e641af945f254ce8a7b427))
* streamline enum and required properties formatting in schema ([606a516](https://github.com/rubiin/Tsumiki/commit/606a516b016260f74a3f1a152ddd27a1b122a95f))
* streamline menu item creation and management in AppBar ([503bb2c](https://github.com/rubiin/Tsumiki/commit/503bb2c64d49ce6abce95bc039de9bd8e87ef924))
* streamline workspace button setup and state management in WorkSpacesWidget ([3027096](https://github.com/rubiin/Tsumiki/commit/30270966874176901dcfec731548e09f13da6a7f))
* streamline workspace handling in Dock and WindowCountWidget ([e4aea5f](https://github.com/rubiin/Tsumiki/commit/e4aea5f19dc6922c31dea367196801d4a7444a91))
* **styles:** centralize popover styling and enable popover shadow; update popovers and clean up duplicated includes ([24db1ec](https://github.com/rubiin/Tsumiki/commit/24db1ec86eefe576d090f1d05f05deeac3e97933))
* **styles:** reduce bar menus popover padding to 0.5em / 0.2em ([5207892](https://github.com/rubiin/Tsumiki/commit/52078929fcb24a73a1bd3449a32a0e031ec4bf8c))
* **styles:** remove blur/spread and set full opacity for bar menus popover shadow ([92e32f9](https://github.com/rubiin/Tsumiki/commit/92e32f966b4c3532cba37c8ad1366a475d710fb5))
* **styles:** set quick_settings slider height to 7px and enable slider in theme & settings ([8c1c570](https://github.com/rubiin/Tsumiki/commit/8c1c57009380b929662ab226179d1faa43db30d3))
* **ui:** add icon padding, use HoverButton for power profiles, and tidy whitespace ([504c8ce](https://github.com/rubiin/Tsumiki/commit/504c8ce0d8b2cc6cd21ef726d910eae3650ade53))
* **ui:** set pointer cursor on ButtonWidget state change and remove stray blank line in window_title ([094bf91](https://github.com/rubiin/Tsumiki/commit/094bf911161f5734fa6c579430b4413be6e67508))
* update constructor signatures to use dict type hints for config ([4d11c84](https://github.com/rubiin/Tsumiki/commit/4d11c844f78e3bd6635ff0158f825904f538040f))
* update LauncherConfig to use BarConfig type hint in app_launcher.py ([62cb3be](https://github.com/rubiin/Tsumiki/commit/62cb3be111ee46bc154ec694cb3cd97ef497ca8e))
* update OSDContainer to use BarConfig type hint in osd.py ([62cb3be](https://github.com/rubiin/Tsumiki/commit/62cb3be111ee46bc154ec694cb3cd97ef497ca8e))
* update style_classes to use list format for consistency across widgets ([9f76ff5](https://github.com/rubiin/Tsumiki/commit/9f76ff52de88a6a745c68476207b4b01d931a6d6))
* update widget type hints for improved clarity and consistency ([13ce89d](https://github.com/rubiin/Tsumiki/commit/13ce89d0a3f79ad55159692a9ea2dd12e66b4ee5))
* update Widget_Groups definition to use a list of TypedDict for improved structure ([1925e57](https://github.com/rubiin/Tsumiki/commit/1925e57f40e5f8751e6768be575a40955b893ab2))


### 🚀 CI Improvements

* add GitHub Actions workflow to auto-update Wiki from doc.md on push ([e641c10](https://github.com/rubiin/Tsumiki/commit/e641c104ad73bd710c7a67fc3e5cacca26544bbb))

## [2.4.1](https://github.com/rubiin/Tsumiki/compare/v2.4.0...v2.4.1) (2025-09-06)


### 🐛 Bug Fixes

* add circular progress bar to notification widget and implement timeout animation ([3b81fca](https://github.com/rubiin/Tsumiki/commit/3b81fca7ff6703d5136b4a34bc662aa12592940a))
* add separator to AppBar and update visibility logic based on pinned apps ([5ae6623](https://github.com/rubiin/Tsumiki/commit/5ae66231e94b65e89b25bca69bb6fc36a3e29362))
* consolidate transition styles into scrolledwindow and remove redundant button hover styles ([aaa5ecf](https://github.com/rubiin/Tsumiki/commit/aaa5ecf07d541c989c919e24992cd91fee284b0b))
* enhance forecast box cleanup by destroying child widgets when removed ([5488bd0](https://github.com/rubiin/Tsumiki/commit/5488bd079e4fc88f0858e6c0b934e8a8bbd67494))
* ensure proper cleanup of app bar items by destroying the box on close ([c40c9dd](https://github.com/rubiin/Tsumiki/commit/c40c9dd1fbaf72f361d474791f4601f8ae70bcd3))
* ensure proper cleanup of Bluetooth device rows by destroying the row on removal ([5488bd0](https://github.com/rubiin/Tsumiki/commit/5488bd079e4fc88f0858e6c0b934e8a8bbd67494))
* format JSON schema for better readability and update enum values in definitions ([3029405](https://github.com/rubiin/Tsumiki/commit/302940532c57a7b0e38f4aaa201edd95e81747fc))
* implement app launcher toggle functionality in AppBar and update dock style reference ([7a9e854](https://github.com/rubiin/Tsumiki/commit/7a9e854d5692fb39b3298beb8218dc4fdbd71aad))
* integrate CircularImage into AppBar and update related styles and schema ([d908d66](https://github.com/rubiin/Tsumiki/commit/d908d66c056cb2346e540081a24845ad8baf434b))
* pin PyGObject version to 3.50.0 for compatibility ([65f4382](https://github.com/rubiin/Tsumiki/commit/65f438208dfe3553bad0a10927f94393b5640eb1))
* reduce vertical padding in dock and app launcher settings for improved layout consistency ([150333d](https://github.com/rubiin/Tsumiki/commit/150333d8f6e148a15cd5c3e5e68b4fc623ee5eed))
* refactor AppLauncher viewport initialization and add CheatSheet and KeybindLoader classes ([ccaf9cf](https://github.com/rubiin/Tsumiki/commit/ccaf9cfbeb1e295b52aa7ac75f7ce9a315a1c7e7))
* rename CircleImage to CircularImage across multiple modules ([d6ba3a3](https://github.com/rubiin/Tsumiki/commit/d6ba3a37ef8ce05d1cf5eb1f8f15938d0c7a9b52))
* rename update methods to use a consistent naming convention across multiple widgets ([10c4864](https://github.com/rubiin/Tsumiki/commit/10c486407154c0e3b5fe83c513c53e3b10cd69e1))
* replace print statements with logger.exception for improved error handling across multiple modules ([52f79fd](https://github.com/rubiin/Tsumiki/commit/52f79fdbff7c064e4da4d82ade73cdfcce0acd0c))
* update AppWidgetFactory style to use style classes and adjust icon margin in common styles ([a575206](https://github.com/rubiin/Tsumiki/commit/a575206ff5d634282ea3c7b89b2c1b5a0206d104))
* update connection handling in WindowCountWidget and MonitorWatcher classes ([e37f232](https://github.com/rubiin/Tsumiki/commit/e37f2329050afc532d0c03dd710981f5ffaf4bc6))
* update layout configuration by removing app_launcher_button from left_section and cleaning up middle_section ([45d1799](https://github.com/rubiin/Tsumiki/commit/45d1799d8170186eba16d9e6103ceb54d313e9b6))
* update pinned apps handling and improve separator visibility logic ([902ee92](https://github.com/rubiin/Tsumiki/commit/902ee9253eb0a26458ef734246f6768d35773133))
* update reference for custom_button in schema to correct path ([6f7c4f3](https://github.com/rubiin/Tsumiki/commit/6f7c4f367a188ddc40f8d163766809607a669ff0))
* update style classes and layout properties in AppWidgetFactory and AppLauncher ([aca9be1](https://github.com/rubiin/Tsumiki/commit/aca9be14b361f024631a8ca7a48324a371eaa564))

## [2.4.0](https://github.com/rubiin/Tsumiki/compare/v2.3.0...v2.4.0) (2025-09-03)


### 🚀 New Features

* add confirmation option to power button actions and update related configurations ([c3baab6](https://github.com/rubiin/Tsumiki/commit/c3baab6a008f5c445b48abea8932d197ff5438b6))
* add search entry icons and clear functionality in app launcher and clip history menu ([681c4a9](https://github.com/rubiin/Tsumiki/commit/681c4a9477f59a20d64801abcfff80aaeac7c9dd))
* App launcher button and usable menu ([#197](https://github.com/rubiin/Tsumiki/issues/197)) ([d7f74eb](https://github.com/rubiin/Tsumiki/commit/d7f74eb8615f2e00dda81a757744480863801087))
* enhance app launcher with tooltip and icon size adjustments; set process name in GLib ([72128c4](https://github.com/rubiin/Tsumiki/commit/72128c4ecab1ae2df14f2be4016b3b0d26f184e6))
* implement process name setting and improve notification sound handling ([0d09bb6](https://github.com/rubiin/Tsumiki/commit/0d09bb64d40939d6516f07b3e138800f3da8c5a5))


### 🐛 Bug Fixes

* add icon size to app launcher button and update layout sections ([a59d183](https://github.com/rubiin/Tsumiki/commit/a59d18391215df21ddfea08efbcda54a14fdfeef))
* add name attribute to dock and osd modules for better identification ([3ff5ddb](https://github.com/rubiin/Tsumiki/commit/3ff5ddb6927604479632ca9680b77913b3fddb58))
* change transition type to slide-down for dialog and power menu popups ([b9972bf](https://github.com/rubiin/Tsumiki/commit/b9972bf7ca631a7744521851d483f48b3d1c55b8))
* downgrade pygobject ([d5b8c3d](https://github.com/rubiin/Tsumiki/commit/d5b8c3d4323f88f349d7056939bc0779ef9e9b4f))
* ensure dialog popup toggles after executing command ([90f43c5](https://github.com/rubiin/Tsumiki/commit/90f43c52bb48739cb000ca3ff44960228a5e072a))
* ensure rebase occurs when conflicts are detected ([c3b0950](https://github.com/rubiin/Tsumiki/commit/c3b095054d5eb485dac83a715de79b306a6b7fb6))
* nested ([bd86a51](https://github.com/rubiin/Tsumiki/commit/bd86a5168f3b8d22458387b798dad6825ed14ab7))
* refactor init_device_audio method for clarity and remove nested function ([b1ad892](https://github.com/rubiin/Tsumiki/commit/b1ad8929c89884063871b431f61a135cf6204579))
* toggle dialog popup after executing command in the dialog class ([1c806dd](https://github.com/rubiin/Tsumiki/commit/1c806dd3a94d320c5bc1e9f9211136d280a09a9b))
* update scale value and improve workspace label styling in overview ([60d5d86](https://github.com/rubiin/Tsumiki/commit/60d5d861a0169d385af6e52e2a22375ce32f6854))


### ♻️ Code Refactoring

* clean up app launcher styles and remove unused focus styles ([b46fc61](https://github.com/rubiin/Tsumiki/commit/b46fc61bb4432460a10e598ad6639cfce92fbd44))
* eliminate nested functions for improved readability ([88d346c](https://github.com/rubiin/Tsumiki/commit/88d346c7686d3e26d2c450b2ca2923846a7d9cbb))
* improve dialog and power menu popup initialization and transition handling ([14dd13a](https://github.com/rubiin/Tsumiki/commit/14dd13a011a8af81a8c3ec32f139365746447bd7))
* streamline StatusBar bar recreation logic and remove unused process name setting ([2e23419](https://github.com/rubiin/Tsumiki/commit/2e23419cbf42f9e68a997b0ee4a1dd26b68fc851))


### 🚀 CI Improvements

* Update checkout action version from v5 to v4 ([d66a6ee](https://github.com/rubiin/Tsumiki/commit/d66a6ee7d5e06a21903f332df2c61e9ad84212ad))

## [2.3.0](https://github.com/rubiin/Tsumiki/compare/v2.2.0...v2.3.0) (2025-08-30)


### 🚀 New Features

* Add multi-monitor support ([#195](https://github.com/rubiin/Tsumiki/issues/195)) ([8804a73](https://github.com/rubiin/Tsumiki/commit/8804a733682c1c8a6586dd445beb3ef58c498dc3))


### 🐛 Bug Fixes

* close active submenus when QuickSettingsButtonBox is unmapped ([174dd67](https://github.com/rubiin/Tsumiki/commit/174dd672bc15aa6ebbf77acf7a79738f6ed8c9f4))
* correct formatting of dotfiles link in README ([8299fc7](https://github.com/rubiin/Tsumiki/commit/8299fc790e91fe1e366b7acbc80e55a16c3156b1))
* prevent multiple simultaneous wallpaper loads in WallpaperPickerBox ([b89cff4](https://github.com/rubiin/Tsumiki/commit/b89cff41680d87ef4edccf4175e637d4b2e8dac1))
* refactor submenu handling in QuickSettingsButtonBox ([27443ec](https://github.com/rubiin/Tsumiki/commit/27443ecb2e6c65491eed234cfd7c2ab443cc82bd))
* remove debug print statement from on_scroll method in DateNotificationMenu ([f6d6457](https://github.com/rubiin/Tsumiki/commit/f6d645791f1fbd9230c140f6f3d3c57920c36924))


### ⚡️ Performance Improvements

* simplify DND switch handling and improve notification removal logic ([58905ab](https://github.com/rubiin/Tsumiki/commit/58905abc9f3de7f2d249a4857bdf08a4ace470e1))


### ♻️ Code Refactoring

* rename load_more_items to _load_next_batch for consistency ([cd5e87c](https://github.com/rubiin/Tsumiki/commit/cd5e87cbe30ed7927a0f5f912d8fa70e73f31b25))

## [2.2.0](https://github.com/rubiin/Tsumiki/compare/v2.1.0...v2.2.0) (2025-08-28)


### 🚀 New Features

* add hover_reveal and reveal_duration options to DateTimeMenu and update transition_duration in widgets ([662df5d](https://github.com/rubiin/Tsumiki/commit/662df5ddcb431620e289e55fe0c63dafdda69fe3))
* add reveal_duration option on date_time ([b9aee3f](https://github.com/rubiin/Tsumiki/commit/b9aee3f889859707aeaf2d3a952cbb4a55b8e62c))


### 🐛 Bug Fixes

* install packages command ([af74941](https://github.com/rubiin/Tsumiki/commit/af749410a3c2f92365f79d12b80bd5f18c3c6a03))
* update user avatar path handling in QuickSettingsMenu ([#193](https://github.com/rubiin/Tsumiki/issues/193)) ([5556f03](https://github.com/rubiin/Tsumiki/commit/5556f0356066a0c8d862ac169fe4fa83e08799d6))


### 📚 Documentation

* add N1xev as a contributor for doc ([#192](https://github.com/rubiin/Tsumiki/issues/192)) ([07cf6fe](https://github.com/rubiin/Tsumiki/commit/07cf6fe842fd96cbf132d5b45bb803af479d625b))


### ♻️ Code Refactoring

* move hover logic to base class ([a64f041](https://github.com/rubiin/Tsumiki/commit/a64f04174586ddc60c813e47b977410e6105ebcb))
* replace 'box' with 'container_box' in widget classes for consistency ([53aece5](https://github.com/rubiin/Tsumiki/commit/53aece5a9450261609a40676ad925488b58f66f5))
* replace set_reveal_child with reveal/unreveal methods in various modules for consistency ([67975c0](https://github.com/rubiin/Tsumiki/commit/67975c06483a737c3569cdc77c594a8422302675))

## [2.1.0](https://github.com/rubiin/Tsumiki/compare/v2.0.2...v2.1.0) (2025-08-24)


### 🚀 New Features

* add BaseWindow class for custom window extensions ([cdd2c20](https://github.com/rubiin/Tsumiki/commit/cdd2c201fc33f18ebc0294ce606c1f1b71504693))
* add custom button schema with properties for command, icon, label, and tooltip ([b8cfecd](https://github.com/rubiin/Tsumiki/commit/b8cfecd7c43279d007fe057b5cc286f1aab6a3fd))
* add exclusive keyboard mode to OverViewOverlay popup ([dc3d05e](https://github.com/rubiin/Tsumiki/commit/dc3d05e4501734e2ce0afe70693408c1ad7fc100))
* add hide_on_default option to widgets and update submap behavior ([8d33143](https://github.com/rubiin/Tsumiki/commit/8d33143e05c8830d27ab1bcaaf4707fe27e4419c))
* add mappings option to window title configuration and update related components ([#186](https://github.com/rubiin/Tsumiki/issues/186)) ([74b3e6d](https://github.com/rubiin/Tsumiki/commit/74b3e6dded52390ce85560d33d08372b16d22206))
* add TeamSpeak to the window title map ([43dcb48](https://github.com/rubiin/Tsumiki/commit/43dcb48894ec917ac843640c78a5526880b12f31))


### 🐛 Bug Fixes

* adjust truncation size and disable mappings in window title configuration ([e5f1de4](https://github.com/rubiin/Tsumiki/commit/e5f1de49d1b573f803ec0e590b6a8871b84d3686))
* ensure truncation behavior respects configuration in WindowTitleWidget ([30533af](https://github.com/rubiin/Tsumiki/commit/30533af94a2424a36fa7bb83cab885078e0f83cc))
* update method name for finding desktop applications ([a59e96b](https://github.com/rubiin/Tsumiki/commit/a59e96b32ef4d7e6416750c2112f222291153da5))
* update schedule time to 2pm on Monday in renovate configuration ([b0f559a](https://github.com/rubiin/Tsumiki/commit/b0f559a7a7752642cce2b0b77db107b274170bae))
* update stubs generation command to use fabric-cli instead of gengir ([95aa767](https://github.com/rubiin/Tsumiki/commit/95aa767ea1ebbb7058244828d5ca7fe65bfedc55))


### ⚙️ Chores

* **deps:** update all non-major dependencies ([#187](https://github.com/rubiin/Tsumiki/issues/187)) ([75ce690](https://github.com/rubiin/Tsumiki/commit/75ce690fe35f929c4da746745f66757c90950c6f))
* **deps:** update dependency rlottie-python to v1.3.8 ([#188](https://github.com/rubiin/Tsumiki/issues/188)) ([51a826e](https://github.com/rubiin/Tsumiki/commit/51a826e48a4f1257d662cac5186045653fd7e57f))


### ♻️ Code Refactoring

* add anchor property to Dock initialization for improved positioning ([1213a09](https://github.com/rubiin/Tsumiki/commit/1213a0945d9cdbd331c019eb107387cf1013ce5e))
* disable annotation for screenshot widget and remove location property from general settings ([b6df5df](https://github.com/rubiin/Tsumiki/commit/b6df5df6321982b0aee68e35aa7cbdc14e275f00))
* enhance Arch-based distro check and improve Python detection logic ([a046798](https://github.com/rubiin/Tsumiki/commit/a046798c9622000cb1d3b64b0aa8f466f3d791d0))
* enhance logging messages with emojis for better user feedback ([4572961](https://github.com/rubiin/Tsumiki/commit/457296169014bd8aa853b73be1f7b45de9b5263c))
* expand Arch-based distro check to include additional distributions ([f5defcd](https://github.com/rubiin/Tsumiki/commit/f5defcd74cdc5138d2067b4457a03a1843ffc480))
* initialize menu as None and create it on demand in show_menu method ([f532a04](https://github.com/rubiin/Tsumiki/commit/f532a046d0f69fa0f7cc5aba376e463504ad10e1))
* manage pinned apps with a dedicated separator and cleanup logic ([89430aa](https://github.com/rubiin/Tsumiki/commit/89430aa1ff5275e69b3846b961db3f45a1a1e09f))
* remove anchor property from dock configuration and schema ([f955c09](https://github.com/rubiin/Tsumiki/commit/f955c094a9c26808d8154dbb703760450ac0250a))
* remove redundant docstring from BaseWidget class ([a1a3f1c](https://github.com/rubiin/Tsumiki/commit/a1a3f1c33f450b0b44ae84543405d0535d8965a0))
* replace set_has_class with toggle_css_class for consistency in widget state management ([7ae0bed](https://github.com/rubiin/Tsumiki/commit/7ae0beded1e6162b8483dc9fbbe64dfacecf73d4))
* simplify TaskBarWidget by removing Hyprland integration and unused code ([cd3fb36](https://github.com/rubiin/Tsumiki/commit/cd3fb36a265997e5ac6e961021da396117cc65ed))
* update Python checks and fix PyGObject version in requirements ([6802725](https://github.com/rubiin/Tsumiki/commit/6802725a449e9d09a20e5cd81dfa4a6386cedb9f))

## [2.0.2](https://github.com/rubiin/Tsumiki/compare/v2.0.1...v2.0.2) (2025-08-15)


### 🚀 New Features

* Add Auto-Reload Configuration Feature ([#156](https://github.com/rubiin/Tsumiki/issues/156)) ([55620f3](https://github.com/rubiin/Tsumiki/commit/55620f3da7f721dcd1da867897e2067a04b6d7a0))


### 🐛 Bug Fixes

* add default values to various properties in schema for improved configuration ([52e62b0](https://github.com/rubiin/Tsumiki/commit/52e62b029576f5130d95d4bb38223aa0c4068dcd))
* add error handling and logging for monitor and keyboard layout retrieval ([5beca69](https://github.com/rubiin/Tsumiki/commit/5beca69e7e57327cee7fa6c422041c93847d4747))
* enhance config auto-reload functionality and improve logger messages ([8b236db](https://github.com/rubiin/Tsumiki/commit/8b236db559a62cf32263d11c9af5fac4812653e6))
* remove pin option from Renovate configuration ([1e04466](https://github.com/rubiin/Tsumiki/commit/1e04466493dba69e27c42433760bdb93e8062ae4))
* update json schema ([98684b7](https://github.com/rubiin/Tsumiki/commit/98684b7c9acd9daf2f25ad2b051ebe528c303734))
* update visibility of revert and add dependency updates section ([cf13f2f](https://github.com/rubiin/Tsumiki/commit/cf13f2fd90536c4e96649ac12f987bffdded91d5))


### ⚙️ Chores

* add renovate configuration for grouping Python packages ([33b7289](https://github.com/rubiin/Tsumiki/commit/33b72890dd632069203e1b051c6662da6d2a5628))
* **deps:** update all non-major dependencies ([#178](https://github.com/rubiin/Tsumiki/issues/178)) ([a57942e](https://github.com/rubiin/Tsumiki/commit/a57942e3cba3774c4436a16577e4e3d5cb8fc7f0))
* **deps:** update dependency psutil to v7 ([#179](https://github.com/rubiin/Tsumiki/issues/179)) ([794b87a](https://github.com/rubiin/Tsumiki/commit/794b87ae80806127b66fddd6e52d49cc8a95f66f))


### ♻️ Code Refactoring

* add type hints to function signatures for improved clarity ([94699e3](https://github.com/rubiin/Tsumiki/commit/94699e3c5dfa7970a65e83ca3bb72d727cb5d584))
* move Animator import statements inside relevant methods for better encapsulation ([a164c2c](https://github.com/rubiin/Tsumiki/commit/a164c2c254df6a496349d00115aec463f208ba38))
* move Popover import statements inside show_popover methods for better encapsulation ([d1fd8cf](https://github.com/rubiin/Tsumiki/commit/d1fd8cf8a212ccabbbebe55956b727e051833b44))
* remove unused layout and general properties from schema ([bd745aa](https://github.com/rubiin/Tsumiki/commit/bd745aaedd99693ee7ceef22b2322fc22010c9b2))
* rename get_hyprland_connection variable for clarity and consistency ([1b8afc4](https://github.com/rubiin/Tsumiki/commit/1b8afc4ab00826e66178f0721a9d193b001efe1b))
* rename PopupWindow to PopOverWindow for consistency ([5cfd028](https://github.com/rubiin/Tsumiki/commit/5cfd028e10733b5e11619ddda877e3caa6acd828))
* replace List with built-in list for type hints consistency ([639b9c8](https://github.com/rubiin/Tsumiki/commit/639b9c8d2a477e67e8da1b233479087fc335a211))

## [2.0.1](https://github.com/rubiin/Tsumiki/compare/v2.0.0...v2.0.1) (2025-08-14)


### 🐛 Bug Fixes

* update widget item type to reference definitions in schema ([cd6e034](https://github.com/rubiin/Tsumiki/commit/cd6e03446a0f8f112ff83747822e75d06ffe0ea0))


### 🎨 Code Style

* format JSON files for consistent indentation ([ffcb90f](https://github.com/rubiin/Tsumiki/commit/ffcb90faa2182e8579f0c752b09098115894adb8))


### ⚙️ Chores

* move release-please configuration files to .github ([67cd0f1](https://github.com/rubiin/Tsumiki/commit/67cd0f1cd9a64a1918576966c59409adba71e65c))


### ♻️ Code Refactoring

* unified widget resolver system ([84d7d94](https://github.com/rubiin/Tsumiki/commit/84d7d948569e2c5a1d7090a4dcfa806661c23b0f))


### 🚀 CI Improvements

* update release please ([3ef4d9c](https://github.com/rubiin/Tsumiki/commit/3ef4d9cc6e4a7f67d2ef223e1fe23a65ee49d8bb))

## [2.0.0](https://github.com/rubiin/Tsumiki/compare/v1.4.0...v2.0.0) (2025-08-13)


### ⚠ BREAKING CHANGES

* no longer supports json5 on json, use json

### Features

* refactor init script and add detached option ([#157](https://github.com/rubiin/Tsumiki/issues/157)) ([b5a0743](https://github.com/rubiin/Tsumiki/commit/b5a074310db05eda2cff16f0e9440e509b66090f))


### Bug Fixes

* add 'autorelease: pending' to exempt-issue-labels in lock.yml ([ecee420](https://github.com/rubiin/Tsumiki/commit/ecee420ee64ffc0488b5547b9a3671eb6990e00c))
* update release type to python in release workflow ([8a0873c](https://github.com/rubiin/Tsumiki/commit/8a0873cfa6be93c2e2a260fb1ea2290c0e86e461))


### Code Refactoring

* remove pyjson5 dependency, and json5 ([f74c95f](https://github.com/rubiin/Tsumiki/commit/f74c95f5a31e60c5388fd46ad7c9fb38fa9d9327))

## [1.4.0](https://github.com/rubiin/Tsumiki/compare/v1.3.0...v1.4.0) (2025-08-13)


### Features

* Add Auto-Reload Configuration Feature ([#156](https://github.com/rubiin/Tsumiki/issues/156)) ([7371b62](https://github.com/rubiin/Tsumiki/commit/7371b62e1ba5c99636e2a2fbd0352ce64a9f3834))
* add initial Renovate configuration for Python dependencies ([b09b819](https://github.com/rubiin/Tsumiki/commit/b09b81960cc9cfc2bba74b1106ab58c6c895094d))


### Bug Fixes

* add default values to various properties in schema for improved configuration ([8bcfc53](https://github.com/rubiin/Tsumiki/commit/8bcfc536440927244a7083b4b324078203ea3f2c))
* add error handling and logging for monitor and keyboard layout retrieval ([02ebed4](https://github.com/rubiin/Tsumiki/commit/02ebed4e50b25475d40c741849c2e2edeab78b2e))
* clipboard manager UTF-8 encoding ([fcd8156](https://github.com/rubiin/Tsumiki/commit/fcd8156a21dc5162cd2b952b332292968a74e045))
* enhance config auto-reload functionality and improve logger messages ([2c71b10](https://github.com/rubiin/Tsumiki/commit/2c71b10c3c9a41c4e8b8aa6075cfd276923c76a8))
* update default icon for custom button and clipboard history widgets ([d7fd76c](https://github.com/rubiin/Tsumiki/commit/d7fd76ca1f04c5eff15a34958e74deecdb422b17))
* update exempt-issue-labels to include enhancement and bug labels ([f130556](https://github.com/rubiin/Tsumiki/commit/f130556181cabdae7f715b7f52927ba69e4b81ac))
* update permissions in release workflow to include issues ([7c2c753](https://github.com/rubiin/Tsumiki/commit/7c2c7533000c2f19cb6ddf42ddd69332d10e6fd7))
* update Renovate configuration to set range strategy and add labels ([da45d99](https://github.com/rubiin/Tsumiki/commit/da45d993c4ed8b7b8413443b054731a82e24ac33))

## [1.3.0](https://github.com/rubiin/Tsumiki/compare/v1.2.1...v1.3.0) (2025-08-13)


### Features

* add tooltip support to window title widget ([781d5ae](https://github.com/rubiin/Tsumiki/commit/781d5ae60497cb9898ec23d87213965c4d42a1c2))


### Bug Fixes

* clean up default configuration by removing unnecessary comments and duplicate icon entry ([999889c](https://github.com/rubiin/Tsumiki/commit/999889ce1bca9ef471085633d1324c97f94d1a90))
* get client data method ([dc28a8b](https://github.com/rubiin/Tsumiki/commit/dc28a8b5cc2a21c39d95d2d7eb61c30111933f10))
* implement sound capture option in screen recording and screenshot methods ([7c51470](https://github.com/rubiin/Tsumiki/commit/7c51470748d4b127fa260a21bc80c49cfde037a5))
* refactor AppBar initialization and clean up unused styles in dock ([d66b247](https://github.com/rubiin/Tsumiki/commit/d66b2475a243fb04885e0e8e1c6395cc5971e1cd))
* remove unnecessary comments and improve code clarity in widget initializations ([4183b3a](https://github.com/rubiin/Tsumiki/commit/4183b3ad5c54e50d01b09485ebcd8aa04683ad76))
* remove unused spacing configuration from constants ([d568a24](https://github.com/rubiin/Tsumiki/commit/d568a24e0168dfb9e35fe0711a7023d412c27b9b))
* replace HyprlandWithMonitors with get_hyprland_connection for improved connection handling ([ef880d4](https://github.com/rubiin/Tsumiki/commit/ef880d403eab0e44153c2cd13970e2222071389c))
* simplify pinned apps initialization in AppBar by using a fallback for None ([7752fe5](https://github.com/rubiin/Tsumiki/commit/7752fe5179f84b96bca76ff4f8aec61580f9f2f9))
* streamline screen recording and screenshot methods by removing redundant path parameter ([94090c2](https://github.com/rubiin/Tsumiki/commit/94090c2634380ba03be3963886083aef3b185575))
* truncate action button label to improve UI clarity ([9290a30](https://github.com/rubiin/Tsumiki/commit/9290a3005d8130dc08e05090c4951ea384c3347c))
* update button styles in common and dock for improved UI consistency ([d010355](https://github.com/rubiin/Tsumiki/commit/d010355f31c0e30a697b8b03ae6af6fcee273796))
* update dock opacity for improved visibility ([31d5381](https://github.com/rubiin/Tsumiki/commit/31d5381d49ec449aa50470d5786c863e65045cbd))
* update sound capture setting to false and enable hover reveal in weather widget ([864b9a8](https://github.com/rubiin/Tsumiki/commit/864b9a8d1ddd4da3a3c0554839c4ed9dab074f12))
