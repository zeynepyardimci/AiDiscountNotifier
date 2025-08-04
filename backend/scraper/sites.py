from urllib.parse import quote_plus
from playwright.sync_api import sync_playwright

def search_hepsiburada(filters):
    results = []
    search_terms = [filters.get("category", "")]
    for key in ["color", "size", "features", "gender", "brand"]:
        if filters.get(key):
            search_terms.append(filters[key])

    search_query = quote_plus(" ".join(search_terms))
    search_url = f"https://www.hepsiburada.com/ara?q={search_query}"
    print(f"[DEBUG] Hepsiburada URL: {search_url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(search_url, timeout=1000)
            page.wait_for_selector("[data-testid='product-card']", timeout=1000)
            items = page.query_selector_all("[data-testid='product-card']")
            for item in items[:3]:
                try:
                    name_el = item.query_selector("h3") or item.query_selector("[data-testid='product-name']")
                    price_el = item.query_selector("div[data-test-id='price-current-price']") or item.query_selector("span.price-value")
                    link_el = item.query_selector("a")
                    name = name_el.inner_text().strip() if name_el else None
                    price = price_el.inner_text().strip() if price_el else None
                    link = link_el.get_attribute("href") if link_el else None
                    if link and link.startswith("/"):
                        link = "https://www.hepsiburada.com" + link
                    if name and price and link:
                        results.append({"name": name, "price": price, "link": link, "site": "hepsiburada"})
                except:
                    continue
        except Exception as e:
            print(f"[DEBUG] Hepsiburada sayfa veya ürün kartları yüklenirken zaman aşımı veya hata: {e}")
        finally:
            browser.close()
    print(f"[DEBUG] Hepsiburada'dan toplam {len(results)} ürün döndü.")
    return results

def search_lcwaikiki(filters):
    results = []
    search_terms = [filters.get("category", "")]
    for key in ["color", "size", "features", "gender", "brand"]:
        if filters.get(key):
            search_terms.append(filters[key])

    search_query = quote_plus(" ".join(search_terms))
    search_url = f"https://www.lcwaikiki.com/tr-TR/TR/arama?q={search_query}"
    print(f"[DEBUG] LC Waikiki URL: {search_url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(search_url, timeout=1000)
            page.wait_for_selector(".product-card__container", timeout=1000)
            items = page.query_selector_all(".product-card__container")
            for item in items[:3]:
                name_el = item.query_selector(".product-card__title")
                price_el = item.query_selector(".product-card__price--new") or item.query_selector(".product-card__price")
                link_el = item.query_selector("a")
                name = name_el.inner_text().strip() if name_el else None
                price = price_el.inner_text().strip() if price_el else None
                link = link_el.get_attribute("href") if link_el else None
                if link and not link.startswith("http"):
                    link = "https://www.lcwaikiki.com" + link
                if name and price and link:
                    results.append({"name": name, "price": price, "link": link, "site": "lcwaikiki"})
        except Exception as e:
            print(f"[DEBUG] LC Waikiki sayfa veya ürün kartları yüklenirken zaman aşımı veya hata: {e}")
        finally:
            browser.close()
    print(f"[DEBUG] LC Waikiki'den toplam {len(results)} ürün döndü.")
    return results

def search_defacto(filters):
    results = []
    search_terms = [filters.get("category", "")]
    for key in ["color", "size", "features", "gender", "brand"]:
        if filters.get(key):
            search_terms.append(filters[key])

    search_query = quote_plus(" ".join(search_terms))
    search_url = f"https://www.defacto.com.tr/arama?q={search_query}"
    print(f"[DEBUG] DeFacto URL: {search_url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(search_url, timeout=1000)
            page.wait_for_selector(".product-item", timeout=1000)
            items = page.query_selector_all(".product-item")
            for item in items[:3]:
                name_el = item.query_selector(".product-title")
                price_el = item.query_selector(".current-price") or item.query_selector(".price")
                link_el = item.query_selector("a")
                name = name_el.inner_text().strip() if name_el else None
                price = price_el.inner_text().strip() if price_el else None
                link = link_el.get_attribute("href") if link_el else None
                if link and not link.startswith("http"):
                    link = "https://www.defacto.com.tr" + link
                if name and price and link:
                    results.append({"name": name, "price": price, "link": link, "site": "defacto"})
        except Exception as e:
            print(f"[DEBUG] DeFacto sayfa veya ürün kartları yüklenirken zaman aşımı veya hata: {e}")
        finally:
            browser.close()
    print(f"[DEBUG] DeFacto'dan toplam {len(results)} ürün döndü.")
    return results

def search_koton(filters):
    results = []
    search_terms = [filters.get("category", "")]
    for key in ["color", "size", "features", "gender", "brand"]:
        if filters.get(key):
            search_terms.append(filters[key])

    search_query = quote_plus(" ".join(search_terms))
    search_url = f"https://www.koton.com/tr-tr/arama?q={search_query}"
    print(f"[DEBUG] Koton URL: {search_url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(search_url, timeout=1000)
            page.wait_for_selector(".product-list__item", timeout=1000)
            items = page.query_selector_all(".product-list__item")
            for item in items[:3]:
                name_el = item.query_selector(".product-list__product-name")
                price_el = item.query_selector(".product-list__price")
                link_el = item.query_selector("a")
                name = name_el.inner_text().strip() if name_el else None
                price = price_el.inner_text().strip() if price_el else None
                link = link_el.get_attribute("href") if link_el else None
                if link and not link.startswith("http"):
                    link = "https://www.koton.com" + link
                if name and price and link:
                    results.append({"name": name, "price": price, "link": link, "site": "koton"})
        except Exception as e:
            print(f"[DEBUG] Koton sayfa veya ürün kartları yüklenirken zaman aşımı veya hata: {e}")
        finally:
            browser.close()
    print(f"[DEBUG] Koton'dan toplam {len(results)} ürün döndü.")
    return results

def get_product_price_from_url(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, timeout=1000)
            price_el = page.query_selector(".price") or page.query_selector(".current-price")
            return price_el.inner_text().strip() if price_el else None
        except Exception as e:
            print(f"[DEBUG] Fiyat alınırken hata oluştu: {e}")
            return None
        finally:
            browser.close()

def search_all_sites(filters):
    results = []
    results.extend(search_hepsiburada(filters))
    results.extend(search_lcwaikiki(filters))
    results.extend(search_defacto(filters))
    results.extend(search_koton(filters))
    return results
