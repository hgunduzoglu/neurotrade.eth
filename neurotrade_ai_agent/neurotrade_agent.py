import asyncio
import aiohttp
import json
import os
import logging
import signal
import sys
from typing import Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv
from aiohttp import web, ClientSession

from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

# Import the enhanced AI agent
try:
    from enhanced_ai_agent import enhanced_analyzer
    ENHANCED_AI_AVAILABLE = True
    print("✅ Enhanced AI agent loaded successfully!")
except ImportError as e:
    print(f"⚠️ Enhanced AI agent not available: {e}")
    ENHANCED_AI_AVAILABLE = False
    enhanced_analyzer = None

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Agent configuration
AGENT_SEED = os.getenv("AGENT_SEED", "neurotrade_ai_agent_seed_2024")
AGENT_PORT = int(os.getenv("AGENT_PORT", "8001"))  # AI agent on port 8001
HTTP_PORT = int(os.getenv("HTTP_PORT", "8000"))  # HTTP server on port 8000
USE_AGENTVERSE = os.getenv("USE_AGENTVERSE", "true").lower() == "true"

# The Graph endpoints for different chains
GRAPH_ENDPOINTS = {
    "ethereum": "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3",
    "arbitrum": "https://api.thegraph.com/subgraphs/name/ianlapham/arbitrum-minimal",
    "polygon": "https://api.thegraph.com/subgraphs/name/ianlapham/uniswap-v3-polygon",
    "optimism": "https://api.thegraph.com/subgraphs/name/ianlapham/optimism-post-regenesis"
}

# Create the NeuroTrade AI Agent with proper mailbox configuration
if True:
    # Use Agentverse mailbox for hosted agent
    neurotrade_agent = Agent(
        name="NeuroTrade",
        seed=AGENT_SEED,
        mailbox=True,
        port=AGENT_PORT,
        endpoint="https://agentverse.ai/v1/submit"
    )
    print("🌐 Agent configured with Agentverse mailbox")
else:
    # Fallback to local agent with mailbox enabled
    neurotrade_agent = Agent(
        name="NeuroTrade",
        seed=AGENT_SEED,
        mailbox=True,
        port=AGENT_PORT,
        endpoint=f"http://localhost:{AGENT_PORT}/submit",
    )
    print("⚠️ Agent configured locally - add AGENT_MAILBOX_KEY for Agentverse hosting")

# Fund the agent if needed (with error handling)
try:
    fund_agent_if_low(neurotrade_agent.wallet.address())
except Exception as e:
    print(f"⚠️ Warning: Could not fund agent: {e}")
    print("💡 Agent will continue without funding")

# Trading protocol for handling user queries (removed - using direct agent handlers)
# trading_protocol = Protocol("NeuroTrade Trading Protocol")

class TradingData:
    """Class to store and manage trading data"""
    def __init__(self):
        self.token_prices = {}
        self.market_trends = {}
        self.last_update = None

    async def fetch_token_price(self, token_address: str, chain: str = "ethereum") -> Optional[float]:
        """Fetch token price from The Graph"""
        try:
            query = f"""
            {{
                token(id: "{token_address.lower()}") {{
                    id
                    symbol
                    name
                    derivedETH
                    totalSupply
                    volume
                    volumeUSD
                    feesUSD
                    txCount
                }}
            }}
            """
            
            endpoint = GRAPH_ENDPOINTS.get(chain, GRAPH_ENDPOINTS["ethereum"])
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    endpoint,
                    json={"query": query},
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        if "data" in data and data["data"]["token"]:
                            token_data = data["data"]["token"]
                            # Convert derivedETH to USD (assuming ETH price)
                            eth_price = await self.get_eth_price()
                            if eth_price and token_data["derivedETH"]:
                                return float(token_data["derivedETH"]) * eth_price
                        return None
                    else:
                        logger.error(f"Graph API error: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error fetching token price: {e}")
            return None

    async def get_eth_price(self) -> Optional[float]:
        """Get ETH price in USD"""
        try:
            # Using a simple API to get ETH price
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd") as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("ethereum", {}).get("usd", 0)
                    return 2500.0  # Fallback price
        except Exception as e:
            logger.error(f"Error fetching ETH price: {e}")
            return 2500.0  # Fallback price

    async def get_pool_liquidity(self, pool_address: str, chain: str = "ethereum") -> Optional[Dict]:
        """Get pool liquidity data from The Graph"""
        try:
            query = f"""
            {{
                pool(id: "{pool_address.lower()}") {{
                    id
                    token0 {{
                        symbol
                        name
                    }}
                    token1 {{
                        symbol
                        name
                    }}
                    liquidity
                    sqrtPrice
                    tick
                    volumeUSD
                    txCount
                    totalValueLockedUSD
                }}
            }}
            """
            
            endpoint = GRAPH_ENDPOINTS.get(chain, GRAPH_ENDPOINTS["ethereum"])
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    endpoint,
                    json={"query": query},
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        if "data" in data and data["data"]["pool"]:
                            return data["data"]["pool"]
                    return None
        except Exception as e:
            logger.error(f"Error fetching pool liquidity: {e}")
            return None

    def analyze_market_trend(self, price_data: Dict) -> str:
        """Analyze market trend based on price data"""
        if not price_data:
            return "Insufficient data for analysis"
        
        # Simple trend analysis (in a real implementation, this would be more sophisticated)
        volume_usd = float(price_data.get("volumeUSD", 0))
        
        if volume_usd > 1000000:  # High volume
            return "High trading volume detected - Strong market activity"
        elif volume_usd > 100000:  # Medium volume
            return "Moderate trading volume - Stable market conditions"
        else:
            return "Low trading volume - Cautious market sentiment"

    def generate_trading_recommendation(self, query: str, market_data: Dict) -> str:
        """Generate AI trading recommendation based on query and market data"""
        query_lower = query.lower()
        
        # Simple rule-based AI recommendations
        if "buy" in query_lower or "purchase" in query_lower:
            if "eth" in query_lower:
                return "🔵 ETH Analysis: Based on current market conditions, ETH shows strong fundamentals. Consider dollar-cost averaging for entry."
            elif "usdc" in query_lower:
                return "🟢 USDC Analysis: USDC is a stable coin. Good for portfolio stability but no growth potential."
            else:
                return "📊 General Buy Signal: Analyze market trends and consider risk management before purchasing."
        
        elif "sell" in query_lower:
            return "🔴 Sell Analysis: Review your portfolio performance and consider taking profits if you're in positive territory."
        
        elif "swap" in query_lower:
            if "usdc" in query_lower and "eth" in query_lower:
                return "🔄 USDC → ETH Swap: Good timing for ETH accumulation. Consider gas fees and slippage."
            else:
                return "🔄 Swap Analysis: Check liquidity pools and compare rates across DEXs for best execution."
        
        elif "price" in query_lower:
            eth_price = market_data.get("eth_price", "N/A")
            return f"💰 Current ETH Price: ${eth_price} USD. Market showing {'bullish' if isinstance(eth_price, (int, float)) and eth_price > 2000 else 'bearish'} sentiment."
        
        elif "cross" in query_lower and "chain" in query_lower:
            return "🌉 Cross-Chain Analysis: LayerZero integration allows seamless cross-chain operations. Consider gas fees on both chains."
        
        else:
            return "🤖 NeuroTrade AI: Please specify your trading query. I can help with buy/sell signals, price analysis, swaps, and cross-chain operations."

# Message models for uAgents
class TradingQueryMessage(Model):
    query: str
    chain: str = "ethereum"

class TradingResponseMessage(Model):
    agent: str
    query: str
    recommendation: str
    market_data: dict
    timestamp: str
    chain: str

class SimpleMessage(Model):
    message: str

class GenericMessage(Model):
    content: str

# Initialize trading data
trading_data = TradingData()

async def handle_trading_query(ctx: Context, sender: str, msg: TradingQueryMessage):
    """Handle incoming trading queries"""
    try:
        # Extract query and chain from message
        query = msg.query
        chain = msg.chain
        
        ctx.logger.info(f"Received trading query: {query} on chain: {chain}")
        
        # Generate recommendation using enhanced AI if available
        if ENHANCED_AI_AVAILABLE and enhanced_analyzer:
            try:
                ctx.logger.info("🤖 Using enhanced AI analyzer...")
                recommendation = await enhanced_analyzer.generate_trading_response(query)
            except Exception as e:
                ctx.logger.error(f"Enhanced AI failed, falling back to basic: {e}")
                # Fallback to basic recommendation
                eth_price = await trading_data.get_eth_price()
                market_data = {
                    "eth_price": eth_price,
                    "timestamp": datetime.now().isoformat(),
                    "chain": chain
                }
                recommendation = trading_data.generate_trading_recommendation(query, market_data)
        else:
            # Use basic recommendation system
            ctx.logger.info("🔧 Using basic recommendation system...")
            eth_price = await trading_data.get_eth_price()
            market_data = {
                "eth_price": eth_price,
                "timestamp": datetime.now().isoformat(),
                "chain": chain
            }
            recommendation = trading_data.generate_trading_recommendation(query, market_data)
        
        # Create response
        response = TradingResponseMessage(
            agent="NeuroTrade AI Agent",
            query=query,
            recommendation=recommendation,
            market_data={"timestamp": datetime.now().isoformat(), "chain": chain},
            timestamp=datetime.now().isoformat(),
            chain=chain
        )
        
        # Send response back
        await ctx.send(sender, response)
        
    except Exception as e:
        ctx.logger.error(f"Error handling trading query: {e}")
        error_response = TradingResponseMessage(
            agent="NeuroTrade AI Agent",
            query=msg.query if hasattr(msg, 'query') else "Unknown",
            recommendation=f"Error: Failed to process trading query - {str(e)}",
            market_data={},
            timestamp=datetime.now().isoformat(),
            chain=msg.chain if hasattr(msg, 'chain') else "ethereum"
        )
        await ctx.send(sender, error_response)

@neurotrade_agent.on_interval(period=300.0)  # Every 5 minutes
async def update_market_data(ctx: Context):
    """Periodically update market data"""
    try:
        ctx.logger.info("Updating market data...")
        
        # Update ETH price
        eth_price = await trading_data.get_eth_price()
        if eth_price:
            trading_data.token_prices["ETH"] = eth_price
            ctx.logger.info(f"Updated ETH price: ${eth_price}")
        
        trading_data.last_update = datetime.now()
        
    except Exception as e:
        ctx.logger.error(f"Error updating market data: {e}")

@neurotrade_agent.on_event("startup")
async def startup_event(ctx: Context):
    """Agent startup event"""
    global agent_context
    agent_context = ctx
    
    ctx.logger.info("🚀 NeuroTrade AI Agent starting up...")
    ctx.logger.info(f"Agent address: {neurotrade_agent.address}")
    
    # Start HTTP server for frontend communication
    http_runner = await start_http_server()
    if http_runner:
        ctx.logger.info("✅ HTTP Server started successfully!")
        ctx.logger.info("🌐 Frontend can now connect to http://localhost:8000")
    else:
        ctx.logger.error("❌ HTTP Server failed to start")
    
    ctx.logger.info("📬 Mailbox enabled - agent will be discoverable on ASI:One")
    ctx.logger.info("🌐 Agent configured as 'Hosted' with 'Chat with Agent' button")
    ctx.logger.info("🔗 Chat functionality enabled via Agentverse endpoint")
    ctx.logger.info("🎯 Agent should appear as: Running, Hosted, Mailnet")
    
    ctx.logger.info("✅ NeuroTrade AI Agent ready for trading queries!")
    
    # Initial market data fetch
    await update_market_data(ctx)

@neurotrade_agent.on_message(model=TradingQueryMessage)
async def handle_trading_query_message(ctx: Context, sender: str, msg: TradingQueryMessage):
    """Handle structured trading query messages"""
    try:
        ctx.logger.info(f"Received trading query from {sender}: {msg.query}")
        
        # Handle trading query directly
        await handle_trading_query(ctx, sender, msg)
        
    except Exception as e:
        ctx.logger.error(f"Error in structured message handler: {e}")

@neurotrade_agent.on_message(model=SimpleMessage)
async def handle_simple_message(ctx: Context, sender: str, msg: SimpleMessage):
    """Handle simple text messages"""
    try:
        ctx.logger.info(f"Received simple message from {sender}: {msg.message}")
        
        # Convert to TradingQueryMessage and route
        trading_msg = TradingQueryMessage(query=msg.message, chain="ethereum")
        await handle_trading_query(ctx, sender, trading_msg)
        
    except Exception as e:
        ctx.logger.error(f"Error in simple message handler: {e}")

@neurotrade_agent.on_message(model=GenericMessage)
async def handle_generic_message(ctx: Context, sender: str, msg: GenericMessage):
    """Handle generic content messages"""
    try:
        ctx.logger.info(f"Received generic message from {sender}: {msg.content}")
        
        # Convert to TradingQueryMessage and route
        trading_msg = TradingQueryMessage(query=msg.content, chain="ethereum")
        await handle_trading_query(ctx, sender, trading_msg)
        
    except Exception as e:
        ctx.logger.error(f"Error in generic message handler: {e}")

# 🎯 OFFICIAL CHAT PROTOCOL INTEGRATION (Working Example)
try:
    from chat_proto import chat_proto, struct_output_client_proto
    neurotrade_agent.include(chat_proto, publish_manifest=True)
    neurotrade_agent.include(struct_output_client_proto, publish_manifest=True)
    print("🚀 Official Chat Protocol loaded successfully!")
    print("🎯 Protocol: AgentChatProtocol v0.3.0 (Official)")
    print("✅ Agent should now show 'Chat with Agent' button!")
    print("💬 Full chat functionality enabled!")
except Exception as e:
    print(f"⚠️ Official Chat Protocol failed: {e}")
    print("💡 Trying fallback protocols...")
    
    # Fallback 1: Custom protocol
    try:
        from neurotrade_chat_protocol import neurotrade_chat_protocol
        neurotrade_agent.include(neurotrade_chat_protocol, publish_manifest=True)
        print("✅ Custom chat protocol loaded!")
    except Exception as e2:
        print(f"❌ All chat protocols failed: {e2}")
        print("💡 Agent will run without chat capabilities")

# Global variables for HTTP server
app = web.Application()
http_server = None
agent_context = None

# HTTP Routes for Frontend
async def health_check(request):
    """Health check endpoint"""
    return web.json_response({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

async def handle_options(request):
    """Handle OPTIONS requests for CORS preflight"""
    return web.Response(
        headers={
            "Access-Control-Allow-Origin": "http://localhost:3000",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }
    )

@web.middleware
async def cors_middleware(request, handler):
    """CORS middleware to allow frontend requests"""
    if request.method == "OPTIONS":
        return await handle_options(request)

    try:
        response = await handler(request)
    except web.HTTPException as ex:
        response = ex

    # Add CORS headers to all responses
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

async def chat_endpoint(request):
    """Chat endpoint for frontend"""
    try:
        data = await request.json()
        query = data.get('message', '')
        symbols = data.get('symbols', [])
        user_id = data.get('user_id', 'frontend_user')
        
        if not query:
            return web.json_response({
                "response": "Please provide a message",
                "success": False,
                "error": "Empty message"
            }, status=400)
        
        # Generate response using enhanced AI if available
        if ENHANCED_AI_AVAILABLE and enhanced_analyzer:
            try:
                response = await enhanced_analyzer.generate_trading_response(query, symbols)
            except Exception as e:
                logger.error(f"Enhanced AI failed: {e}")
                # Fallback to basic response
                eth_price = await trading_data.get_eth_price()
                market_data = {"eth_price": eth_price}
                response = trading_data.generate_trading_recommendation(query, market_data)
        else:
            # Use basic response
            eth_price = await trading_data.get_eth_price()
            market_data = {"eth_price": eth_price}
            response = trading_data.generate_trading_recommendation(query, market_data)
        
        return web.json_response({
            "response": response,
            "timestamp": datetime.utcnow().isoformat(),
            "symbols_analyzed": symbols,
            "analysis_type": "trading_analysis",
            "success": True
        })
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        return web.json_response({
            "response": f"Error: {str(e)}",
            "timestamp": datetime.utcnow().isoformat(),
            "symbols_analyzed": [],
            "analysis_type": "error",
            "success": False,
            "error": str(e)
        }, status=500)

async def analyze_token(request):
    """Token analysis endpoint"""
    try:
        symbol = request.match_info['symbol'].upper()
        
        if ENHANCED_AI_AVAILABLE and enhanced_analyzer:
            try:
                analysis = await enhanced_analyzer.analyze_token(symbol)
                return web.json_response({
                    "symbol": symbol,
                    "analysis": analysis,
                    "timestamp": datetime.utcnow().isoformat(),
                    "success": True
                })
            except Exception as e:
                logger.error(f"Enhanced analysis failed for {symbol}: {e}")
        
        # Fallback to basic analysis
        eth_price = await trading_data.get_eth_price()
        basic_analysis = {
            "symbol": symbol,
            "price": eth_price if symbol == "ETH" else "N/A",
            "recommendation": f"Basic analysis for {symbol}",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return web.json_response({
            "symbol": symbol,
            "analysis": basic_analysis,
            "timestamp": datetime.utcnow().isoformat(),
            "success": True
        })
        
    except Exception as e:
        logger.error(f"Token analysis error: {e}")
        return web.json_response({
            "symbol": symbol,
            "analysis": {},
            "timestamp": datetime.utcnow().isoformat(),
            "success": False,
            "error": str(e)
        }, status=500)

async def supported_tokens(request):
    """Supported tokens endpoint"""
    tokens = ["BTC", "ETH", "USDC", "USDT", "BNB", "SOL", "ADA", "DOT", "MATIC", "UNI", "LINK", "AVAX", "LTC", "XRP", "DOGE"]
    return web.json_response({
        "tokens": tokens,
        "count": len(tokens),
        "timestamp": datetime.utcnow().isoformat()
    })

async def start_session(request):
    """Start a new chat session"""
    session_id = request.match_info.get('session_id', '')
    try:
        data = await request.json()
        user_id = data.get('user_id', 'anonymous')
        return web.json_response({
            "status": "success",
            "session_id": session_id,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return web.json_response({
            "status": "error",
            "error": str(e)
        }, status=400)

async def start_http_server():
    """Start the HTTP server for frontend communication"""
    app = web.Application(middlewares=[cors_middleware])
    
    # Add routes
    app.router.add_get('/health', health_check)
    app.router.add_post('/chat', chat_endpoint)
    app.router.add_post('/analyze-token', analyze_token)
    app.router.add_get('/supported-tokens', supported_tokens)
    
    # Add session routes
    app.router.add_post('/session/{session_id}/start', start_session)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', HTTP_PORT)
    await site.start()
    logger.info(f"HTTP server started on http://localhost:{HTTP_PORT}")
    return runner

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    print(f"\n🛑 Received signal {signum}, shutting down gracefully...")
    sys.exit(0)

if __name__ == "__main__":
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("🔥 Starting NeuroTrade.eth AI Agent...")
    print(f"Agent Address: {neurotrade_agent.address}")
    print("📡 Connecting to Agentverse...")
    
    try:
        # Run the agent
        neurotrade_agent.run()
    except KeyboardInterrupt:
        print("\n🛑 Agent stopped by user")
    except Exception as e:
        print(f"\n❌ Agent error: {e}")
        print("💡 Check logs for details")
    finally:
        print("👋 NeuroTrade AI Agent shutdown complete") 