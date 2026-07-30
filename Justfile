# justfile

# Command to freeze current pip packages to requirements.txt
freeze:
    pip freeze > requirements.txt

doc_gen:
    python doc_gen.py

docs-dev:
    cd docs && pnpm dev

restore_config:
    cp config.toml.bak config.toml

stubs_gen:
    fabric-cli gs GtkLayerShell-0.1 Playerctl-2.0 NM-1.0
