# NeuroTrade.eth — Geliştirme Rehberi (Detaylı Flow + Adımlar)

## 🔥 Proje Özeti

NeuroTrade.eth:

- AI destekli trade önerileri sunar (Fetch.AI uAgent)
- Hem tek zincir (tek blockchain) swap yapar → **1inch Swap API** kullanır
- Hem cross-chain swap yapar → **LayerZero** kullanır
- Kullanıcıya login, wallet yönetimi, güvenli imza → **Privy** ile yapılır
- Bazı hassas verileri gizli işler → **Oasis ROFL** kullanılır
- ENS domaini neurotrade.eth kullanılır → kimlik sağlar

## 🧩 Kullanılan Teknolojiler & Görevleri

| Teknoloji         | Görevi                                  | Backend / Frontend    |
| ----------------- | --------------------------------------- | --------------------- |
| Privy             | Login, wallet yönetimi, embedded wallet | Frontend + Backend    |
| ENS               | Domain kimliği                          | Frontend + Backend    |
| Fetch.AI uAgents  | AI sinyal üretimi, Python kodu          | Backend               |
| The Graph         | Blockchain verilerini almak             | Backend               |
| 1inch Swap API    | Tek zincir swap işlemleri               | Frontend veya Backend |
| LayerZero         | Cross-chain token taşıma                | Backend               |
| Oasis ROFL        | Gizli veri işleme                       | Backend               |
| Ledger (ERC-7730) | Güvenli imzalama                        | Frontend              |

## ✅ Geliştirme Adımları ve Akış

Aşağıda tüm proje geliştirme adımları sırasıyla anlatılmıştır.

---

# 1. Privy ile Onboarding (Login ve Wallet Yönetimi)

İlk adım **login** ve **wallet oluşturma**.

### 🎯 Yapılacaklar

1. Privy SDK kur (npm install privy)
2. Privy Provider ile uygulamayı sarmala (React Context gibi)
3. Login modal aç:
   - email login
   - Metamask, Ledger gibi wallet connect
4. Kullanıcı login olunca:
   - privy.user.id → kullanıcı kimliği
   - privy.user.wallet.address → wallet adresi

### ✅ Neden?

- Kullanıcı olmadan **trade** yapılamaz.
- Privy embedded wallet sayesinde seed phrase gerekmez.
- Tek SDK → wallet connect işlemleri kolaylaşır.

---

# 2. ENS Domain Kullanımı

Projemiz ENS domainine sahip: **neurotrade.eth**

### 🎯 Yapılacaklar

- ethers.js veya wagmi kullanarak ENS text recordları oku veya güncelle:
  - ör. "AI agent versiyonu"
  - ör. "desteklediği zincirler"

### ✅ Neden?

- Projeye güven katar
- ENS ödüllerine katılabiliriz

---

# 3. AI Agent Geliştirmesi (Fetch.AI uAgents)

NeuroTrade’in AI beyni **Fetch.AI uAgent** kullanır. **Bu kısmı Python’da geliştireceğiz.**

### ✅ Neden Python?

- uAgent SDK sadece Python’da var
- AI modelleri Python’da daha güçlü

### 🎯 AI Agent Görevleri:

- The Graph’ten fiyat verisi çeker (GraphQL endpoint)
- Piyasa analizini yapar
- Kullanıcının trade kurallarını kontrol eder (ör. ETH < 2400\$)
- AI önerisi oluşturur:
  - "ETH al."
  - "USDC → ETH swap yap."
- Cross-chain işlemlerde hangi zincirde swap yapacağını belirler

### 🎯 AI Agent için Yapılacaklar:

1. Python ortamı kur (virtualenv, poetry vs.)
2. uAgent SDK yükle
3. AI agent kodunu yaz:
   - GraphQL sorguları ile fiyat çek
   - basit ML modeli kur (veya sabit kurallar)
   - öneri metinleri üret
4. Agent’i **Agentverse** üzerinde deploy et veya local çalıştır
5. AI agent bir API gibi çalışır → REST veya websockets üzerinden çağrılabilir

---

# 4. Python + JS Bağlantısı

### ✅ Neden Bağlamak Gerekir?

- Frontend JS → kullanıcıya AI önerisi göstermek ister
- AI kodu Python’da → JS ile konuşmak lazım

### 🎯 Nasıl Bağlayacağız?

**Yöntem 1 — REST API**

- Python’da Flask/FastAPI ile bir endpoint yaz
- JS → HTTP request gönderir
- Response döner

Örnek Flow:

```
JS → POST /ai-signal { params }
Python → analiz yapar → response döner
```

**Yöntem 2 — Websocket**

- Python websocket açar
- JS sürekli bağlı kalır
- Anlık önerileri alabilir

**Hackathon için en kolay yol → REST API.**

### 🎯 Yapılacaklar

1. Python’da FastAPI kur
2. AI agent’ı HTTP endpoint’e bağla
3. JS kodu → fetch veya axios ile çağır
4. AI cevabını frontend’de göster

---

# 5. Kullanıcının Trade Modunu Seçmesi

Frontend’de kullanıcıya **üç mod** sunacağız:

✅ AI önerileri → kullanıcı manuel karar verir ✅ Tam otomatik AI → AI kendisi trade yapar ✅ Kullanıcı kuralları → "ETH < 2400\$ → al" gibi

### 🎯 Yapılacaklar

- React state oluştur:
  - selectedMode: "manual", "autoAI", "customRules"
- UI üzerinde seçim ekranı yap

**Her mod ayrı işlem akışını tetikler.**

---

# 6. The Graph Kullanımı

AI agent veya JS kodu, blockchain verilerini **The Graph**’ten çeker:

Örnek:

> "Arbitrum’da son 10 blokta ETH fiyatı ne?"

### 🎯 Yapılacaklar

- The Graph’ten endpoint belirle
- GraphQL sorgusu yaz:
  - token price
  - pool liquidity
  - volume
- Python veya JS → sorgu gönderir

**AI’nin analiz yapabilmesi için Graph verisi şart.**

---

# 7. Tek Zincir İşlem (1inch Swap API)

Kullanıcı diyor ki:

> "Arbitrum üzerinde 500 USDC → ETH almak istiyorum."

Bu durumda: → **1inch API** çağırılacak → swap yapılacak

### 🎯 Yapılacaklar

1. 1inch API docs’u incele: [https://portal.1inch.dev/documentation/apis/swap/introduction](https://portal.1inch.dev/documentation/apis/swap/introduction)
2. JS’te axios veya fetch kullan
3. Swap datasını al:
   - en iyi fiyat
   - slippage
   - raw transaction data
4. Privy wallet veya Ledger ile imzala
5. İşlemi blockchain’e gönder

### ✅ Neden 1inch?

- Cross-DEX routing
- En iyi fiyat garantisi
- Tek zincirde işlem hızlı çözülür

---

# 8. Cross-Chain İşlem (LayerZero + 1inch)

Kullanıcı diyor ki:

> "Base zincirindeki USDC’mi Arbitrum’da ETH yapmak istiyorum."

### Akış:

1. **LayerZero** çağrılır → Base → Arbitrum transfer
2. Hedef zincire mesaj gider:
   - "Arbitrum’da 500 USDC geldi."
3. Arbitrum’da **1inch API** çağırılır → ETH swap yapılır
4. ETH kullanıcının cüzdanına geçer

### 🎯 Yapılacaklar

- LayerZero SDK yükle
- Cross-chain message formatını belirle
- LayerZero message listener yaz
- Arbitrum tarafında 1inch çağrısını yap
- İşlem bitince frontend’e event döndür

**Bu sayede LayerZero ödüllerine katılabilirsin.**

---

# 9. Kurallara Dayalı Otomatik İşlem

Kullanıcı kendi kuralını yazar:

> "ETH < 2400\$ olursa al."

Bu kurallar:

- Python AI agent’ta veya
- Oasis ROFL’da saklanabilir (gizlilik için)

### 🎯 Yapılacaklar

- Frontend → kural formu yap
- Kuralları backend’e kaydet:
  - Python backend’e yolla
  - veya ROFL kullanarak gizli sakla
- AI agent fiyatları sürekli kontrol eder
- Şart oluşunca otomatik swap çağırılır

**Cross-chain ise LayerZero + 1inch devreye girer.**

---

# 10. Ledger Integration (ERC-7730 Clear Signing)

Ledger ile **Clear Signing** kullanacağız:

- swap işlemini Ledger cihazında onaylarsın
- kullanıcı ne imzaladığını net görür:
  - "500 USDC → 0.15 ETH"

### 🎯 Yapılacaklar

- Ledger SDK yükle (ethers.js destekli)
- ERC-7730 JSON oluştur
- Ledger cihazına transaction gönder

**Hackathon için önemli güvenlik artısı sağlar.**

---

# 11. INTMAX (Opsiyonel)

Özel ödemeler yapmak istersen INTMAX entegre edebilirsin:

- AI subscription için ödeme
- Gizli ödeme yapmak isteyen kullanıcılar için

**Bu opsiyoneldir.**

---

# Python + JS Bağlantısının Özeti

> **Senin projen iki parçalı: Python + JS.**

✅ Python → AI, Fetch.AI, ROFL entegrasyonu ✅ JS → Frontend UI, Privy, 1inch, LayerZero entegrasyonu

Birbirine bağlamak için:

- Python’da REST API aç (FastAPI, Flask)
- JS → fetch ile çağırır
- AI cevabını UI’ye koyarsın

Böylece **tek frontend** kullanarak **backend AI** logic’i çalıştırırsın.

---

# 🔥 Sonuç

**NeuroTrade.eth**, hem tek zincir, hem cross-chain trading yapabilen, AI tabanlı, güvenli ve kullanıcı dostu bir web3 trading platformudur.

Bu README → Cursor’a veya başka bir AI asistanına verildiğinde, proje baştan sona geliştirilebilir.

**Hazırsan kodlamaya başlayabilirsin!**

