import sys
import os

# backend klasörünü Python'a tanıt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraper.sites import search_lcwaikiki

urun_adi = input("Lütfen aramak istediğiniz ürünü yazın: ")
sonuclar = search_lcwaikiki(urun_adi)

for ürün in sonuclar:
    print(ürün)
