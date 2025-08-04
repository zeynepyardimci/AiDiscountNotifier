#!/usr/bin/env python3
"""
Test script for the scraper functionality
"""

import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from scraper.sites import search_hepsiburada, search_all_sites

def test_hepsiburada():
    print("🔍 Hepsiburada test ediliyor...")
    results = search_hepsiburada("beyaz gömlek", brand="LC Waikiki", size="M")
    
    if results:
        print(f"✅ {len(results)} ürün bulundu:")
        for i, product in enumerate(results, 1):
            print(f"  {i}. {product['name']}")
            print(f"     Fiyat: {product['price']}")
            print(f"     Link: {product['link']}")
            print()
    else:
        print("❌ Hiç ürün bulunamadı")

def test_all_sites():
    print("🔍 Tüm siteler test ediliyor...")
    filters = {
        "category": "beyaz gömlek",
        "brand": "LC Waikiki",
        "size": "M"
    }
    
    results = search_all_sites(filters)
    
    if results:
        print(f"✅ Toplam {len(results)} ürün bulundu:")
        for i, product in enumerate(results, 1):
            print(f"  {i}. {product['name']}")
            print(f"     Fiyat: {product['price']}")
            print(f"     Link: {product['link']}")
            print()
    else:
        print("❌ Hiç ürün bulunamadı")

if __name__ == "__main__":
    print("🚀 Scraper Test Başlıyor...")
    print("=" * 50)
    
    try:
        test_hepsiburada()
        print("=" * 50)
        test_all_sites()
    except Exception as e:
        print(f"❌ Test sırasında hata: {e}")
    
    print("✅ Test tamamlandı!") 