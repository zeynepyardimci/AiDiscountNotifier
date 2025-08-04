# 🛒 AI Discount Notifier

**Yapay zekâ destekli fiyat takip ve bildirim sistemi**

AI Discount Notifier, kullanıcıların tarif ettiği ürünleri anlayan, bu ürünleri e-ticaret sitelerinde arayıp en uygun fiyatlı seçenekleri sunan yapay zekâ destekli bir sistemdir. Kullanıcılar beğendikleri ürünleri favorilerine ekleyebilir; sistem, ürün fiyatı düştüğünde bildirim göndererek kullanıcıyı anında haberdar eder.

---

## 💡 Amaç

- Kullanıcıların ürünleri tek tek aramak yerine doğal dil kullanarak tarif etmesini sağlamak  
- Gerçek zamanlı fiyat değişimlerini takip ederek kullanıcıya bildirim göndermek  
- E-ticaret takibini daha akıllı, hızlı ve erişilebilir hâle getirmek  

---

## 🚀 Temel Özellikler

- 🧠 **Gemini API** kullanılarak doğal dil girdisi filtrelere dönüştürülür  
- 🛍️ **Hepsiburada** üzerinden ürün verisi çekilir (web scraping)  
- 🔁 Ürün fiyatları düzenli olarak kontrol edilir  
- 🔔 **Firebase Cloud Messaging** ile kullanıcıya anında bildirim gönderilir  
- 💾 **Firebase Firestore** üzerinde kullanıcıya özel ürün takibi yapılır  
- 🌐 Kullanıcı dostu React tabanlı arayüz ile şık bir deneyim sunar  

---

## 🧰 Kullanılan Teknolojiler

| Katman         | Teknoloji                          | Açıklama                                      |
|----------------|------------------------------------|-----------------------------------------------|
| NLP            | **Gemini API**                     | Ürün açıklamasını yapay zekâ ile analiz eder  |
| Backend        | **Flask**                          | Python tabanlı REST API                       |
| Bildirim       | **Firebase Cloud Messaging**       | Fiyat düşüşü anında push bildirimi            |
| Veritabanı     | **Firebase Firestore (NoSQL)**     | Takip edilen ürünlerin saklanması             |
| Scraper        | **Playwright**                     | Hepsiburada web verisi çekimi                 |
| Frontend       | **React + TypeScript + Tailwind**  | Modern, responsive kullanıcı arayüzü          |

---

## 🧠 Sistem Akışı

1. Kullanıcı: _"Siyah Etek"_ yazar  
2. AI, bu açıklamayı `kategori`, `renk`, `numara`, `marka` gibi filtrelere çevirir  
3. Scraper, bu filtrelerle e-ticaret sitesinde ürünleri tarar  
4. Ürün bulunduğunda Firestore’a kaydedilir  
5. Düzenli aralıklarla fiyat kontrolü yapılır  
6. Fiyat düşerse, kullanıcıya bildirim gönderilir  

---

## 🔧 Kurulum

### Backend (Python - Flask)

```bash
cd backend
python main.py
```

### Frontend (React - TypeScript)

```bash
cd frontend
npm install
npm run dev
```

## 🚀 Kurulum Notu:
Firebase ile bildirim göndermek için gerekli dosya: `ai-discount-notifier-main-firebase-adminsdk-fbsvc-d6162fb703.json`
Bu dosyayı `backend/` klasörüne ekleyin. (Jüriler BTK Hackhathon formundaki "Ürünüzün Detaylarını Anlattığınız Açıklama Giriniz." kısmından linke ulaşıp indirebilir.)

---

## 👩‍💻 Geliştirici Ekip

**TechNova** ekibi tarafından geliştirilmiştir. Ekip üyeleri:

- Azra Ateşoğlu 
- Nisa Naz Korkmaz 
- Zeynep Yardımcı

---
## © 2025 TechNova – Tüm hakları saklıdır.
