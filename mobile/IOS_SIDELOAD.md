# iOS Sideload Checklist (Xcode)

Follow these steps on your Mac to build and install the app directly to your iPhone (free Apple ID works but the app expires after 7 days).

1) Install node deps

```bash
cd mobile
npm install
```

2) Generate native Xcode project

```bash
npx expo prebuild
```

This creates `ios/` and `android/` folders. If you need native modules, add them before prebuild.

3) Open workspace in Xcode

```bash
cd ios
open *.xcworkspace
```

4) Xcode configuration
- Connect your iPhone to the Mac.
- Select your physical device as run target.
- In the project `Signing & Capabilities`: set `Team` to your Apple ID (Xcode will manage provisioning).
- Ensure `Bundle Identifier` matches `mobile/app.json` (`com.goldenkalala.studybuddy`).

5) Build & Run
- Click the Run ▶️ button in Xcode. The app will be installed on the device.

6) Trust the developer (if needed)
- On the device: Settings → General → VPN & Device Management → Trust the Apple ID used to sign the app.

7) Notes & tips
- Free Apple ID: provisioning lasts 7 days and you must re‑sign every 7 days.
- To distribute to other testers long‑term, join Apple Developer Program and use TestFlight or EAS build + App Store Connect.
- If you run into signing errors, open the Signing panel, click `Automatically manage signing`, and let Xcode create a provisioning profile.

8) Troubleshooting
- If you get entitlement/capability errors, add the matching capability in Xcode (e.g., Push Notifications, Keychain).
- If build fails due to dependencies, run `pod install` inside `ios/` and reopen the workspace:

```bash
cd ios
pod install --repo-update
open *.xcworkspace
```

9) Rebuilding after JS changes
- For most JS changes you can keep using Expo Dev Server and Expo Go. For native code changes, run `npx expo prebuild` again and rebuild in Xcode.

---

If you want, I can also: create an `App.entitlements` example, or generate an `eas.json` tailored to TestFlight builds. Which would you like next? 
