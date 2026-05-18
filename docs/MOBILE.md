# 📱 Mobile & Multi-Platform Deployment Guide

This guide details the architecture of the **Sentience Layer Mobile Application** (located in the [mobile/](file:///c:/Users/catac/OneDrive/Desktop/sentience-layer/mobile) directory) and provides step-by-step instructions on running it locally, compiling static Next.js exports, synchronizing Capacitor bridges for Android/iOS, and deploying the mobile dashboard to Firebase Hosting.

---

## 🏛️ Mobile Architecture Overview

The Sentience mobile app is a responsive dashboard tailored for cognitive monitoring, real-time agent telemetry, and interaction on mobile screens.

- **Frontend Core**: Built with **Next.js 14**, React 18, and Tailwind CSS.
- **State Management**: **Zustand** store with persistence for user preferences, including the new **Verbosity Prefs** (Brief, Default, Detailed).
- **Mobile Bridge**: **CapacitorJS (v8)** acts as a native wrapper to package the Next.js static build into native iOS and Android binaries.
- **Hosting**: Deployed globally to **Firebase Hosting** for rapid loading times and static asset delivery.

---

## 🚀 Local Development

### 1. Installation
Navigate to the mobile directory and install all required dependencies:
```bash
cd mobile
npm install
```

### 2. Running in Dev Mode
To launch the Next.js development server with hot-reload support:
```bash
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) to view the interface in your browser.

---

## 🛠️ Capacitor Native Compilation

Capacitor bridges the web application with native mobile frameworks (Android Studio for Android, Xcode for iOS).

### 1. Prerequisites
- **Android**: Install [Android Studio](https://developer.android.com/studio) and configure the Android SDK.
- **iOS**: Install [Xcode](https://developer.apple.com/xcode/) (requires a macOS machine).

### 2. Building the Web Application
Before running Capacitor commands, you must compile a production static export of the Next.js app:
```bash
npm run build
```
This outputs a fully optimized static website in the `out/` directory.

### 3. Synchronizing Capacitor Bridges
Sync the compiled web assets into the native native projects:
```bash
# Sync web assets to both Android and iOS projects
npx cap sync
```

### 4. Running the Native Projects

#### Android
Open the project in Android Studio to build, emulate, or run on physical devices:
```bash
npx cap open android
```
Inside Android Studio, select your target device and click **Run**.

#### iOS
Open the project in Xcode (macOS only) to run in the simulator or deploy to an iPhone:
```bash
npx cap open ios
```
Inside Xcode, select your simulator and click the **Play** button.

---

## 🔥 Firebase Hosting Deployment

We have configured automated scripts to build the Next.js static export and deploy the directory seamlessly to Firebase.

### 1. Initialize Firebase CLI
Make sure you are logged into Firebase:
```bash
npx firebase login
```

### 2. Configure Firebase in Mobile Directory
If you need to re-initialize your hosting project configuration:
```bash
npx firebase init hosting
```
- Select your target Firebase project.
- Specify the public directory as `out` (since Next.js builds static files there).
- Configure as a single-page app (write `y` to rewrite all URLs to `/index.html`).
- Set up automatic builds and deploys with GitHub Actions (optional).

### 3. Automated One-Command Build & Deploy
We added automated scripts to the mobile package:
```bash
npm run firebase:deploy
```
This command runs:
1. `next build` (Next.js compilation, outputting files to the `out/` directory).
2. `firebase deploy --only hosting` (uploads the static bundle to Firebase Hosting servers).

Once completed, the CLI will output the live URL of your deployed mobile cognitive dashboard.
