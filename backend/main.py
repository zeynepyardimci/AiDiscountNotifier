from scraper.sites import search_hepsiburada, search_all_sites
from notifications.push_sender import init_firebase
from scraper.product_db import save_product_firestore, get_tracked_products, check_price_changes
from backend.gemini.parse_user_input import parse_product_description
import time
import schedule

def add_product_to_track_from_text(user_input, site="hepsiburada"):
    print(f"🔍 Kullanıcı girdisi parse ediliyor: {user_input}")
    
    # 1- Gemini API ile parse et (json filtre oluştur)
    filters = parse_product_description(user_input)
    if not filters:
        print("❌ Ürün açıklaması parse edilemedi.")
        return
    
    print(f"✅ Parse sonucu filtreler: {filters}")

    # 2- Siteye göre arama yap
    if site == "hepsiburada":
        results = search_hepsiburada(filters.get("category", ""),
                                    brand=filters.get("brand"),
                                    color=filters.get("color"),
                                    size=filters.get("size"))
    else:
        results = search_all_sites(filters)
    
    if not results:
        print("❌ Hiç ürün bulunamadı.")
        return
    
    print(f"✅ {len(results)} ürün bulundu ve takip listesine eklendi:")
    
    # 3- Bulunan ürünleri kaydet
    for product in results:
        print(f"  📦 {product['name']}: {product['price']}")
        try:
            save_product_firestore(
                product["name"], 
                product["price"], 
                product["link"], 
                site=product.get("site", site)
            )
        except Exception as e:
            print(f"  ❌ Ürün kaydedilirken hata: {e}")

def check_all_tracked_products():
    print("🔍 Takip edilen ürünlerin fiyatları kontrol ediliyor...")
    updated_products = check_price_changes()
    if updated_products:
        print(f"🎉 {len(updated_products)} üründe indirim tespit edildi!")
        for product in updated_products:
            print(f"  📦 {product['name']}: %{product['discount_percentage']:.1f} indirim")
    else:
        print("📊 Hiç indirim tespit edilmedi.")

def show_tracked_products():
    products = get_tracked_products()
    if not products:
        print("📝 Takip edilen ürün bulunmuyor.")
        return
    print(f"📋 Takip edilen {len(products)} ürün:")
    print("=" * 60)
    for i, product in enumerate(products, 1):
        print(f"{i}. {product['name']}")
        print(f"   💰 Fiyat: {product.get('current_price', product.get('price', 'Bilinmiyor'))} TL")
        print(f"   🌐 Site: {product.get('site', 'Bilinmiyor')}")
        print(f"   🔗 Link: {product['link']}")
        if product.get('discount_detected'):
            print(f"   🎉 Son indirim: %{product.get('discount_percentage', 0):.1f}")
        print()

def main():
    if not init_firebase():
        print("Firebase başlatılamadı. Uygulama devam ediyor...")
    print("🚀 İndirim Takip Sistemi Başlatıldı!")
    print("=" * 50)
    
    # Kullanıcıdan gelen açıklama örneği
    user_input = "Siyah uzun kadın etek"
    
    # Arama + takip başlat
    add_product_to_track_from_text(user_input, site="lcwaikiki")
    
    # Takip edilen ürünleri göster
    show_tracked_products()
    
    # Fiyat kontrolü yap
    check_all_tracked_products()

def run_scheduler():
    print("⏰ Zamanlayıcı başlatıldı...")
    schedule.every(6).hours.do(check_all_tracked_products)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
