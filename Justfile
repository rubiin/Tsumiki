# justfile

# Command to freeze current pip packages to requirements.txt
freeze:
    pip freeze > requirements.txt

doc_gen:
    python doc_gen.py

restore_config:
    cp config.json.bak config.json

stubs_gen:
    gengir Glace-0.1 Gray-0.1 GtkLayerShell-0.1 Playerctl-2.0 NM-1.0
