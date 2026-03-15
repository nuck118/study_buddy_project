Xcode setup and local archive

Steps to get the iOS project ready and produce a development-signed .ipa locally:

1. Install prerequisites

```bash
# Install Homebrew (if missing): https://brew.sh
brew install cocoapods watchman
sudo gem install cocoapods -v 1.16.2 || true
```

2. Generate native iOS project and install pods

```bash
cd mobile
npx expo prebuild --clean
cd ios
pod install --repo-update --verbose
```

3. Open workspace in Xcode and set your Team (Signing & Capabilities) for the StudyBuddyMobile target, or use the `TEAM_ID` env var when running the archive script.

4. Archive and export (example):

```bash
cd mobile
TEAM_ID=YOUR_TEAM_ID ./scripts/xcode_archive.sh
```

If you prefer GUI: open `mobile/ios/StudyBuddyMobile.xcworkspace` in Xcode, select the generic device or target device, Product → Archive, then export.

If `pod install` still fails, paste the verbose output here and I will iterate.
