import sys
import os
# Projenin kök dizinini path'e ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import re
from firebase_admin import firestore
from push_sender import send_notification, init_firebase
from scraper.sites import get_product_price_from_url

# Terminal argümanı ile test modu aktif edilir
TEST_MODE = "--test" in sys.argv

def format_discount_message(name, old_price, new_price, discount_percentage):
    title = f"🎉 {name} İndirimde!"
    body = f"Eski: {old_price:.2f} TL → Yeni: {new_price:.2f} TL (%{discount_percentage:.1f} indirim)"
    return title, body

def check_price_changes():
    if not init_firebase():
        print("Firebase başlatılamadı. Çıkılıyor.")
        return

    db = firestore.client()
    products = db.collection("products").get()

    for doc in products:
        product = doc.to_dict()
        doc_id = doc.id

        try:
            print(f"[CHECK] {product['name']} kontrol ediliyor...")

            if TEST_MODE:
                # DEMO modu: yapay olarak fiyat düşür
                current_price = max(1.0, product.get("current_price", 100) - 20)
                print(f"[TEST MODE] Simüle edilen fiyat: {current_price}")
            else:
                # Gerçek fiyat çek
                current_price_str = get_product_price_from_url(product['link'])
                if not current_price_str:
                    print("[WARN] Fiyat çekilemedi, atlanıyor.")
                    continue

                # String fiyatı float'a dönüştür
                price_clean = current_price_str.replace("TL", "").replace("₺", "").strip()
                match = re.search(r'[\d.,]+', price_clean)
                if not match:
                    print("[WARN] Fiyat parse edilemedi, atlanıyor.")
                    continue

                price_str = match.group().replace(".", "").replace(",", ".")
                current_price = float(price_str)

            old_price = product.get("current_price", 0)

            if current_price < old_price:
                discount_amount = old_price - current_price
                discount_percentage = (discount_amount / old_price) * 100

                # Firestore güncelle
                db.collection("products").document(doc_id).update({
                    "current_price": current_price,
                    "old_price": old_price,
                    "last_updated": firestore.SERVER_TIMESTAMP,
                    "discount_detected": True,
                    "discount_amount": discount_amount,
                    "discount_percentage": discount_percentage
                })

                # Bildirim oluştur
                title, body = format_discount_message(product["name"], old_price, current_price, discount_percentage)

                # Kullanıcı topic'ine bildirim gönder
                topic = f"user_{product['user_id']}"
                send_notification(title, body, topic=topic)

                print(f"[SUCCESS] {product['name']} için indirim bildirimi gönderildi.")
            else:
                # İndirim yok, sadece güncelle
                db.collection("products").document(doc_id).update({
                    "current_price": current_price,
                    "last_updated": firestore.SERVER_TIMESTAMP,
                    "discount_detected": False
                })

                print(f"[OK] {product['name']} için fiyat değişimi yok.")

        except Exception as e:
            print(f"[ERROR] {product['name']} kontrol edilirken hata: {e}")

if __name__ == "__main__":
    check_price_changes()
