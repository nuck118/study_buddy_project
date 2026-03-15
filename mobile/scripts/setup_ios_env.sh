#!/usr/bin/env bash
set -euo pipefail

echo "Setup iOS environment for StudyBuddy mobile"

if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew not found. Install Homebrew first: https://brew.sh" >&2
  exit 1
fi

echo "Installing/updating CocoaPods and Watchman via Homebrew..."
brew install cocoapods || brew reinstall cocoapods || true
brew install watchman || true

echo "Increasing file descriptor limit for this shell (may not persist across sessions)..."
ulimit -n 10240 || true

if ! command -v node >/dev/null 2>&1; then
  echo "Node.js not found. Install Node (recommended via nvm or Homebrew)" >&2
  exit 1
fi

if ! command -v npx >/dev/null 2>&1; then
  echo "npx not available. Ensure npm is installed alongside Node." >&2
  exit 1
fi

echo "Running Expo prebuild (will recreate ios/android dirs)..."
npx expo prebuild --clean

echo "Running CocoaPods install in ios/"
cd ios
pod install --repo-update --verbose

echo "Done. If pod install failed, paste the output here for further diagnosis."
