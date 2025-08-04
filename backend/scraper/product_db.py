from firebase_admin import firestore, messaging
import re
from .sites import get_product_price_from_url

def format_discount_message(name, old_price, new_price, discount_percentage):
    title = f"🎉 {name} İndirimde!"
    body = f"Eski: {old_price} TL → Yeni: {new_price} TL (%{discount_percentage:.1f})"
    return title, body

def save_product_firestore(name, price, link, site="unknown", filters=None, user_id=None):
    db = firestore.client()
    print(f"[SAVE] Kullanıcı: {user_id}, Ürün: {name}, Fiyat: {price}")

    try:
        price_clean = price.replace("TL", "").replace("₺", "").strip()
        price_match = re.search(r'[\d.,]+', price_clean)
        if price_match:
            price_str = price_match.group()
            price_str = price_str.replace(".", "").replace(",", ".")
            price_clean = float(price_str)
        else:
            print(f"[ERROR] Fiyat parse edilemedi: {price}")
            return

    except Exception as e:
        print(f"[ERROR] Fiyat temizleme hatası: {e}")
        return

    try:
        existing_product = db.collection("products") \
            .where("link", "==", link) \
            .where("user_id", "==", user_id) \
            .limit(1).get()

        if existing_product:
            doc = existing_product[0]
            old_price = doc.get("current_price")

            if price_clean < old_price:
                discount_amount = old_price - price_clean
                discount_percentage = (discount_amount / old_price) * 100

                doc.reference.update({
                    "current_price": price_clean,
                    "old_price": old_price,
                    "last_updated": firestore.SERVER_TIMESTAMP,
                    "discount_detected": True,
                    "discount_amount": discount_amount,
                    "discount_percentage": discount_percentage
                })

                title, body = format_discount_message(name, old_price, price_clean, discount_percentage)
                send_notification_to_user(user_id, title, body)

                return True
            else:
                doc.reference.update({
                    "current_price": price_clean,
                    "last_updated": firestore.SERVER_TIMESTAMP,
                    "discount_detected": False
                })
        else:
            doc_ref = db.collection("products").add({
                "name": name,
                "current_price": price_clean,
                "initial_price": price_clean,
                "link": link,
                "site": site,
                "user_id": user_id,
                "filters": filters or {},
                "created_at": firestore.SERVER_TIMESTAMP,
                "last_updated": firestore.SERVER_TIMESTAMP,
                "discount_detected": False
            })
            print(f"[FIRESTORE] Yeni ürün eklendi: {doc_ref[1].id}")

    except Exception as e:
        print(f"[ERROR] Firestore kayıt hatası: {e}")

def get_tracked_products(user_id=None):
    db = firestore.client()
    query = db.collection("products")
    if user_id:
        query = query.where("user_id", "==", user_id)

    products = query.get()
    tracked_products = []

    for doc in products:
        data = doc.to_dict()
        data["id"] = doc.id
        tracked_products.append(data)

    return tracked_products

def send_notification_to_user(user_id, title, body):
    try:
        topic = f"user_{user_id}"
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            topic=topic
        )
        response = messaging.send(message)
        print(f"Bildirim gönderildi → {user_id}: {response}")
    except Exception as e:
        print(f"Bildirim gönderilemedi → {user_id}: {e}")

def check_price_changes():
    db = firestore.client()
    products = db.collection("products").get()

    updated_products = []
    for doc in products:
        product = doc.to_dict()
        product["id"] = doc.id

        try:
            print(f"[CHECK] {product['name']} ({product['user_id']}) kontrol ediliyor...")

            current_price_str = get_product_price_from_url(product['link'])
            if not current_price_str:
                continue

            price_clean = current_price_str.replace("TL", "").replace("₺", "").strip()
            price_match = re.search(r'[\d.,]+', price_clean)
            if price_match:
                price_str = price_match.group()
                price_str = price_str.replace(".", "").replace(",", ".")
                current_price = float(price_str)
            else:
                continue

            old_price = product.get("current_price", 0)

            if current_price < old_price:
                discount_amount = old_price - current_price
                discount_percentage = (discount_amount / old_price) * 100

                db.collection("products").document(product["id"]).update({
                    "current_price": current_price,
                    "old_price": old_price,
                    "last_updated": firestore.SERVER_TIMESTAMP,
                    "discount_detected": True,
                    "discount_amount": discount_amount,
                    "discount_percentage": discount_percentage
                })

                title, body = format_discount_message(product["name"], old_price, current_price, discount_percentage)
                send_notification_to_user(product["user_id"], title, body)

                updated_products.append({
                    **product,
                    "new_price": current_price,
                    "discount_amount": discount_amount,
                    "discount_percentage": discount_percentage
                })

            else:
                db.collection("products").document(product["id"]).update({
                    "current_price": current_price,
                    "last_updated": firestore.SERVER_TIMESTAMP,
                    "discount_detected": False
                })

        except Exception as e:
            print(f"[ERROR] {product['name']} kontrol edilirken hata: {e}")

    return updated_products
