# Changelog

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
