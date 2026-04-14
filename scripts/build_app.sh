#!/usr/bin/env bash
# Build AIM Flow.app using PyInstaller and the checked-in spec file.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -x ".venv/bin/python" ]]; then
  echo "Virtual environment not found. Run ./install.sh first."
  exit 1
fi

# Ensure the .icns file exists before building.
if [[ ! -f "assets/aim-flow.icns" ]]; then
  echo "Creating app icon..."
  bash scripts/create_icns.sh
fi

echo "Installing build dependencies..."
.venv/bin/pip install -r requirements-build.txt --quiet

echo "Building AIM Flow.app..."
rm -rf build dist
.venv/bin/pyinstaller --noconfirm "AIM Flow.spec"

echo ""
echo "Build complete: dist/AIM Flow.app"
echo ""
echo "To install, drag dist/AIM Flow.app to /Applications."
