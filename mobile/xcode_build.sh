#!/usr/bin/env bash
set -euo pipefail

# Usage: ./xcode_build.sh [scheme] [workspace-or-project-path] [export-method]
# Example: ./xcode_build.sh StudyBuddy ios/StudyBuddy.xcworkspace development
# Defaults:
#  - scheme: read from app.json slug (StudyBuddy)
#  - workspace: ios/*.xcworkspace
#  - export-method: development (choices: development, ad-hoc, app-store, enterprise)

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MOBILE_DIR="$REPO_ROOT/mobile"

SCHEME=${1:-}
WORKSPACE_PATH=${2:-}
EXPORT_METHOD=${3:-development}

if [ -z "$SCHEME" ]; then
  # try to infer scheme from app.json name/slug
  SCHEME=$(node -e "console.log(require('./mobile/app.json').expo.slug || require('./mobile/app.json').expo.name)") || true
fi

if [ -z "$WORKSPACE_PATH" ]; then
  # find workspace
  cd "$MOBILE_DIR/ios"
  WORKSPACE_PATH=$(ls *.xcworkspace 2>/dev/null | head -n1 || true)
  if [ -n "$WORKSPACE_PATH" ]; then
    WORKSPACE_PATH="$MOBILE_DIR/ios/$WORKSPACE_PATH"
  else
    # fallback to project.xcodeproj
    PROJ=$(ls *.xcodeproj 2>/dev/null | head -n1 || true)
    if [ -n "$PROJ" ]; then
      WORKSPACE_PATH="$MOBILE_DIR/ios/$PROJ"
    fi
  fi
fi

if [ -z "$WORKSPACE_PATH" ]; then
  echo "Could not find workspace or project in mobile/ios. Run 'npx expo prebuild' first." >&2
  exit 1
fi

ARCHIVE_PATH="/tmp/${SCHEME}.xcarchive"
EXPORT_DIR="$MOBILE_DIR/build"
mkdir -p "$EXPORT_DIR"

echo "Scheme: $SCHEME"
echo "Workspace/Project: $WORKSPACE_PATH"
echo "Export method: $EXPORT_METHOD"
echo "Archive path: $ARCHIVE_PATH"
echo "Export dir: $EXPORT_DIR"

echo "Archiving..."
xcodebuild -workspace "$WORKSPACE_PATH" -scheme "$SCHEME" -configuration Release -archivePath "$ARCHIVE_PATH" archive | sed -u 's/^/xcodebuild: /'

echo "Exporting .ipa..."
xcodebuild -exportArchive -archivePath "$ARCHIVE_PATH" -exportOptionsPlist "$MOBILE_DIR/exportOptions.plist" -exportPath "$EXPORT_DIR" -allowProvisioningUpdates | sed -u 's/^/xcodebuild: /'

IPA_FILE="$(ls $EXPORT_DIR/*.ipa 2>/dev/null | head -n1 || true)"
if [ -z "$IPA_FILE" ]; then
  echo "Export failed: no .ipa found in $EXPORT_DIR" >&2
  exit 1
fi

echo "Exported .ipa: $IPA_FILE"
echo "You can install it using Apple Configurator or upload to App Store Connect / TestFlight."
