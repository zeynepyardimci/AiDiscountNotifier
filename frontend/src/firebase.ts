import { initializeApp } from "firebase/app";
import { getMessaging } from "firebase/messaging";

const firebaseConfig = {
    apiKey: "AIzaSyBg7eFF55J1XQm1EC4JiuzZ27KRzM5KfMY",
    authDomain: "ai-discount-notifier-main.firebaseapp.com",
    projectId: "ai-discount-notifier-main",
    storageBucket: "ai-discount-notifier-main.firebasestorage.app",
    messagingSenderId: "1052112269117",
    appId: "1:1052112269117:web:10c98f8d39543f3ee21f54",
    measurementId: "G-RRJECM3CMB"
};

const app = initializeApp(firebaseConfig);
export const messaging = getMessaging(app);
