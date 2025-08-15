# Changelog

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
