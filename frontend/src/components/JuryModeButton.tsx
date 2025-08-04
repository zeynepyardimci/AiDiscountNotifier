import { useState } from 'react';

const API_BASE = 'http://localhost:5001';

export default function JuryModeButton() {
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState('');

  const triggerTest = async () => {
    setLoading(true);
    setResponse('');

    try {
      const res = await fetch(`${API_BASE}/run-price-checker?mode=test`);
      const data = await res.json();

      if (data.status === 'success') {
        setResponse('✅ Bildirimler başarıyla gönderildi!');
        console.log('[TEST LOG]:', data.output);
      } else {
        setResponse('❌ Hata oluştu: ' + data.message);
      }
    } catch (error: any) {
      setResponse('💥 Sunucu hatası: ' + error.message);
    }

    setLoading(false);
  };

  return (
    <div className="form-card">
      <h3 className="form-title">🧪 Jüri Modu</h3>
      <p className="search-info">
        Bu buton test modunda sistemin çalıştığını jüriye göstermek için
        bildirim gönderir.
      </p>
      <button
        onClick={triggerTest}
        disabled={loading}
        className="form-submit-button"
        style={{
          background: '#7c3aed',
          color: '#fff',
          fontWeight: 'bold',
          padding: '12px 20px',
          borderRadius: '10px',
          marginTop: '10px',
        }}
      >
        {loading ? 'Gönderiliyor...' : '🧪 Jüri Modu: Test Bildirim Gönder'}
      </button>

      {response && (
        <p
          className="mt-2 text-sm"
          style={{ color: response.startsWith('✅') ? 'green' : 'red' }}
        >
          {response}
        </p>
      )}
    </div>
  );
}
