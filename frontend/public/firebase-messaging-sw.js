import { initializeApp } from "firebase/app";
import { getMessaging, getToken, onMessage } from "firebase/messaging";

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
const messaging = getMessaging(app);

export async function subscribeToNotifications(userId) {
  try {
    const token = await getToken(messaging, {
      vapidKey: "BIOy4b7RiU0G3VxK2LmhaPDOtn3zwQSZrDHN5QX4klolPm0jl1zyyYIdLKO-8DxS_FnQjBZ6dU8CElDVVYMf6sA" 
    });

    if (token) {
      console.log("🔥 Token alındı:", token);

      // Backend'e token ve userId gönder
      await fetch("/api/subscribe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token, userId })
      });

      console.log("✅ Kullanıcı backend'e gönderildi.");
    } else {
      console.warn("🚫 Token alınamadı. Bildirim izni verilmedi.");
    }
  } catch (error) {
    console.error("❌ Bildirim aboneliği hatası:", error);
  }
}

// Aktif ön yüzde bildirim geldiğinde
onMessage(messaging, (payload) => {
  console.log("🎯 Anlık mesaj geldi:", payload);
  // buraya toast gösterimi vs. ekleyebilirsin
});
