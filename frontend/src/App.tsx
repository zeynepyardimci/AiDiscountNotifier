import React, { useEffect, useState } from "react";
import {
  ShoppingBag,
  Package,
  CheckCircle,
  Trash2,
  Edit,
  Bell,
  Heart,
  Search,
  Star,
  Zap,
  Smartphone,
  Shield,
  X,
} from "lucide-react";
import "./App.css";
import JuryModeButton from "./components/JuryModeButton";

interface ProductInfo {
  id?: string;
  description: string;
  price?: number;
  link?: string;
  site?: string;
  discount_detected?: boolean;
  discount_percentage?: number;
}

interface SearchResult {
  id: number;
  name: string;
  price: string;
  link: string;
  site: string;
}

const API_BASE = "http://localhost:5001";
const USER_ID = "demo-user";

// Fiyatı TL formatında göstermek için fonksiyon
const formatPrice = (price: number | string): string => {
  const numericPrice = typeof price === "string" ? parseFloat(price) : price;

  if (isNaN(numericPrice)) {
    return "0,00 ₺";
  }

  return new Intl.NumberFormat("tr-TR", {
    style: "currency",
    currency: "TRY",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(numericPrice / 100);
};

const App: React.FC = () => {
  const [productDescription, setProductDescription] = useState("");
  const [isSearching, setIsSearching] = useState(false);
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [allProducts, setAllProducts] = useState<ProductInfo[]>([]);
  const [editingProduct, setEditingProduct] = useState<ProductInfo | null>(
    null
  );
  const [showSuccess, setShowSuccess] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");

  const fetchAllProducts = async () => {
    try {
      const res = await fetch(`${API_BASE}/products?user_id=${USER_ID}`);
      const result = await res.json();
      setAllProducts(result.products || []);
    } catch (err) {
      console.error("Ürünler alınamadı", err);
    }
  };

  useEffect(() => {
    fetchAllProducts();
  }, []);

  const handleSearch = async () => {
    if (!productDescription.trim()) return;

    setIsSearching(true);
    try {
      console.log("[DEBUG] Arama başlatılıyor:", productDescription);
      console.log("[DEBUG] API URL:", `${API_BASE}/search-products`);

      const res = await fetch(`${API_BASE}/search-products`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          description: productDescription,
          user_id: USER_ID,
        }),
      });

      console.log("[DEBUG] Response status:", res.status);
      console.log("[DEBUG] Response ok:", res.ok);

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const result = await res.json();
      console.log("[DEBUG] Backend yanıtı:", result);

      if (result.error) {
        alert(result.error);
        return;
      }

      console.log("[DEBUG] Arama sonuçları:", result.products);
      setSearchResults(result.products || []);
    } catch (err: any) {
      console.error("Arama hatası:", err);
      alert(`Arama hatası: ${err.message}`);
    } finally {
      setIsSearching(false);
    }
  };

  const handleAddToFavorites = async (product: SearchResult) => {
    try {
      // Önce kullanıcıya onay soralım
      const confirmed = window.confirm(
        `"${product.name}" ürününü favorilere eklemek istediğinizden emin misiniz?\n\nFiyat: ${product.price}\nSite: ${product.site}`
      );

      if (!confirmed) return;

      const res = await fetch(`${API_BASE}/add-to-favorites`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          product: product,
          user_id: USER_ID,
        }),
      });

      const result = await res.json();
      if (result.error) {
        alert(`Hata: ${result.error}`);
        return;
      }

      setSuccessMessage(`${product.name} favorilere eklendi!`);
      setShowSuccess(true);
      fetchAllProducts();

      // 3 saniye sonra success mesajını kapat
      setTimeout(() => {
        setShowSuccess(false);
      }, 3000);
    } catch (err) {
      console.error("Favorilere ekleme hatası:", err);
      alert(
        "Favorilere ekleme sırasında bir hata oluştu. Lütfen tekrar deneyin."
      );
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await fetch(`${API_BASE}/products/${id}`, { method: "DELETE" });
      fetchAllProducts();
    } catch (err) {
      console.error("Silme hatası:", err);
    }
  };

  const handleEditSave = async () => {
    if (!editingProduct?.id) return;
    try {
      await fetch(`${API_BASE}/products/${editingProduct.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(editingProduct),
      });
      setEditingProduct(null);
      fetchAllProducts();
    } catch (err) {
      console.error("Güncelleme hatası:", err);
    }
  };

  const handleReset = () => {
    setProductDescription("");
    setIsSearching(false);
    setSearchResults([]);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && e.ctrlKey) {
      handleSearch();
    }
  };

  return (
    <div className="app-container">
      <div className="main-wrapper">
        <div className="hero-section">
          <div className="hero-logo">
            <ShoppingBag size={40} />
          </div>
          <h1 className="hero-title">İndirim Takip Sistemi</h1>
          <p className="hero-subtitle">
            Aradığınız ürünün özelliklerini detaylı bir şekilde belirtin ,
            sonuçları görün, istediğinizi favorilere ekleyin.
          </p>
          {/* Features Badges */}
          <div className="flex gap-6 mt-4">
            <div className="flex items-center gap-2 bg-gray-100 px-3 py-2 rounded-md shadow-sm">
              <Zap size={18} />
              <span>Hızlı İşlem</span>
            </div>
            <div className="flex items-center gap-2 bg-gray-100 px-3 py-2 rounded-md shadow-sm">
              <Smartphone size={18} />
              <span>Mobil Uyumlu</span>
            </div>
            <div className="flex items-center gap-2 bg-gray-100 px-3 py-2 rounded-md shadow-sm">
              <Shield size={18} />
              <span>Güvenli</span>
            </div>
          </div>
        </div>
      </div>

      <div className="content-wrapper">
        <div className="form-card">
          <div className="form-header">
            <div className="form-logo">
              <Search size={28} />
            </div>
            <h2 className="form-title">Ürün Ara</h2>
            <p className="form-description">
              Ürünü detaylı açıklayın, sistem sitelerde arasın ve sonuçları
              göstersin.
            </p>
          </div>

          <textarea
            value={productDescription}
            onChange={(e) => setProductDescription(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="Örnek: Kısa kollu beyaz tişört, M beden, pamuklu kumaş..."
            className="form-textarea"
            maxLength={500}
          />
          <div className="character-count">{productDescription.length}/500</div>

          <button
            onClick={handleSearch}
            disabled={!productDescription.trim() || isSearching}
            className="form-submit-button"
          >
            {isSearching ? "Aranıyor..." : "Ürün Ara"}
          </button>
        </div>

        {showSuccess && (
          <div className="success-card">
            <CheckCircle size={40} color="#10b981" />
            <h3>✅ {successMessage}</h3>
            <p className="notification-info">
              <Bell size={16} /> Bu üründe indirim olduğunda size bildirim
              gönderilecek.
            </p>
            <button
              onClick={() => setShowSuccess(false)}
              className="reset-button"
            >
              Tamam
            </button>
          </div>
        )}

        {searchResults.length > 0 && (
          <div className="form-card">
            <h3 className="form-title">
              <Search size={20} /> Arama Sonuçları ({searchResults.length})
            </h3>
            <p className="search-info">
              💡 İstediğiniz ürünü favorilere ekleyebilirsiniz. Fiyat takibi
              otomatik olarak yapılacak.
            </p>
            <div className="search-results">
              {searchResults.map((product) => (
                <div key={product.id} className="search-result-item">
                  <div className="product-info">
                    <div className="product-name">
                      <strong>{product.name}</strong>
                    </div>
                    <div className="product-details">
                      <span className="price">💰 {product.price}</span>
                      <span className="site-name">🏪 {product.site}</span>
                    </div>
                  </div>
                  <div className="product-actions">
                    <a
                      href={product.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="link-button"
                    >
                      👁️ Ürünü Gör
                    </a>
                    <button
                      onClick={() => handleAddToFavorites(product)}
                      className="favorite-button"
                      title="Favorilere Ekle"
                      style={{
                        background:
                          "linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%)",
                        color: "white",
                        border: "none",
                        padding: "12px 20px",
                        borderRadius: "8px",
                        cursor: "pointer",
                        fontSize: "14px",
                        fontWeight: "600",
                        marginLeft: "10px",
                      }}
                    >
                      ❤️ Favorilere Ekle
                    </button>
                  </div>
                </div>
              ))}
            </div>
            <button onClick={handleReset} className="reset-button">
              🔍 Yeni Ürün Bilgisi Gir
            </button>
          </div>
        )}

        <div className="form-card">
          <h3 className="form-title">
            <Heart size={20} /> Favori Ürünlerim ({allProducts.length})
          </h3>
          {allProducts.map((p) => (
            <div key={p.id} className="product-info-display">
              {editingProduct?.id === p.id ? (
                <>
                  <input
                    value={editingProduct?.description || ""}
                    onChange={(e) =>
                      editingProduct &&
                      setEditingProduct({
                        ...editingProduct,
                        description: e.target.value,
                      })
                    }
                    className="edit-input"
                  />
                  <button
                    onClick={handleEditSave}
                    className="save-button"
                    title="Kaydet"
                    aria-label="Kaydet"
                  >
                    <CheckCircle size={20} color="#10b981" />
                  </button>
                  <button
                    onClick={() => setEditingProduct(null)}
                    className="cancel-button"
                    title="İptal"
                    aria-label="İptal"
                  >
                    <X size={20} color="#ef4444" />
                  </button>
                </>
              ) : (
                <>
                  <div className="product-info">
                    <div className="product-name">
                      <strong>{p.description}</strong>
                      {p.discount_detected && (
                        <span className="discount-badge">
                          🎉 %{p.discount_percentage?.toFixed(1)} İndirim!
                        </span>
                      )}
                    </div>
                    <div className="product-details">
                      <span>
                        {p.price ? formatPrice(p.price) : "Fiyat yok"}
                      </span>
                      <span className="site-name">{p.site}</span>
                    </div>
                  </div>
                  <div className="product-actions">
                    <a
                      href={p.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="link-button"
                    >
                      Ürünü Gör
                    </a>
                    <button
                      onClick={() => handleDelete(p.id!)}
                      className="icon-button delete-button"
                      title="Sil"
                      aria-label="Sil"
                    >
                      <Trash2 size={18} color="#ef4444" />
                    </button>

                    <button
                      onClick={() => setEditingProduct(p)}
                      className="icon-button edit-button"
                      title="Düzenle"
                      aria-label="Düzenle"
                    >
                      <Edit size={18} color="#3b82f6" />
                    </button>
                  </div>
                </>
              )}
            </div>
          ))}
        </div>
        <JuryModeButton />
      </div>

      <div className="footer text-center w-full py-4 text-sm text-gray-500">
        © 2025 İndirim Takip Sistemi. Tüm hakları saklıdır.
      </div>
    </div>
  );
};

export default App;
