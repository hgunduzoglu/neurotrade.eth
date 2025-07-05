# NeuroTrade The Graph MCP Integration 🌐

Bu belgede NeuroTrade AI Agent'ınızın **The Graph'ın gerçek MCP (Model Context Protocol) server'ına** entegrasyonu açıklanmaktadır.

## 🚀 Özellikler

- **Gerçek The Graph MCP Server**: `https://token-api.mcp.thegraph.com` adresine doğrudan bağlantı
- **Maple Nodes API Fallback**: The Graph MCP başarısız olursa Maple Nodes API kullanır
- **Çoklu Veri Kaynağı**: The Graph MCP, Maple Nodes, CoinGecko fallback'leri
- **Akıllı Tool Dispatcher**: Kullanıcı sorgularını otomatik olarak doğru The Graph aracına yönlendirir
- **Blockchain Data Expert**: ETH, token, DeFi protokol, indexer ve subgraph verileri
- **Resilient Architecture**: Bir kaynak başarısız olursa otomatik fallback

## 📁 Dosya Yapısı

```
neurotrade_ai_agent/
├── thegraph_mcp_client.py         # The Graph MCP istemci kodu
├── mcp_enhanced_agent.py          # The Graph entegreli AI agent
├── test_thegraph_integration.py   # The Graph test scripti
├── chat_proto.py                  # Chat protocol entegrasyonu
├── neurotrade_agent.py            # Orijinal agent (yedek)
├── requirements.txt               # Güncellenmiş bağımlılıklar
└── MCP_INTEGRATION_README.md      # Bu dosya
```

## 🔧 The Graph MCP Araçları

### 1. Token Verileri
- **get_token_data**: Token fiyat, hacim ve değişim verileri
- **get_balance**: Token bakiye sorguları
- **get_price**: Gerçek zamanlı fiyat verileri

### 2. The Graph Network Araçları
- **get_graph_indexer_info**: Indexer performans metrikleri
- **get_graph_allocations**: Indexer allocation verileri
- **get_graph_network_info**: Network istatistikleri
- **get_graph_indexers_list**: Tüm indexer listesi
- **convert_subgraph_to_ipfs**: Subgraph ID'den IPFS hash'e dönüştürme

### 3. DeFi Protocol Araçları
- **get_defi_protocol_data**: Uniswap, Aave, Compound verileri
- **get_protocol_metrics**: Protocol TVL, hacim, kullanıcı sayısı
- **get_liquidity_data**: Likidite pool bilgileri

## 🚀 Hızlı Başlangıç

### 1. Bağımlılıkları Yükle
```bash
cd neurotrade_ai_agent
pip install -r requirements.txt
```

### 2. Test The Graph MCP Integration
```bash
python test_thegraph_integration.py
```

### 3. Agent'ı Başlat
```bash
python mcp_enhanced_agent.py
```

## 🌐 The Graph MCP Server Integration

### Bağlantı Bilgileri
- **Primary MCP Server**: `https://token-api.mcp.thegraph.com`
- **Fallback API**: `https://api.maplenodes.com` (Maple Nodes)
- **Emergency Fallback**: CoinGecko API

### Authentication
The Graph MCP server kimlik doğrulama gerektirebilir. Gerekirse:

```bash
export THEGRAPH_API_KEY="your_api_key_here"
export THEGRAPH_MCP_URL="https://token-api.mcp.thegraph.com"
```

## 💬 Kullanım Örnekleri

### 1. Token Fiyat Sorguları
```python
# Agent'a şu soruları sorabilirsiniz:
"ETH fiyatı nedir?"
"Current ETH price"
"Show me USDC price data"
"What's the price of Bitcoin?"
```

### 2. The Graph Network Sorguları
```python
"Show me indexer information"
"Get allocation data for indexer"
"The Graph network statistics"
"How many indexers are there?"
```

### 3. DeFi Protocol Sorguları
```python
"Uniswap protocol data on Ethereum"
"Show me Aave metrics"
"Compound protocol information"
"DeFi TVL data"
```

### 4. Advanced Blockchain Queries
```python
"Subgraph information for ID xyz"
"Convert subgraph ID to IPFS hash"
"Cross-chain token data"
"Multi-chain protocol comparison"
```

## 🔧 Programmatic Usage

### Direct Tool Calling
```python
from thegraph_mcp_client import TheGraphMCPClient

# Initialize client
client = TheGraphMCPClient("https://token-api.mcp.thegraph.com")
await client.connect()

# Get token data
eth_data = await client.get_token_data("ETH", "ethereum")
print(f"ETH Price: ${eth_data['price_usd']}")

# Get indexer metrics
indexer_data = await client.get_graph_indexer_metrics("0x...")
print(f"Total Stake: {indexer_data['total_stake']} GRT")

# Get DeFi protocol data
uniswap_data = await client.get_defi_protocol_data("uniswap", "ethereum")
print(f"Protocol TVL: ${uniswap_data['tvl_usd']}")
```

### Using Tool Dispatcher
```python
from thegraph_mcp_client import TheGraphToolDispatcher

dispatcher = TheGraphToolDispatcher(client)

# Natural language queries
result = await dispatcher.dispatch_query("What's the ETH price?")
print(result['formatted_response'])
```

## 📊 Veri Kaynakları ve Fallback

### 1. Primary: The Graph MCP Server
- **URL**: `https://token-api.mcp.thegraph.com`
- **Data**: Gerçek zamanlı blockchain verileri
- **Coverage**: Ethereum, Arbitrum, Polygon, Optimism, Base

### 2. Fallback: Maple Nodes API
- **URL**: `https://api.maplenodes.com`
- **Data**: The Graph network metrikleri
- **Coverage**: Indexer, allocation, network statistics

### 3. Emergency Fallback: CoinGecko
- **URL**: `https://api.coingecko.com`
- **Data**: Token fiyat verileri
- **Coverage**: Binlerce token ve coin

## 🛡️ Error Handling

### Connection Failures
```python
# Otomatik fallback sistemi
try:
    result = await client.get_token_data("ETH")
    source = result.get("source")  # "thegraph_mcp", "maple_nodes", or "coingecko"
except Exception as e:
    print(f"All data sources failed: {e}")
```

### Rate Limiting
```python
# Otomatik retry ve backoff
await client.call_tool_with_retry("get_token_data", {"symbol": "ETH"})
```

## 🔍 Troubleshooting

### 1. The Graph MCP Connection Issues
```bash
# Test connection
curl -X GET https://token-api.mcp.thegraph.com/health

# Check logs
tail -f neurotrade_agent.log
```

### 2. Authentication Problems
```bash
# Set API key if required
export THEGRAPH_API_KEY="your_key"

# Test with auth
python test_thegraph_integration.py
```

### 3. Fallback Mode
```bash
# Force fallback mode for testing
export THEGRAPH_MCP_URL="https://invalid-server.example.com"
python mcp_enhanced_agent.py
```

## 📈 Performance Optimizations

### 1. Caching
- Token price data cached for 30 seconds
- Network statistics cached for 5 minutes
- Indexer data cached for 2 minutes

### 2. Concurrent Requests
```python
# Multiple queries in parallel
tasks = [
    client.get_token_data("ETH"),
    client.get_token_data("BTC"),
    client.get_graph_network_info()
]
results = await asyncio.gather(*tasks)
```

### 3. Connection Pooling
- Persistent HTTP connections
- Connection reuse across requests
- Automatic connection recovery

## 🧪 Testing

### Run All Tests
```bash
python test_thegraph_integration.py
```

### Specific Test Categories
```bash
# Test only The Graph MCP connection
python -c "
import asyncio
from test_thegraph_integration import test_thegraph_mcp_client
asyncio.run(test_thegraph_mcp_client())
"

# Test only tool dispatcher
python -c "
import asyncio
from test_thegraph_integration import test_thegraph_tool_dispatcher
asyncio.run(test_thegraph_tool_dispatcher())
"
```

## 🔄 Migration from Test Server

Eğer daha önceki test server'ı kullanıyorsanız:

### 1. Update Configuration
```bash
# Old (test server)
export MCP_SERVER_URL="http://localhost:8080"

# New (The Graph MCP)
export THEGRAPH_MCP_URL="https://token-api.mcp.thegraph.com"
```

### 2. Update Imports
```python
# Old
from mcp_client import MCPClient

# New
from thegraph_mcp_client import TheGraphMCPClient
```

### 3. Update Agent
```bash
# Use new enhanced agent
python mcp_enhanced_agent.py  # Uses The Graph MCP
```

## 📚 Additional Resources

### The Graph Resources
- [The Graph Documentation](https://thegraph.com/docs/)
- [The Graph Explorer](https://thegraph.com/explorer/)
- [The Graph Discord](https://discord.gg/thegraph)

### MCP Protocol
- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)
- [MCP GitHub Repository](https://github.com/modelcontextprotocol)

### API References
- [Maple Nodes API](https://docs.maplenodes.com/)
- [CoinGecko API](https://coingecko.com/api)

## 🎯 Sonuç

NeuroTrade artık **gerçek The Graph MCP server'ına** bağlanarak:

✅ **Gerçek blockchain verileri** kullanır  
✅ **Güvenilir fallback sistemleri** ile kesintisiz hizmet sağlar  
✅ **Akıllı tool routing** ile en doğru veriyi bulur  
✅ **High-performance** concurrent operations destekler  
✅ **Production-ready** error handling ve monitoring içerir  

---

🌐 **NeuroTrade The Graph AI** - *Blockchain Verilerinde Uzman* 