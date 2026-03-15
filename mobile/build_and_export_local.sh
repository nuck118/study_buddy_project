#!/usr/bin/env bash
set -euo pipefail

# Automated local build + export script for iOS .ipa
# Usage: ./build_and_export_local.sh [SCHEME]
# The script will:
#  - check for node/npm/npx and CocoaPods
#  - run npm install
#  - run npx expo prebuild --clean
#  - run pod install
#  - archive and export .ipa using xcodebuild and exportOptions.plist

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
MOBILE_DIR="$ROOT_DIR"

SCHEME=${1:-}

echo "Starting local build/export (mobile directory: $MOBILE_DIR)"

command_exists() { command -v "$1" >/dev/null 2>&1; }

if ! command_exists node || ! command_exists npm || ! command_exists npx; then
  echo "Error: node/npm/npx not found. Please install Node (recommended via Homebrew or nvm):"
  echo "  brew install node"
  echo "  or use nvm: https://github.com/nvm-sh/nvm"
  exit 1
fi

if ! command_exists pod; then
  echo "CocoaPods (pod) not found. Install via Homebrew: brew install cocoapods" 
  echo "or: sudo gem install cocoapods"
  exit 1
fi

cd "$MOBILE_DIR"

echo "Installing JS dependencies..."
npm install

echo "Running expo prebuild..."
npx expo prebuild --clean

echo "Installing CocoaPods dependencies..."
cd ios
pod install --repo-update
cd ..

# Infer scheme if not provided
if [ -z "$SCHEME" ]; then
  echo "Inferring scheme from app.json..."
  SCHEME=$(python3 - <<PY
import json,sys
f='app.json'
try:
    j=json.load(open(f))
    slug=j.get('expo',{}).get('slug') or j.get('expo',{}).get('name')
    print(slug)
except Exception as e:
    sys.exit(1)
PY
)
  if [ -z "$SCHEME" ]; then
    echo "Could not infer scheme. Please pass SCHEME as first arg." >&2
    exit 1
  fi
fi

echo "Using scheme: $SCHEME"

# Find workspace or project
cd ios
WORKSPACE="$(ls *.xcworkspace 2>/dev/null | head -n1 || true)"
if [ -n "$WORKSPACE" ]; then
  WORKSPACE_PATH="$PWD/$WORKSPACE"
else
  PROJ="$(ls *.xcodeproj 2>/dev/null | head -n1 || true)"
  if [ -n "$PROJ" ]; then
    WORKSPACE_PATH="$PWD/$PROJ"
  else
    echo "No .xcworkspace or .xcodeproj found in ios/. Did prebuild succeed?" >&2
    exit 1
  fi
fi

ARCHIVE_PATH="/tmp/${SCHEME}.xcarchive"
EXPORT_DIR="$MOBILE_DIR/build"
mkdir -p "$EXPORT_DIR"

echo "Archiving scheme $SCHEME..."
xcodebuild -workspace "$WORKSPACE_PATH" -scheme "$SCHEME" -configuration Release -archivePath "$ARCHIVE_PATH" archive | sed -u 's/^/xcodebuild: /'

echo "Exporting .ipa..."
xcodebuild -exportArchive -archivePath "$ARCHIVE_PATH" -exportOptionsPlist "$MOBILE_DIR/exportOptions.plist" -exportPath "$EXPORT_DIR" -allowProvisioningUpdates | sed -u 's/^/xcodebuild: /'

IPA_FILE="$(ls $EXPORT_DIR/*.ipa 2>/dev/null | head -n1 || true)"
if [ -z "$IPA_FILE" ]; then
  echo "Export failed: no .ipa found in $EXPORT_DIR" >&2
  exit 1
fi

echo "Exported .ipa: $IPA_FILE"
echo "Done. Install via Apple Configurator or upload to App Store Connect / TestFlight."
