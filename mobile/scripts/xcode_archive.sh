#!/usr/bin/env bash
set -euo pipefail

# xcode_archive.sh
# Usage:
#  TEAM_ID=YOUR_TEAM_ID ./xcode_archive.sh [scheme]
# If TEAM_ID not provided, Xcode will prompt for signing in GUI.

WORKSPACE="ios/StudyBuddyMobile.xcworkspace"
SCHEME=${1:-StudyBuddyMobile}
CONFIG=${CONFIG:-Release}
ARCHIVE_PATH="$(pwd)/ios/build/${SCHEME}.xcarchive"
EXPORT_PATH="$(pwd)/ios/build/export"

if [ ! -f "$WORKSPACE" ]; then
  echo "Workspace not found at $WORKSPACE. Run ./scripts/setup_ios_env.sh first to generate ios project." >&2
  exit 1
fi

echo "Cleaning previous build artifacts..."
rm -rf "ios/build"
mkdir -p "ios/build"

echo "Running pod install..."
(cd ios && pod install --repo-update)

echo "Archiving scheme $SCHEME..."
BUILD_CMD=(xcodebuild -workspace "$WORKSPACE" -scheme "$SCHEME" -configuration "$CONFIG" -archivePath "$ARCHIVE_PATH" archive)

if [ -n "${TEAM_ID:-}" ]; then
  BUILD_CMD+=(CODE_SIGN_IDENTITY="-" DEVELOPMENT_TEAM="$TEAM_ID" CODE_SIGN_STYLE=Automatic)
fi

"${BUILD_CMD[@]}"

echo "Exporting archive to $EXPORT_PATH..."
mkdir -p "$EXPORT_PATH"

if [ -f ios/exportOptions.plist ]; then
  xcodebuild -exportArchive -archivePath "$ARCHIVE_PATH" -exportPath "$EXPORT_PATH" -exportOptionsPlist ios/exportOptions.plist
else
  echo "exportOptions.plist not found; exporting with automatic signing (may require GUI)."
  xcodebuild -exportArchive -archivePath "$ARCHIVE_PATH" -exportPath "$EXPORT_PATH" -allowProvisioningUpdates
fi

echo "Archive and export complete. Find .ipa in $EXPORT_PATH"
