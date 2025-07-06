# NeuroTrade.eth - AI Trading Agent Integration

🚀 **Complete AI Trading Assistant with Frontend Integration**

This project integrates a sophisticated AI trading agent with a Next.js frontend, providing real-time trading analysis, market insights, and personalized trading recommendations.

## 🌟 Features

### AI Agent Capabilities
- **Real-time Price Analysis** - Live market data from CryptoCompare API
- **Historical Data Analysis** - 30-day historical analysis with technical indicators
- **Trading Signals** - Buy/Sell/Hold recommendations with confidence levels
- **Risk Assessment** - Volatility, liquidity, and market cap risk analysis
- **Multi-token Support** - BTC, ETH, USDC, USDT, BNB, SOL, ADA, DOT, MATIC, AVAX, LINK, UNI, AAVE, COMP, MKR
- **Batch Analysis** - Analyze multiple tokens simultaneously
- **Market Sentiment** - AI-powered sentiment scoring

### Frontend Features
- **Interactive Chat Interface** - Real-time communication with AI agent
- **Connection Status** - Visual indicator of AI agent connectivity
- **Quick Questions** - Pre-defined queries for common trading scenarios
- **Modern UI** - Glassmorphism design with smooth animations
- **Responsive Design** - Works on desktop and mobile devices
- **Real-time Updates** - Live data feeds and instant responses

### Technical Architecture
- **FastAPI Backend** - RESTful API with WebSocket support
- **Next.js Frontend** - Server-side rendering with TypeScript
- **Real-time Communication** - WebSocket connections for instant messaging
- **Data Consistency** - Unified data sources across frontend and AI agent
- **Error Handling** - Comprehensive error handling and fallback mechanisms
- **Session Management** - User session tracking and management

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Easy Launch (Recommended)
Use the provided launcher script to start both services:

```bash
# Make the launcher executable (Linux/Mac)
chmod +x start_neurotrade.py

# Run the launcher
python start_neurotrade.py
```

The launcher will:
1. ✅ Check dependencies (Python, Node.js, npm)
2. 🔧 Install Python dependencies
3. 🔧 Install Node.js dependencies  
4. 🤖 Start AI Agent API Bridge (port 8002)
5. 🌐 Start Frontend (port 3000)

### Manual Setup

#### 1. Install Python Dependencies
```bash
cd neurotrade_ai_agent
pip install -r requirements.txt
```

#### 2. Install Node.js Dependencies
```bash
npm install
```

#### 3. Start AI Agent API Bridge
```bash
cd neurotrade_ai_agent
python -m uvicorn api_bridge:app --host 0.0.0.0 --port 8002 --reload
```

#### 4. Start Frontend
```bash
npm run dev
```

## 🎯 Usage

### Accessing the Application
- **Frontend**: http://localhost:3000
- **AI Agent API**: http://localhost:8002
- **API Documentation**: http://localhost:8002/docs

### Chat Interface
The homepage features an integrated chat interface where you can:

#### Quick Trading Queries
- "What's ETH price?" - Get current price analysis
- "Should I buy BTC?" - Receive buy/sell recommendations
- "Market overview" - Get overall market sentiment
- "ETH vs BTC analysis" - Compare multiple tokens

#### Advanced Queries
- "I have 1 ETH and 1000 USDC, what should I do?" - Portfolio recommendations
- "Is it a good time to swap ETH to USDC?" - Swap timing analysis
- "What's the risk of buying SOL right now?" - Risk assessment
- "Give me a trading signal for MATIC" - Technical analysis

### API Endpoints

#### Chat Endpoint
```bash
POST /chat
{
    "message": "What's ETH price?",
    "symbols": ["ETH"],
    "user_id": "optional"
}
```

#### Token Analysis
```bash
POST /analyze/ETH
```

#### Batch Analysis
```bash
POST /batch-analyze
{
    "symbols": ["BTC", "ETH", "SOL"]
}
```

#### Health Check
```bash
GET /health
```

## 🏗️ Architecture

### Data Flow
1. **Frontend** → User enters query in chat interface
2. **AI Service** → Processes query and sends to API bridge
3. **API Bridge** → Routes request to enhanced AI agent
4. **Enhanced AI Agent** → Analyzes query and fetches market data
5. **Data Service** → Retrieves real-time and historical data
6. **AI Agent** → Generates intelligent response with trading insights
7. **Frontend** → Displays formatted response to user

### Key Components

#### Frontend (`src/`)
- **`components/AIChat.tsx`** - Main chat interface component
- **`services/aiService.ts`** - AI agent communication service
- **`pages/homepage.tsx`** - Homepage with integrated chat
- **`styles/AIChat.module.css`** - Chat interface styles

#### AI Agent (`neurotrade_ai_agent/`)
- **`api_bridge.py`** - FastAPI service for frontend communication
- **`enhanced_ai_agent.py`** - Sophisticated trading analysis engine
- **`enhanced_data_service.py`** - Unified data fetching and processing
- **`*_chat_protocol.py`** - Multiple protocol implementations

### Technical Features

#### Data Sources
- **CryptoCompare API** - Real-time and historical price data
- **Technical Indicators** - RSI, SMA, volatility, momentum
- **Market Sentiment** - AI-powered sentiment analysis
- **Risk Metrics** - Volatility, liquidity, market cap analysis

#### AI Capabilities
- **Multi-token Analysis** - Support for 15+ major cryptocurrencies
- **Confidence Scoring** - Each recommendation includes confidence level
- **Risk Assessment** - Comprehensive risk analysis across multiple factors
- **Trading Signals** - Clear buy/sell/hold recommendations
- **Portfolio Analysis** - Personalized portfolio recommendations

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the `neurotrade_ai_agent/` directory:

```env
# API Configuration
CRYPTOCOMPARE_API_KEY=your_api_key_here
AGENTVERSE_MAILBOX=your_mailbox_address

# Agent Configuration
AGENT_SEED=your_agent_seed
AGENT_ADDRESS=your_agent_address
```

### API Keys
- **CryptoCompare API**: Free tier available at https://cryptocompare.com/api
- **Agentverse**: Optional, for hosted agent deployment

## 🎨 Customization

### Adding New Tokens
Edit `enhanced_ai_agent.py` to add new supported tokens:

```python
self.supported_tokens = [
    "BTC", "ETH", "USDC", "USDT", "BNB", "SOL", "ADA", "DOT", 
    "MATIC", "AVAX", "LINK", "UNI", "AAVE", "COMP", "MKR",
    "YOUR_NEW_TOKEN"  # Add here
]
```

### Custom Analysis Logic
Modify `enhanced_ai_agent.py` to add custom trading strategies:

```python
async def your_custom_analysis(self, symbol: str):
    # Your custom analysis logic
    pass
```

### UI Customization
Modify `src/styles/AIChat.module.css` to customize the chat interface appearance.

## 📊 API Documentation

### Response Formats

#### Chat Response
```json
{
    "response": "Based on current market data, ETH is trading at $2,456...",
    "timestamp": "2024-01-15T10:30:00Z",
    "symbols_analyzed": ["ETH"],
    "analysis_type": "price_analysis",
    "success": true
}
```

#### Token Analysis Response
```json
{
    "symbol": "ETH",
    "analysis": {
        "current_price": 2456.78,
        "price_change_24h": -2.34,
        "trading_signal": "HOLD",
        "confidence": 0.75,
        "risk_level": "MEDIUM",
        "recommendation": "Current market conditions suggest...",
        "technical_indicators": {
            "rsi": 45.6,
            "sma_20": 2450.0,
            "volatility": 0.12
        }
    },
    "timestamp": "2024-01-15T10:30:00Z",
    "success": true
}
```

## 🚀 Deployment

### Production Deployment
1. **Frontend**: Deploy to Vercel, Netlify, or any static hosting
2. **AI Agent**: Deploy to cloud servers (AWS, GCP, Azure)
3. **Environment**: Use production environment variables
4. **SSL**: Enable HTTPS for secure communication

### Docker Deployment
```dockerfile
# Example Dockerfile for AI Agent
FROM python:3.9-slim
COPY neurotrade_ai_agent/ /app/
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["uvicorn", "api_bridge:app", "--host", "0.0.0.0", "--port", "8002"]
```

## 🛠️ Development

### Testing
```bash
# Test AI Agent
cd neurotrade_ai_agent
python -m pytest tests/

# Test Frontend
npm test
```

### Debugging
- **AI Agent Logs**: Check console output for API bridge
- **Frontend Logs**: Check browser console for frontend issues
- **API Testing**: Use http://localhost:8002/docs for API testing

## 🎯 Hackathon Features

This integration provides everything needed for a hackathon demo:

### Demo Flow
1. **Homepage** - Show the integrated chat interface
2. **Live Chat** - Demonstrate real-time AI communication
3. **Trading Analysis** - Show sophisticated market analysis
4. **Multi-token Support** - Demonstrate batch analysis
5. **Real-time Data** - Show live market data integration

### Key Demo Points
- ✅ **Full Integration** - Frontend and AI agent working together
- ✅ **Real-time Data** - Live market data from CryptoCompare
- ✅ **Sophisticated AI** - Advanced trading analysis and recommendations
- ✅ **Professional UI** - Modern, responsive design
- ✅ **Multiple Protocols** - Various chat protocol implementations
- ✅ **Scalable Architecture** - Production-ready design

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Check the API documentation at http://localhost:8002/docs
- Review the console logs for error messages
- Ensure all dependencies are installed correctly

---

**Happy Trading! 🚀📈** 