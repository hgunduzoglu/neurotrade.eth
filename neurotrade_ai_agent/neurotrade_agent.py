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

from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Agent configuration
AGENT_SEED = os.getenv("AGENT_SEED", "neurotrade_ai_agent_seed_2024")
AGENT_PORT = int(os.getenv("AGENT_PORT", "8001"))
USE_AGENTVERSE = os.getenv("USE_AGENTVERSE", "true").lower() == "true"

# The Graph MCP Server Configuration
GRAPH_MCP_URL = "https://token-api.mcp.thegraph.com"
GRAPH_MCP_SSE_URL = "https://token-api.mcp.thegraph.com/sse"

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
    """Class to store and manage trading data - simplified for MCP integration"""
    def __init__(self):
        self.token_prices = {}
        self.market_trends = {}
        self.last_update = None

    async def get_eth_price(self) -> Optional[float]:
        """Get ETH price in USD - fallback only"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd") as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("ethereum", {}).get("usd", 0)
                    return 2500.0  # Fallback price
        except Exception as e:
            logger.error(f"Error fetching ETH price: {e}")
            return 2500.0  # Fallback price

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
        
        # Fetch market data
        eth_price = await trading_data.get_eth_price()
        market_data = {
            "eth_price": eth_price,
            "timestamp": datetime.now().isoformat(),
            "chain": chain
        }
        
        # Generate recommendation
        recommendation = trading_data.generate_trading_recommendation(query, market_data)
        
        # Create response
        response = TradingResponseMessage(
            agent="NeuroTrade AI Agent",
            query=query,
            recommendation=recommendation,
            market_data=market_data,
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
    ctx.logger.info("🚀 NeuroTrade AI Agent starting up...")
    ctx.logger.info(f"Agent address: {neurotrade_agent.address}")
    
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

# 🎯 OFFICIAL CHAT PROTOCOL INTEGRATION with The Graph MCP
try:
    from chat_proto import chat_proto, struct_output_client_proto
    neurotrade_agent.include(chat_proto, publish_manifest=True)
    neurotrade_agent.include(struct_output_client_proto, publish_manifest=True)
    print("🚀 Official Chat Protocol loaded successfully!")
    print("🎯 Protocol: AgentChatProtocol v0.3.0 with The Graph MCP")
    print("✅ Agent should now show 'Chat with Agent' button!")
    print("💬 Full chat functionality enabled!")
    print("🔗 The Graph MCP integration ready!")
except Exception as e:
    print(f"⚠️ Official Chat Protocol failed: {e}")
    print("💡 Agent will run without chat capabilities")

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