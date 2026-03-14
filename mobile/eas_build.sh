#!/usr/bin/env bash
set -euo pipefail

# Simple wrapper to start an EAS iOS build and optionally submit to App Store Connect
# Requires: eas-cli installed and you are logged in (`npm install -g eas-cli; eas login`)
# Usage: ./eas_build.sh [profile] [submit]
# Example: ./eas_build.sh production submit

PROFILE=${1:-production}
SUBMIT=${2:-}

echo "Starting EAS build with profile: $PROFILE"
cd "$(cd "$(dirname "$0")" && pwd)"
eas build -p ios --profile "$PROFILE"

if [ "$SUBMIT" = "submit" ]; then
  echo "Submitting last iOS build to App Store Connect (TestFlight)..."
  eas submit -p ios --profile "$PROFILE"
fi
