# Changelog

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
