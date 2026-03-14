#!/usr/bin/env bash
set -euo pipefail

# Run from the mobile/ directory locally to generate native ios/android projects
# Requires: npm, npx, expo-cli installed locally

echo "Installing node deps (run this locally)..."
npm install

echo "Running expo prebuild to generate native projects..."
npx expo prebuild --clean

echo "Done. Open ios/*.xcworkspace in Xcode to sideload onto a device."
