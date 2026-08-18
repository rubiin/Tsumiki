# justfile

# Regenerate the uv lockfile from pyproject.toml
lock:
    uv lock

# Run the test suite
test:
    python3 -m unittest discover tests -q

doc_gen:
    python doc_gen.py

docs-dev:
    cd docs && pnpm dev

docs-build:
    cd docs && pnpm build

docs-lint:
    cd docs && pnpm lint

docs-lint-fix:
    cd docs && pnpm lint:fix

docs-fmt:
    cd docs && pnpm fmt

docs-fmt-check:
    cd docs && pnpm fmt:check

restore_config:
    cp config.toml.bak config.toml

stubs_gen:
    fabric-cli gs GtkLayerShell-0.1 Playerctl-2.0 NM-1.0
