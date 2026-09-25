#!/usr/bin/env bash
# Package the Stream Prep Premiere plugin as a .ccx and optionally install it.
#   build.sh            -> writes dist/stream-prep.ccx
#   build.sh --install  -> also installs it with Adobe's Unified Plugin Installer Agent
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
dist="$here/dist"
stage="$(mktemp -d)"
trap 'rm -rf "$stage"' EXIT

# The .ccx must hold the plugin inside a single top-level folder.
mkdir -p "$stage/stream-prep" "$dist"
cp "$here/manifest.json" "$here/index.js" "$stage/stream-prep/"
find "$stage" -type d -exec chmod 755 {} +
find "$stage" -type f -exec chmod 644 {} +
rm -f "$dist/stream-prep.ccx"
(cd "$stage" && zip -qrX "$dist/stream-prep.ccx" stream-prep)
echo "built $dist/stream-prep.ccx"

if [ "${1:-}" = "--install" ]; then
  upia="/Library/Application Support/Adobe/Adobe Desktop Common/RemoteComponents/UPI/UnifiedPluginInstallerAgent/UnifiedPluginInstallerAgent.app/Contents/MacOS/UnifiedPluginInstallerAgent"
  # --install doesn't replace an existing copy, so remove any old one first.
  "$upia" --remove "Stream Prep" >/dev/null 2>&1 || true
  "$upia" --install "$dist/stream-prep.ccx"
fi
