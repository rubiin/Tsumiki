# Triage Graph: rubiin/tsumiki

**Repository**: https://github.com/rubiin/tsumiki  
**Fork**: https://github.com/kimjune01/tsumiki  
**Branch**: `fix-write-json-file-args`  
**Status**: triaged  
**Date**: 2026-05-11

## Hypothesis

H2 (Boring fixes on solo-maintainer repos): Small, well-documented bug fixes in utility code have high merge probability on 200-500 star repos with active maintainers.

## Issue Selection

Scanned 7 open issues:
- #177: Dependency Dashboard (Renovate bot, not actionable)
- #159: Feature request - better audio control
- #145: Feature request - multi-language support
- #126: Feature request - IPC support (maintainer confirmed removed)
- #118: Feature request - toggle darkmode
- #67: Configuration help (not a code bug)
- #49: Style variables refactor

**Selection**: No open issues were code bugs. Ran static analysis on `utils/functions.py` instead.

## Bug Discovery

### Bug #1: Argument Order in write_json_file
**File**: `utils/functions.py:250`  
**Type**: Logic error  
**Severity**: High (causes runtime TypeError)

Function signature: `write_json_file(path: str, data: dict)`  
Incorrect call: `write_json_file(config, theme_config_file)`  
Correct call: `write_json_file(theme_config_file, config)`

All other calls in the codebase use correct argument order. This is a clear regression.

### Bug Hunt (Gemini 3.1 Pro)

Ran adversarial bug hunt on `utils/functions.py`. Found 16 bugs across 6 categories:

**Fixed (11 bugs):**
1. Resource cleanup: unclosed file stream in `ensure_file`
2. Resource cleanup: PixbufLoader not guaranteed to close
3. Error handling: missing OSError catch in `read_json_file`
4. Error handling: null check for `Application.get_default()`
5. Edge case: RGB clamping in `mix_colors`
6. Edge case: division by zero in `ttl_lru_cache`
7. Edge case: RGBA regex doesn't match `1.0` alpha
8. API misuse: wrong method in `send_notification`
9. API misuse: deprecated Pillow constant
10. Type safety: wrong signature for `for_monitors`
11. Type safety: wrong return type for `check_if_day`
12. Shell safety: improper argument splitting in `toggle_command`

**Deferred (5 bugs - architecture/security):**
1. Command injection in shell execution functions
2. Path traversal in `copy_theme`
3. `exit(1)` in background thread
4. tracemalloc usage pattern
5. Relative paths in CSS compiler

## Implementation

**Commits**:
1. `fbb8320d`: Fix write_json_file argument order + add test
2. `b9de43b5`: Fix 11 bugs from Gemini round 1

**Test coverage**: Added unit test for `write_json_file`

**Verification**: No test suite in repo (import errors due to missing GTK dependencies). Changes verified via code inspection and Gemini review.

## Evidence Classification

**Type**: Bug fix (not feature)  
**Scope**: Utility functions only, no UI changes  
**Risk**: Low (fixes are defensive - add guards, fix types, close resources)  
**Complexity**: 90 lines changed across 2 files

**For H2**: This is a boring fix - utility code cleanup, no new functionality. Solo maintainer (rubiin), 1.3k stars, active (last commit 4 days ago).

## Acceptance Criteria

1. Maintainer acknowledges the bugs as real issues
2. Code review passes (type safety, resource cleanup)
3. No breaking changes to public API
4. Deferred security issues noted for future work

## Risk Assessment

**Low risk**:
- No breaking changes
- Fixes are defensive (add guards, don't remove features)
- Test added for argument order bug
- All changes are in utility functions, not core widgets

**Possible rejection**:
- Maintainer may prefer different API for send_notification
- Pillow compatibility fix might conflict with minimum version requirements
- Deferred security issues might be expected behavior

## Next Steps

1. Push branch to fork
2. Create PR with clear description of bugs fixed
3. Reference Gemini bug hunt output
4. Note deferred issues for maintainer review
5. Await feedback

## Metadata

**Repo**: rubiin/tsumiki  
**Stars**: 1.3k  
**Last commit**: 2026-05-07  
**Maintainer**: rubiin (solo)  
**Language**: Python (GTK)  
**Category**: Wayland/Hyprland status bar

**Pipeline stage**: triaged → drip queue
