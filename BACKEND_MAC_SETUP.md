# Run Django backend from your MacBook and connect mobile app

This guide automates starting the Django server on your MacBook and wiring the mobile app to use it on your local network for testing with an iPhone.

Steps (run these on your MacBook terminal inside the repo):

1) Find your Mac's local IP (Wi‑Fi):

```bash
# most Macs
ip=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1)
echo "Local IP: $ip"
```

2) Start the Django dev server bound to all interfaces so other devices can reach it:

```bash
# Activate your venv, then
/Users/golden/Documents/GitHub/study_buddy_project/venv/bin/python manage.py runserver 0.0.0.0:8000
```

3) Allow incoming connections on port 8000 (macOS firewall off or allow incoming for Python/Xcode). If you use the built-in firewall, add an exception in System Settings → Firewall.

4) Point the mobile app to your Mac's IP. Quick automated helper (runs locally):

```bash
./scripts/set_mobile_backend.sh
# supply IP optionally: ./scripts/set_mobile_backend.sh 192.168.1.42
```

This script will replace the `BACKEND_URL` value inside `mobile/src/api.js` with `http://<your-ip>:8000`.

5) Start Expo and open on your iPhone (same Wi‑Fi) or use Tunnel:

```bash
cd mobile
npm install
npx expo start
```

6) Test endpoint from your phone: open `http://<your-ip>:8000/api/subjects/` in the device browser — should return JSON.

Notes
- For Google OAuth sign-in on device, you may need to use a domain (e.g., `goldenkalala.com`) and configure DNS or use ngrok to expose localhost over HTTPS. Expo Auth with Google sometimes requires https redirect URIs.
- Using IP (http) is fine for many API calls but OAuth providers may require HTTPS and exact redirect URIs.
