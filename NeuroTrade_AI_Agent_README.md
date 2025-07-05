# NeuroTrade AI Agent 🤖

An AI-powered trading agent built with Fetch.AI uAgents framework that provides intelligent trading recommendations and market analysis.

## 🚀 Features

- **AI-Powered Trading Recommendations**: Analyzes market data and provides intelligent trading suggestions
- **Multi-Chain Support**: Supports Ethereum, Arbitrum, Polygon, Optimism, and Base networks
- **The Graph Integration**: Fetches real-time blockchain data for accurate market analysis
- **Cross-Chain Analysis**: Provides recommendations for cross-chain trading opportunities
- **ASI:One Compatible**: Discoverable through https://asi1.ai for real users
- **Real-Time Market Data**: Continuously updates market prices and trends

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

3. **Configure environment variables:**
   
   Create a `.env` file in the root directory:
   ```env
   AGENT_MAILBOX_KEY=your_mailbox_key_here
   AGENT_SEED=neurotrade_ai_agent_seed_2024
   AGENT_PORT=8000
   LOG_LEVEL=INFO
   ```

   - `AGENT_MAILBOX_KEY`: Your Agentverse mailbox key (required for ASI:One discovery)
   - `AGENT_SEED`: Unique seed for your agent (can be customized)
   - `AGENT_PORT`: Port for the agent to run on (default: 8000)

4. **Get your Agentverse Mailbox Key:**
   - Visit [Agentverse.ai](https://agentverse.ai)
   - Create an account and get your mailbox key
   - Add it to your `.env` file

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

## 🔗 ASI:One Integration

The agent is designed to be discoverable on ASI:One at https://asi1.ai. Users can:

1. Visit ASI:One platform
2. Search for "NeuroTrade" or "trading"
3. Connect to the agent
4. Start asking trading-related questions
5. Receive AI-powered recommendations

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
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
└── README.md              # This documentation
```

### Key Components

1. **Agent Core**: Built on Fetch.AI uAgents framework
2. **Trading Data Manager**: Handles market data fetching and analysis
3. **AI Recommendation Engine**: Generates trading recommendations
4. **Protocol Handler**: Manages message routing and responses
5. **The Graph Client**: Fetches blockchain data via GraphQL

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