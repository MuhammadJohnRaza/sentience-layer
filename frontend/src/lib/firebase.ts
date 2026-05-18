import { initializeApp, getApp, getApps } from "firebase/app";
import { getAnalytics, Analytics } from "firebase/analytics";

const firebaseConfig = {
  apiKey: "AIzaSyB8ahyGxaecr107I7r6wGS3E7UwC2uRn8Y",
  authDomain: "sentenceproject-496712.firebaseapp.com",
  projectId: "sentenceproject-496712",
  storageBucket: "sentenceproject-496712.firebasestorage.app",
  messagingSenderId: "367781661404",
  appId: "1:367781661404:web:14883afb1ce8095c684219",
  measurementId: "G-HT9XKYBVVN"
};

// Initialize Firebase
const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApp();

let analytics: Analytics | undefined;
if (typeof window !== "undefined") {
  analytics = getAnalytics(app);
}

export { app, analytics };
