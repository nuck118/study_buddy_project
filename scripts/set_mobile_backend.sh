#!/usr/bin/env bash
set -euo pipefail

# Usage: ./set_mobile_backend.sh [IP]
# If IP not provided, auto-detect common Wi-Fi interface IPs (en0, en1)

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MOBILE_API_FILE="$REPO_ROOT/mobile/src/api.js"

if [ $# -ge 1 ]; then
  IP="$1"
else
  IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "127.0.0.1")
fi

if [ -z "$IP" ]; then
  echo "Could not detect local IP. Please pass it as argument." >&2
  exit 1
fi

URL="http://$IP:8000"
echo "Setting mobile backend URL to: $URL"

if [ ! -f "$MOBILE_API_FILE" ]; then
  echo "File not found: $MOBILE_API_FILE" >&2
  exit 1
fi

# Replace BACKEND_URL default in api.js
python3 - <<PY
from pathlib import Path
f = Path(r'''$MOBILE_API_FILE''')
s = f.read_text()
s_new = s.replace("'http://localhost:8000'", "'${URL}'")
if s==s_new:
    print('No change made (placeholder not found).')
else:
    f.write_text(s_new)
    print('Updated mobile/src/api.js with backend URL.')
PY

echo "Done. Run the mobile app (npm install then npx expo start) and connect via Expo Go."
