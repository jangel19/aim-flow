#!/usr/bin/env bash
# Convert status_logo.png to a macOS .icns file using sips and iconutil.
# Output: assets/aim-flow.icns
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE="$ROOT_DIR/status_logo.png"
ICONSET="$ROOT_DIR/assets/aim-flow.iconset"
OUTPUT="$ROOT_DIR/assets/aim-flow.icns"

if [[ ! -f "$SOURCE" ]]; then
  echo "Source image not found: $SOURCE"
  exit 1
fi

rm -rf "$ICONSET"
mkdir -p "$ICONSET"

for size in 16 32 64 128 256 512; do
  sips -z "$size" "$size" "$SOURCE" --out "$ICONSET/icon_${size}x${size}.png"    >/dev/null 2>&1
  double=$((size * 2))
  sips -z "$double" "$double" "$SOURCE" --out "$ICONSET/icon_${size}x${size}@2x.png" >/dev/null 2>&1
done

iconutil -c icns "$ICONSET" -o "$OUTPUT"
rm -rf "$ICONSET"

echo "Created $OUTPUT"
