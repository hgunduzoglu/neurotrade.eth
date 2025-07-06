# NeuroTrade AI Agent - HTTP API Integration

AI Agent artık kendi HTTP server'ını çalıştırıyor! Frontend direkt AI agent'a bağlanabilir.

## 🚀 Nasıl Çalıştırılır

### 1. AI Agent'ı Başlatın

```bash
# Terminal'i neurotrade_ai_agent klasörüne açın
cd neurotrade_ai_agent

# AI Agent'ı başlatın (HTTP server otomatik başlar)
python neurotrade_agent.py
```

### 2. Bağlantı Durumunu Kontrol Edin

```bash
# Tarayıcıda açın veya curl ile test edin
curl http://localhost:8000/health

# Sonuç:
{
  "status": "healthy",
  "timestamp": "2025-01-06T12:00:00.000Z",
  "version": "1.0.0",
  "agent_address": "agent1q..."
}
```

### 3. Frontend'i Başlatın

```bash
# Ana dizinde
npm run dev
```

## 🌐 Otomatik Açılan Endpoint'ler

AI Agent çalıştığında otomatik olarak aşağıdaki HTTP endpoint'leri açılır:

### 🔧 Sistem Endpoint'leri
- `GET /health` - Server durumu
- `GET /supported-tokens` - Desteklenen tokenlar

### 💬 Chat Endpoint'leri
- `POST /chat` - AI ile sohbet

### 📊 Analiz Endpoint'leri
- `POST /analyze/{symbol}` - Token analizi

## 📝 Kullanım Örnekleri

### Chat Endpoint'i Test Et

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is ETH price?",
    "user_id": "test_user"
  }'
```

### Token Analizi Test Et

```bash
curl -X POST http://localhost:8000/analyze/ETH \
  -H "Content-Type: application/json"
```

### JavaScript ile Test

```javascript
// Chat test
fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: "Should I buy BTC?",
    user_id: "frontend_user"
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## 🎯 Özellikler

✅ **AI Agent + HTTP Server** - Tek komutla başlatma
✅ **Otomatik CORS** - Frontend bağlantısı hazır
✅ **Enhanced AI** - Gelişmiş analiz desteği
✅ **Fallback System** - Hata durumunda temel analiz
✅ **Real-time Updates** - Canlı market verileri
✅ **Chat Protocol** - ASI:One desteği

## 🔧 Sorun Giderme

### Port 8000 Kullanımda

```bash
# AI Agent'ı farklı port'ta çalıştır
AGENT_PORT=8002 python neurotrade_agent.py
```

### Enhanced AI Hatası

```bash
# Enhanced AI yüklenmediyse temel sistem çalışır
# Logları kontrol edin:
tail -f neurotrade_agent.log
```

### Frontend Bağlantı Hatası

```bash
# Environment variable'ı kontrol edin
# .env.local dosyasında:
NEXT_PUBLIC_AI_API_URL=http://localhost:8000
```

## 🚀 Avantajlar

- **Tek Komut**: Sadece `python neurotrade_agent.py` ile her şey başlar
- **Otomatik**: HTTP server otomatik açılır
- **CORS**: Frontend bağlantısı hazır
- **Fallback**: Enhanced AI yoksa temel sistem çalışır
- **Unified**: AI agent ve HTTP server aynı process'te

## 🎉 Başarıyla Çalıştıysa

AI Agent başladığında şu logları görmelisiniz:

```
🚀 NeuroTrade AI Agent starting up...
🌐 HTTP Server started on http://localhost:8000
🔧 Health check: http://localhost:8000/health
💬 Chat endpoint: http://localhost:8000/chat
📊 Token analysis: http://localhost:8000/analyze/{symbol}
✅ HTTP Server started successfully!
🌐 Frontend can now connect to http://localhost:8000
```

Artık frontend http://localhost:8000 üzerinden AI agent'a bağlanabilir!

---

**Not**: Artık ayrı FastAPI server gerekmez. AI agent'ın kendisi HTTP endpoint'lerini sağlar. 