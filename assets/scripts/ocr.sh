#!/bin/bash

NOTIFY=true
OCR_LANG="eng"

# --- Parse Flags ---
while [[ $# -gt 0 ]]; do
    case "$1" in
        --no-notify)
            NOTIFY=false
            shift
            ;;
        --lang)
            OCR_LANG="${2:-eng}"
            shift 2
            ;;
        *)
            echo "Usage: $0 [--no-notify] [--lang <tesseract_lang>]"
            exit 1
            ;;
    esac
done

# --- Check Dependencies ---
for cmd in grimblast tesseract wl-copy notify-send; do
    if ! command -v "$cmd" &>/dev/null; then
        $NOTIFY && notify-send "OCR Tool" "Missing dependency: $cmd"
        echo "Missing dependency: $cmd"
        exit 1
    fi
done

# --- Run OCR ---
ocr_text=$(grimblast --freeze save area - | tesseract -l "$OCR_LANG" - - 2>/dev/null || true)

# --- Output / Notification ---
if [[ -n "$ocr_text" ]]; then
    echo -n "$ocr_text" | wl-copy
    $NOTIFY && notify-send -a "Tsumiki" "OCR Success" "Text Copied to Clipboard"
else
    $NOTIFY && notify-send -a "Tsumiki" "OCR Failed" "No text recognized or operation failed"
fi
