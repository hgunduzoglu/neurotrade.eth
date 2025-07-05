# NeuroTrade.eth - Test & Usage Guide

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Copy template and add your JWT token
cp env_template.txt .env

# Edit .env file:
# GRAPH_JWT=eyJhbGciOiJLTVNFUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Test Connection
```bash
# Quick connection test
python quick_mcp_test.py

# Comprehensive test suite
cd neurotrade_ai_agent
python test_graph_mcp.py
```

### 4. Run Agent
```bash
cd neurotrade_ai_agent
python neurotrade_agent.py
```

## 🧪 Testing Options

### Option 1: Quick Connection Test
```bash
python quick_mcp_test.py
```
**What it does:**
- Checks JWT token
- Tests SSE connection to The Graph MCP
- Lists available tools
- Tests first tool call

### Option 2: Comprehensive Test Suite
```bash
cd neurotrade_ai_agent
python test_graph_mcp.py
```
**Test modes:**
1. **Connection test** - Full SSE connection and tool testing
2. **Query dispatcher test** - Natural language query processing
3. **Interactive test** - Manual query testing
4. **All tests** - Complete test suite

### Option 3: Interactive Testing
```bash
cd neurotrade_ai_agent
python test_graph_mcp.py
# Select option 3 for interactive mode
```

## 📊 Expected Results

### ✅ Successful Connection
```
🧪 Testing The Graph MCP SSE Connection
✅ JWT Token found: eyJhbGciOiJLTVNFUzI1NiIsInR5cCI6IkpXVCJ9...
📡 Connecting to https://token-api.mcp.thegraph.com/sse ...
✅ SSE connection successful!
Session ID: abc123...
✅ Found 4 tools:
   • get_token_data
   • get_indexer_info  
   • get_allocations
   • get_network_stats
```

### ❌ Common Issues

#### JWT Token Missing
```
❌ GRAPH_JWT not found in environment!
💡 Steps to fix:
   1. Copy env_template.txt to .env
   2. Add your JWT token to GRAPH_JWT in .env
   3. Run this test again
```

#### JWT Token Invalid
```
❌ SSE connection failed - check your JWT token
💡 Verify token is valid and not expired
```

#### Connection Issues
```
❌ Connection failed: [Errno 11001] getaddrinfo failed
💡 Check your internet connection
```

## 🤖 Using the Agent

### Starting the Agent
```bash
cd neurotrade_ai_agent
python neurotrade_agent.py
```

### Expected Output
```
🚀 Official Chat Protocol loaded successfully!
🎯 Protocol: AgentChatProtocol v0.3.0 with The Graph MCP
✅ Agent should now show 'Chat with Agent' button!
💬 Full chat functionality enabled!
🔗 The Graph MCP integration ready!
🔥 Starting NeuroTrade.eth AI Agent...
Agent Address: agent1q...
📡 Connecting to Agentverse...
```

### Chat Queries
Once running, you can chat with the agent using:

**Token Queries:**
- "ETH token data"
- "What's the price of USDC?"
- "Show me token information"

**Indexer Queries:**
- "Show me indexer information"
- "Get indexer metrics"
- "Indexer performance data"

**Network Queries:**
- "The Graph network statistics"
- "Network stats"
- "Show network data"

**Allocation Queries:**
- "Show allocation data"
- "Get allocations"
- "Allocation information"

## 🔧 Troubleshooting

### Debug Mode
```bash
# Enable detailed logging
export PYTHONPATH=.
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
import asyncio
from neurotrade_ai_agent.graph_mcp_client import test_graph_mcp_connection
asyncio.run(test_graph_mcp_connection())
"
```

### Manual JWT Test
```bash
# Test JWT token manually
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Accept: text/event-stream" \
     https://token-api.mcp.thegraph.com/sse
```

### Environment Check
```bash
# Check Python version (3.8+ required)
python --version

# Check dependencies
pip list | grep -E "(aiohttp|uagents|python-dotenv)"

# Check .env file
cat .env
```

## 📈 Performance Tips

### For Best Results:
1. **Stable Internet**: SSE requires stable connection
2. **Valid JWT**: Ensure token is not expired
3. **Python 3.8+**: Use recent Python version
4. **Clean Environment**: Fresh virtual environment recommended

### Monitoring:
```bash
# Monitor agent logs
tail -f neurotrade_agent.log

# Monitor system resources
top -p $(pgrep -f neurotrade_agent.py)
```

## 🚀 Production Deployment

### Environment Variables
```bash
# Production .env
GRAPH_JWT=your_production_jwt_token
AGENT_SEED=unique_production_seed
AGENT_PORT=8001
USE_AGENTVERSE=true
```

### Service Setup
```bash
# Create systemd service
sudo tee /etc/systemd/system/neurotrade.service > /dev/null <<EOF
[Unit]
Description=NeuroTrade AI Agent
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/neurotrade.eth/neurotrade_ai_agent
ExecStart=/usr/bin/python3 neurotrade_agent.py
Restart=always
RestartSec=5
Environment=PYTHONPATH=/path/to/neurotrade.eth

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl enable neurotrade
sudo systemctl start neurotrade
sudo systemctl status neurotrade
```

## 📞 Support

### Getting Help:
1. Check this guide first
2. Run test suite for diagnostics
3. Check logs for error messages
4. Verify JWT token validity

### Common Commands:
```bash
# Full diagnostic
python quick_mcp_test.py && cd neurotrade_ai_agent && python test_graph_mcp.py

# Reset and restart
rm -rf __pycache__ && python neurotrade_agent.py

# Check agent status
ps aux | grep neurotrade_agent
```

---

**NeuroTrade.eth** - The Graph MCP AI Agent 🚀 