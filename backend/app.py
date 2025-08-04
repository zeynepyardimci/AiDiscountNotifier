import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper.sites import search_all_sites
from scraper.product_db import save_product_firestore, get_tracked_products, check_price_changes
from notifications.push_sender import init_firebase
from gemini.parse_user_input import parse_product_description

app = Flask(__name__)
CORS(app, origins=['*'], 
     methods=['GET', 'POST', 'PUT', 'DELETE'], 
     allow_headers=['Content-Type', 'Authorization'])

# Firebase başlat
init_firebase()


@app.route('/test', methods=['GET'])
def test():
    """Test endpoint"""
    return jsonify({'message': 'Backend çalışıyor!', 'status': 'success'})


@app.route('/search-products', methods=['POST'])
def search_products():
    """Kullanıcının aradığı ürünleri Gemini API ile filtreleyerek arar, sonuç yoksa test verisi döner"""
    print(f"[DEBUG] POST isteği alındı: /search-products")
    try:
        data = request.get_json()
        print(f"[DEBUG] Request data: {data}")
        description = data.get('description', '')
        user_id = data.get('user_id')

        if not description or not user_id:
            return jsonify({'error': 'Ürün açıklaması ve kullanıcı ID\'si zorunludur'}), 400

        print(f"[DEBUG] Arama yapılıyor: {description}")

        # Gemini API ile açıklamayı filtrelere çevir
        filters = parse_product_description(description)
        if not filters:
            print("[WARN] Gemini filtre üretemedi, test verisine geçilecek")
        else:
            print(f"[DEBUG] Gemini'den gelen filtreler: {filters}")
            results = search_all_sites(filters)
            print(f"[DEBUG] Gerçek sonuç sayısı: {len(results)}")

            if results:
                formatted_results = []
                for i, product in enumerate(results[:10]):
                    formatted_results.append({
                        'id': i,
                        'name': product["name"],
                        'price': product["price"],
                        'link': product["link"],
                        'site': product.get("site", "hepsiburada")
                    })
                    print(f"[DEBUG] Ürün {i}: {product['name']} - {product['price']}")
                
                return jsonify({
                    'success': True,
                    'products': formatted_results
                })

        # Eğer sonuç yoksa veya filtre başarısızsa: test verileri
        print("[DEBUG] Sonuç bulunamadı veya Gemini başarısız, test verisi döndürülüyor")
       
        test_results = [
    {
        "name": "Koton Aerobin Kumaş A‑Kesim Saten Midi Boy Siyah Etek – M Beden",
        "price": "899.99 TL",
        "link": "https://www.koton.com/aerobin-kumas-a-kesim-yirtmac-detayli-midi-boy-saten-klos-etek-siyah-4074480-2/",
        "site": "koton"
    },
    {
        "name": "Hepsiburada Grimelange Estela Paraşüt Kumaş Uzun Balon Siyah Etek – M Beden",
        "price": "406.35 TL",
        "link": "https://www.hepsiburada.com/grimelange-estela-kadin-beli-lastikli-cepli-su-gecirmez-parasut-kumas-uzun-balon-siyah-etek-p-HBCV0000705UPR",
        "site": "hepsiburada"
    },
    {
        "name": "Defacto Relax Fit Saten Uzun Boy Siyah Etek – M Beden",
        "price": "899.99 TL",
        "link": "https://www.defacto.com.tr/relax-fit-beli-lastikli-saten-uzun-boy-etek-3344632",
        "site": "defacto"
    },
    {
        "name": "Defacto Beli Bağcıklı Viskon Maxi Siyah Etek – M Beden",
        "price": "189.99 TL",
        "link": "https://www.defacto.com.tr/beli-bagcikli-viskon-maxi-tesettur-etek-3210910",
        "site": "defacto"
    },
    {
        "name": "Koton Viskon‑Keten Cepli Uzun Kloş Siyah Etek – M Beden",
        "price": "179.90 TL",
        "link": "https://www.koton.com/rahat-kalip-viskon-keten-karisimli-cepli-uzun-klos-etek-siyah-3971023-1/",
        "site": "koton"
    }
]


        formatted_results = []
        for i, product in enumerate(test_results[:10]):
            formatted_results.append({
                'id': i,
                'name': product["name"],
                'price': product["price"],
                'link': product["link"],
                'site': product.get("site", "hepsiburada")
            })
            print(f"[DEBUG] Test Ürün {i}: {product['name']} - {product['price']}")

        return jsonify({
            'success': True,
            'products': formatted_results,
            'note': 'Gerçek sonuç bulunamadı, test verisi gösteriliyor.'
        })

    except Exception as e:
        print(f"[ERROR] Arama hatası: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/add-to-favorites', methods=['POST'])
def add_to_favorites():
    """Kullanıcının seçtiği ürünü favorilere ekler"""
    try:
        data = request.get_json()
        product_data = data.get('product')
        user_id = data.get('user_id')

        if not product_data or not user_id:
            return jsonify({'error': 'Ürün bilgisi ve kullanıcı ID\'si zorunludur'}), 400

        # Ürünü Firebase'e kaydet
        save_product_firestore(
            name=product_data["name"],
            price=product_data["price"],
            link=product_data["link"],
            site=product_data.get("site", "hepsiburada"),
            filters={},
            user_id=user_id
        )

        return jsonify({
            'success': True,
            'message': 'Ürün favorilere eklendi!'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/products', methods=['GET'])
def get_products():
    """Kullanıcının tüm ürünlerini getirir"""
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'Kullanıcı ID\'si gerekli'}), 400

        products = get_tracked_products(user_id=user_id)

        formatted = []
        for product in products:
            formatted.append({
                'id': product.get('id'),
                'description': product.get('name', ''),
                'price': product.get('current_price', 0),
                'link': product.get('link', ''),
                'site': product.get('site', ''),
                'discount_detected': product.get('discount_detected', False),
                'discount_percentage': product.get('discount_percentage', 0)
            })

        return jsonify({'products': formatted})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Belirli bir ürünü siler"""
    try:
        from firebase_admin import firestore
        db = firestore.client()
        db.collection("products").document(product_id).delete()
        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    """Ürün bilgilerini günceller"""
    try:
        data = request.get_json()
        from firebase_admin import firestore
        db = firestore.client()

        doc_ref = db.collection("products").document(product_id)
        doc_ref.update({
            'name': data.get('description', ''),
            'last_updated': firestore.SERVER_TIMESTAMP
        })

        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/check-prices', methods=['POST'])
def check_prices():
    """Tüm kullanıcılar için ürün fiyatlarını kontrol eder"""
    try:
        updated_products = check_price_changes()

        return jsonify({
            'success': True,
            'updated_count': len(updated_products),
            'products': updated_products
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/parse-product', methods=['POST'])
def parse_product():
    """Açıklamayı parçalar (AI destekli değil, basit parse)"""
    try:
        data = request.get_json()
        text = data.get('text', '')

        parsed = {
            'category': text.split()[0] if text else '',
            'brand': None,
            'color': None,
            'size': None,
            'features': text
        }

        return jsonify(parsed)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/subscribe', methods=['POST'])
def subscribe_token():
    try:
        data = request.get_json()
        token = data.get('token')
        user_id = data.get('user_id')

        if not token or not user_id:
            return jsonify({'error': 'Token ve kullanıcı ID gerekli'}), 400

        from notifications.push_sender import subscribe_to_topic
        subscribe_to_topic(token, f"user_{user_id}")  # kişiye özel topic

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/run-price-checker', methods=['GET'])
def run_price_checker():
    mode = request.args.get('mode', '')

    try:
        if mode == "test":
            result = subprocess.run(
                ["python", "backend/notifications/price_checker.py", "--test"],
                capture_output=True,
                text=True
            )
        else:
            result = subprocess.run(
                ["python", "backend/notifications/price_checker.py"],
                capture_output=True,
                text=True
            )

        return jsonify({
            "status": "success",
            "output": result.stdout,
            "error": result.stderr
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Flask API Server Başlatıldı!")
    print("📍 http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)
