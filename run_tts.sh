#!/usr/bin/env bash
set -euo pipefail

DEFAULT_TEXT="Hello! I am Astrid, running locally. What would you like to talk about?"
DEFAULT_VOICE="af_bella"
DEFAULT_SPEED="1"
DEFAULT_OUTPUT="astrid-tts-test.mp3"

prompt_with_default() {
  local prompt="$1"
  local default="$2"
  local value

  read -r -p "$prompt [$default]: " value
  printf '%s' "${value:-$default}"
}

echo "Astrid TTS"
echo "Press Enter to use each default."
echo

TEXT="$(prompt_with_default "Text" "$DEFAULT_TEXT")"
VOICE="$(prompt_with_default "Voice" "$DEFAULT_VOICE")"
SPEED="$(prompt_with_default "Speed" "$DEFAULT_SPEED")"
OUTPUT="$(prompt_with_default "Export location" "$DEFAULT_OUTPUT")"

echo
uv run python tts_test.py \
  --text "$TEXT" \
  --voice "$VOICE" \
  --speed "$SPEED" \
  --output "$OUTPUT"
