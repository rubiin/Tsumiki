#!/bin/bash

# Language argument (default to eng)
LANG="${1:-eng}"

# Optional slurp arguments
SLURP_ARGS="${2:-}"

# Temporary file name
TMP_IMG="tmp.png"

# Select area with slurp and capture with grim
grim -g "$(slurp "$SLURP_ARGS")" "$TMP_IMG" && \
tesseract -l "$LANG" "$TMP_IMG" - | wl-copy

if [ -f "${TMP_IMG}" ]; then
    notify-send -a "Hydepanel" "OCR Success" "Text Copied to Clipboard (${LANG})"
else
    notify-send -a "Hydepanel" "OCR Aborted"
fi
rm "$TMP_IMG"
