# justfile

# Command to freeze current pip packages to requirements.txt
freeze:
    pip freeze > requirements.txt

doc_gen:
    python doc_gen.py

restore_config:
    cp config.toml.bak config.toml
    cp theme.toml.bak theme.toml

stubs_gen:
    fabric-cli gs Glace-0.1 GtkLayerShell-0.1 Playerctl-2.0 NM-1.0
