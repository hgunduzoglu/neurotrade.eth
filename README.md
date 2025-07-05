# NeuroTrade.eth - The Graph MCP AI Agent

🚀 **Advanced AI Trading Agent** with real-time blockchain data from The Graph MCP (Model Context Protocol) server.

## 🔥 Features

- 🌐 **Real-time blockchain data** via The Graph MCP SSE connection
- 🤖 **AI-powered trading analysis** with natural language queries
- 📊 **Multi-chain support** (Ethereum, Arbitrum, Polygon, Optimism, Base)
- 🔍 **Advanced indexer metrics** and network statistics
- 💬 **Chat interface** with AgentChatProtocol v0.3.0
- 📈 **Token price tracking** with fallback systems
- 🎯 **Smart query dispatcher** for optimal tool selection

## 🛠️ Architecture

```
User Query → Agent → The Graph MCP (SSE) → Indexer/Token Data → AI Analysis → Response
                        ↓ (fallback)
                   CoinGecko API
```

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/neurotrade.eth.git
cd neurotrade.eth
```

### 2. Environment Setup
```bash
# Copy template and add your JWT token
cp env_template.txt .env

# Edit .env and add your JWT token:
# GRAPH_JWT=eyJhbGciOiJLTVNFUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Test Connection
```bash
# Quick test
python quick_mcp_test.py

# Comprehensive test
cd neurotrade_ai_agent
python test_graph_mcp.py
```

### 5. Run Agent
```bash
cd neurotrade_ai_agent
python neurotrade_agent.py
```

## 🔧 The Graph MCP Integration

### SSE Connection
- **Endpoint**: `https://token-api.mcp.thegraph.com/sse`
- **Protocol**: Server-Sent Events (SSE)
- **Authentication**: JWT Bearer token

### Available Tools
- `get_token_data` - Token information and pricing
- `get_indexer_info` - Indexer metrics and performance
- `get_allocations` - Allocation data for indexers
- `get_network_stats` - The Graph network statistics

### Query Examples
```python
# Token queries
"ETH token data"
"What's the price of USDC?"

# Indexer queries
"Show me indexer information"
"Get indexer metrics"

# Network queries
"The Graph network statistics"
"Network stats"

# Allocation queries
"Show allocation data"
"Get allocations for indexer"
```

## 💬 Chat Interface

The agent supports natural language queries through the chat interface:

```
🤖 NeuroTrade AI: Hello! I can help you with:
• Token prices and data
• The Graph indexer information
• Network statistics
• Allocation data
• Trading analysis

User: "Show me ETH price"
🤖 NeuroTrade AI: 💰 **Token Data**
Current ETH price: $2,547.32
24h change: +2.4%
Network: Ethereum
Source: The Graph MCP
```

## 🧪 Testing

### Quick Connection Test
```bash
python quick_mcp_test.py
```

### Comprehensive Test Suite
```bash
cd neurotrade_ai_agent
python test_graph_mcp.py
```

### Interactive Testing
```bash
# Run interactive test mode
python test_graph_mcp.py
# Select option 3 for interactive mode
```

## 📊 Data Sources

1. **Primary**: The Graph MCP Server
   - Real-time blockchain data
   - Indexer metrics
   - Network statistics

2. **Fallback**: CoinGecko API
   - Token prices
   - Market data
   - Emergency fallback

## 🔒 Security

- JWT token authentication
- Secure SSE connections
- Error handling with fallbacks
- Rate limiting protection

## 📈 Performance

- Persistent SSE connections
- Efficient tool dispatch
- Caching for frequent queries
- Parallel data fetching

## 🛡️ Error Handling

The agent includes comprehensive error handling:

- **Connection failures**: Automatic fallback to CoinGecko
- **JWT expiration**: Clear error messages
- **Tool unavailable**: Graceful degradation
- **Rate limiting**: Automatic retry with backoff

## 🔧 Configuration

### Environment Variables
```bash
# Required
GRAPH_JWT=your_jwt_token

# Optional
AGENT_SEED=neurotrade_ai_agent_seed_2024
AGENT_PORT=8001
USE_AGENTVERSE=true
```

### Advanced Configuration
```python
# Custom MCP server URL
GRAPH_MCP_URL="https://token-api.mcp.thegraph.com"
GRAPH_MCP_SSE_URL="https://token-api.mcp.thegraph.com/sse"
```

## 📚 API Reference

### GraphMCPClient
```python
from graph_mcp_client import GraphMCPClient

client = GraphMCPClient()
await client.initialize_session()  # Start SSE connection
tools = await client.list_tools()  # Get available tools
result = await client.call_tool("get_token_data", {"symbol": "ETH"})
await client.close()  # Clean up
```

### GraphMCPQueryDispatcher
```python
from graph_mcp_client import GraphMCPQueryDispatcher

dispatcher = GraphMCPQueryDispatcher(client)
response = await dispatcher.dispatch_query("ETH price")
```

## 🐛 Troubleshooting

### Common Issues

1. **JWT Token Not Found**
   ```bash
   ❌ GRAPH_JWT not found in environment!
   💡 Add your JWT token to .env file
   ```

2. **SSE Connection Failed**
   ```bash
   ❌ SSE connection failed - check your JWT token
   💡 Verify token is valid and not expired
   ```

3. **No Tools Available**
   ```bash
   ❌ No tools found
   💡 Check MCP server status and JWT permissions
   ```

### Debug Mode
```bash
# Enable debug logging
export PYTHONPATH=.
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
# Run your tests
"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🔗 Links

- [The Graph](https://thegraph.com/)
- [The Graph MCP Documentation](https://docs.thegraph.com/mcp/)
- [uAgents Framework](https://github.com/fetchai/uAgents)
- [MCP Protocol](https://modelcontextprotocol.io/)

---

**NeuroTrade.eth** - Powered by The Graph MCP 🚀