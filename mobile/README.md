StudyBuddy Mobile (Expo)

Quick start

1. Install dependencies:

```bash
cd mobile
npm install
# or: yarn
```

2. Set environment variables / replace placeholders:
- Replace `<YOUR_GOOGLE_CLIENT_ID>` in `App.js` or set `GOOGLE_CLIENT_ID` in your env.
- Replace `<YOUR_BACKEND_URL>` with your Django server URL (e.g. `http://192.168.1.5:8000`).

3. Run the app:

```bash
npx expo start
```

Notes
- This example uses `expo-auth-session` to obtain a Google ID token, then POSTs it to the backend endpoint `/api/auth/google/` which you already added.
- Implement secure token storage (e.g., `expo-secure-store`) before storing JWTs in production.
- You will need to configure OAuth credentials (Google Console) and add the correct redirect URIs for Expo.
