# Changelog

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
