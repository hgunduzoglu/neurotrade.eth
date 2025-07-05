# NeuroTrade AI Agent 🤖

An AI-powered trading agent built with Fetch.AI uAgents framework that provides intelligent trading recommendations and market analysis. **Now with full ASI:One Chat Protocol support!**

## 🚀 Features

- **🗣️ ASI:One Chat Protocol**: Full natural language chat support through ASI:One interface
- **🤖 AI-Powered Trading Recommendations**: Analyzes market data and provides intelligent trading suggestions
- **🌐 Multi-Chain Support**: Supports Ethereum, Arbitrum, Polygon, Optimism, and Base networks
- **📊 The Graph Integration**: Fetches real-time blockchain data for accurate market analysis
- **🔄 Cross-Chain Analysis**: Provides recommendations for cross-chain trading opportunities
- **🌍 ASI:One Compatible**: Discoverable and chattable through https://asi1.ai for real users
- **⏰ Real-Time Market Data**: Continuously updates market prices and trends
- **🧠 Structured Output Processing**: Uses OpenAI agent for intelligent query parameter extraction

## 🛠️ Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager
- Internet connection for API calls

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/neurotrade.eth.git
   cd neurotrade.eth
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   **Dependencies include:**
   - `uagents`: Core agent framework
   - `uagents-core`: Chat protocol support
   - `aiohttp`: HTTP client for API calls
   - `requests`: HTTP requests library
   - `python-dotenv`: Environment variable management

3. **Configure environment variables (optional):**
   
   Create a `.env` file in the root directory:
   ```env
   AGENT_SEED=neurotrade_ai_agent_seed_2024
   AGENT_PORT=8000
   LOG_LEVEL=INFO
   USE_AGENTVERSE=true
   ```

   - `AGENT_SEED`: Unique seed for your agent (can be customized)
   - `AGENT_PORT`: Port for the agent to run on (default: 8000)
   - `USE_AGENTVERSE`: Enable Agentverse hosting (default: true)

4. **No Additional Setup Required:**
   - No mailbox key needed
   - Agent automatically configured for Agentverse hosting
   - "Chat with Agent" button will appear automatically

## 🎯 Usage

### Running the Agent

```bash
python neurotrade_agent.py
```

The agent will start and automatically:
- Connect to Agentverse for mailbox communication
- Register on the Almanac contract for ASI:One discovery
- Begin fetching market data every 5 minutes
- Accept trading queries from users

### Supported Queries

The NeuroTrade AI Agent can handle various types of trading queries:

**Price Analysis:**
- "What's the current ETH price?"
- "Analyze ETH market conditions"

**Buy/Sell Recommendations:**
- "Should I buy ETH now?"
- "Is it a good time to sell?"
- "Give me a buy signal for USDC"

**Swap Analysis:**
- "Should I swap USDC to ETH?"
- "Analyze ETH/USDC swap opportunity"

**Cross-Chain Operations:**
- "Cross-chain trading from Base to Arbitrum"
- "Best chain for ETH trading"

### Example Interactions

```python
# Example query to the agent
{
    "query": "Should I buy ETH now?",
    "chain": "ethereum"
}

# Example response
{
    "agent": "NeuroTrade AI Agent",
    "query": "Should I buy ETH now?",
    "recommendation": "🔵 ETH Analysis: Based on current market conditions, ETH shows strong fundamentals. Consider dollar-cost averaging for entry.",
    "market_data": {
        "eth_price": 2456.78,
        "timestamp": "2024-01-15T10:30:00",
        "chain": "ethereum"
    },
    "timestamp": "2024-01-15T10:30:00",
    "chain": "ethereum"
}
```

## 🔗 ASI:One Chat Integration

**🎉 NEW: Full Chat Protocol Support!**

The agent now supports full natural language conversation through ASI:One's chat interface:

### 💬 How to Chat with NeuroTrade AI

1. **Visit ASI:One:** https://asi1.ai
2. **Enable Agents:** Toggle the "Agents" switch on
3. **Search:** Look for "NeuroTrade" or search "trading"
4. **Start Chatting:** Ask questions in natural language!

### 🗣️ Natural Language Examples

**Instead of structured queries, just ask naturally:**

- ❓ "What's the current price of Ethereum?"
- ❓ "Should I buy ETH right now given market conditions?"
- ❓ "I want to swap 1000 USDC to ETH, is this a good time?"
- ❓ "Which blockchain has the best liquidity for trading ETH?"
- ❓ "Give me analysis on cross-chain trading opportunities"
- ❓ "Is the crypto market bullish or bearish today?"

### 🤖 Chat Features

- **🧠 Smart Parameter Extraction**: Uses OpenAI agent to understand your intent
- **📝 Structured Responses**: Get formatted, easy-to-read trading analysis
- **💬 Session Management**: Maintains conversation context
- **🚀 Real-time Processing**: Live market data in every response
- **🌍 Multi-language Support**: Ask questions naturally

### 🔄 Chat Flow

1. **You ask:** "Should I buy ETH now?"
2. **AI processes:** Extracts intent and parameters
3. **Market analysis:** Fetches live ETH price and market data
4. **Smart response:** Returns formatted trading recommendation
5. **Interactive:** Continue the conversation with follow-up questions

## 📊 The Graph Integration

The agent integrates with The Graph Protocol to fetch real-time blockchain data:

- **Token Prices**: Real-time token pricing data
- **Pool Liquidity**: DEX liquidity information
- **Trading Volume**: Market activity metrics
- **Multi-Chain Data**: Support for multiple blockchain networks

## 🔧 Technical Architecture

```
NeuroTrade AI Agent
├── neurotrade_agent.py     # Main agent implementation
├── chat_protocol.py        # ASI:One chat protocol handler
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
├── test_agent.py           # Testing utilities
├── setup.py                # Installation script
└── README.md              # This documentation
```

### Key Components

1. **Agent Core**: Built on Fetch.AI uAgents framework
2. **Chat Protocol Handler**: Processes natural language queries from ASI:One
3. **Trading Data Manager**: Handles market data fetching and analysis
4. **AI Recommendation Engine**: Generates trading recommendations
5. **Structured Output Client**: Interfaces with OpenAI agent for parameter extraction
6. **The Graph Client**: Fetches blockchain data via GraphQL
7. **Multi-Protocol Support**: Handles both direct API calls and chat messages

## 🌐 Supported Networks

- **Ethereum**: Main network for ETH and ERC-20 tokens
- **Arbitrum**: Layer 2 solution for faster, cheaper transactions
- **Polygon**: Scalable blockchain for DeFi applications
- **Optimism**: Ethereum Layer 2 for reduced gas fees
- **Base**: Coinbase's Layer 2 solution

## 📈 AI Capabilities

The agent provides:

- **Market Trend Analysis**: Identifies bullish/bearish market conditions
- **Volume Analysis**: Assesses trading activity levels
- **Risk Assessment**: Evaluates trading risks
- **Timing Recommendations**: Suggests optimal entry/exit points
- **Cross-Chain Opportunities**: Identifies arbitrage possibilities

## 🔐 Security Features

- **Secure Messaging**: All communications are cryptographically secured
- **Wallet Protection**: Agent wallet addresses are protected
- **API Rate Limiting**: Prevents abuse and ensures stability
- **Error Handling**: Robust error handling for reliable operation

## 🚨 Disclaimer

This AI agent provides trading suggestions for educational and informational purposes only. It is not financial advice. Always do your own research and consider consulting with a financial advisor before making trading decisions.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🧪 Testing

### Running Tests

1. **Simple Chat Protocol Tests (Recommended):**
   ```bash
   python test_simple_chat.py
   ```
   This tests the simple chat protocol that avoids the "locked protocol" error.

2. **Agent Functionality Tests:**
   ```bash
   python test_agent.py
   ```
   Tests the core agent functionality and trading features.

3. **Legacy Chat Protocol Tests:**
   ```bash
   python test_chat_protocol.py
   ```
   **Note**: If you encounter "Cannot add interaction to locked protocol" errors, use the simple chat protocol instead.

### Troubleshooting Common Issues

**"Locked Protocol" Error:**
- This occurs when trying to modify an already registered protocol
- Solution: Use the simple chat protocol (`simple_chat_protocol.py`) instead
- The agent automatically loads the simple chat protocol for compatibility

**Import Errors:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version compatibility (3.10+ required)

**Connection Issues:**
- Check internet connection for API calls
- Ensure port 8000 is available or change `AGENT_PORT` in `.env`
- Verify endpoint is set to `https://agentverse.ai/v1/submit`

**Agent Not Showing as "Hosted":**
- Ensure `mailbox=True` is set
- Check that endpoint points to Agentverse
- Restart the agent completely

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For support or questions:
- Open an issue on GitHub
- Contact via ASI:One platform
- Email: support@neurotrade.eth

## 🏆 Hackathon Submission

This agent was developed for the Fetch.AI hackathon and meets all requirements:
- ✅ Built with uAgents framework
- ✅ Hosted on Agentverse.ai
- ✅ Discoverable on ASI:One
- ✅ Uses Agent Chat Protocol
- ✅ Registered on Almanac contract
- ✅ Public GitHub repository
- ✅ Comprehensive documentation

---

**Built with ❤️ using Fetch.AI uAgents** 