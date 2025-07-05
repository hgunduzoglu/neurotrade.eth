import asyncio
import aiohttp
import json
import os
import logging
import signal
import sys
from typing import Dict, List, Optional, Any
from datetime import datetime
from dotenv import load_dotenv

from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

# Import The Graph MCP client instead of generic one
from graph_mcp_client import GraphMCPClient, GraphMCPQueryDispatcher

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Agent configuration
AGENT_SEED = os.getenv("AGENT_SEED", "neurotrade_thegraph_agent_seed_2024")
AGENT_PORT = int(os.getenv("AGENT_PORT", "8001"))
THEGRAPH_MCP_URL = os.getenv("THEGRAPH_MCP_URL", "https://token-api.mcp.thegraph.com")
USE_AGENTVERSE = os.getenv("USE_AGENTVERSE", "true").lower() == "true"

# Create the NeuroTrade AI Agent with The Graph MCP capabilities
neurotrade_agent = Agent(
    name="NeuroTrade-TheGraph",
    seed=AGENT_SEED,
    mailbox=True,
    port=AGENT_PORT,
    endpoint="https://agentverse.ai/v1/submit" if USE_AGENTVERSE else f"http://localhost:{AGENT_PORT}/submit"
)

# Initialize The Graph MCP client and dispatcher
thegraph_client = GraphMCPClient()
graph_dispatcher = GraphMCPQueryDispatcher(thegraph_client)

print(f"🚀 NeuroTrade The Graph Agent initialized")
print(f"🌐 The Graph MCP URL: {THEGRAPH_MCP_URL}")
print(f"🤖 Agent Address: {neurotrade_agent.address}")

# Fund the agent if needed
try:
    fund_agent_if_low(neurotrade_agent.wallet.address())
except Exception as e:
    print(f"⚠️ Warning: Could not fund agent: {e}")

# Enhanced Message Models with The Graph MCP support
class TheGraphTradingQuery(Model):
    query: str
    chain: str = "ethereum"
    use_thegraph: bool = True
    requested_tools: List[str] = []

class TheGraphTradingResponse(Model):
    agent: str
    query: str
    response: str
    tools_used: List[str]
    tool_results: Dict[str, Any]
    data_source: str  # "thegraph_mcp", "maple_nodes", or "coingecko_fallback"
    timestamp: str
    chain: str
    success: bool

class GraphToolRequest(Model):
    tool_name: str
    parameters: Dict[str, Any]

class GraphToolResponse(Model):
    tool_name: str
    result: Dict[str, Any]
    data_source: str
    success: bool
    error: Optional[str] = None

# Enhanced Trading Data with The Graph integration
class TheGraphTradingData:
    """Enhanced trading data class with The Graph MCP integration"""
    
    def __init__(self, thegraph_client: GraphMCPClient):
        self.thegraph_client = thegraph_client
        self.cache = {}
        self.last_update = None
    
    async def get_enhanced_market_data(self, symbol: str, chain: str = "ethereum") -> Dict:
        """Get enhanced market data using The Graph MCP"""
        if not self.thegraph_client.connected:
            return await self._fallback_market_data(symbol)
        
        try:
            # Call The Graph MCP for token data
            token_data = await self.thegraph_client.get_token_data(symbol, chain)
            
            if "error" not in token_data:
                return token_data
            else:
                logger.warning(f"The Graph MCP failed, using fallback: {token_data['error']}")
                return await self._fallback_market_data(symbol)
                
        except Exception as e:
            logger.error(f"The Graph market data error: {e}")
            return await self._fallback_market_data(symbol)
    
    async def _fallback_market_data(self, symbol: str) -> Dict:
        """Fallback market data using direct API"""
        try:
            if symbol.upper() == "ETH":
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        "https://api.coingecko.com/api/v3/simple/price",
                        params={
                            "ids": "ethereum",
                            "vs_currencies": "usd",
                            "include_24hr_change": "true",
                            "include_24hr_vol": "true"
                        }
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            eth_data = data.get("ethereum", {})
                            return {
                                "symbol": "ETH",
                                "price_usd": eth_data.get("usd", 0),
                                "change_24h": eth_data.get("usd_24h_change", 0),
                                "volume_24h": eth_data.get("usd_24h_vol", 0),
                                "source": "coingecko_fallback"
                            }
            
            return {"error": "Fallback data not available"}
            
        except Exception as e:
            return {"error": f"Fallback failed: {str(e)}"}
    
    async def generate_thegraph_trading_analysis(self, query: str, chain: str = "ethereum") -> str:
        """Generate trading analysis using The Graph MCP tools"""
        try:
            # Use The Graph tool dispatcher for comprehensive analysis
            analysis_result = await graph_dispatcher.dispatch_query(query)
            
            if analysis_result.get("formatted_response"):
                return analysis_result["formatted_response"]
            else:
                return "❌ The Graph araçları ile analiz oluşturulamadı"
                
        except Exception as e:
            logger.error(f"The Graph analysis error: {e}")
            return f"❌ Analiz hatası: {str(e)}"

# Global The Graph trading data instance
thegraph_trading_data = TheGraphTradingData(thegraph_client)

# Enhanced message handlers with The Graph MCP integration
async def handle_thegraph_trading_query(ctx: Context, sender: str, msg: TheGraphTradingQuery):
    """Handle trading queries with The Graph MCP"""
    try:
        ctx.logger.info(f"🌐 The Graph Trading Query: {msg.query} (Chain: {msg.chain})")
        
        # Check if specific tools are requested
        if msg.requested_tools:
            ctx.logger.info(f"📋 Requested tools: {msg.requested_tools}")
            
            # Execute specific tools
            tool_results = {}
            data_sources = []
            
            for tool_name in msg.requested_tools:
                available_tools = await thegraph_client.list_tools()
                tool_names = [tool.get("name", "Unknown") for tool in available_tools] if available_tools else []
                
                if tool_name in tool_names:
                    result = await thegraph_client.call_tool(tool_name, {"query": msg.query})
                    tool_results[tool_name] = result
                    data_sources.append(result.get("source", "thegraph_mcp"))
                    ctx.logger.info(f"✅ The Graph tool '{tool_name}' executed")
                else:
                    tool_results[tool_name] = {"error": f"Tool '{tool_name}' not available"}
                    ctx.logger.warning(f"❌ Tool '{tool_name}' not found")
            
            # Generate response from tool results
            response_text = format_thegraph_tool_results(tool_results, msg.query)
            tools_used = msg.requested_tools
            primary_source = data_sources[0] if data_sources else "unknown"
            
        else:
            # Use intelligent The Graph tool dispatcher
            ctx.logger.info("🌐 Using The Graph intelligent tool dispatcher")
            
            # Generate analysis using The Graph MCP
            response_text = await thegraph_trading_data.generate_thegraph_trading_analysis(msg.query, msg.chain)
            
            # Get tools that were used (from dispatcher)
            analysis_result = await graph_dispatcher.dispatch_query(msg.query)
            tools_used = ["analysis"]
            tool_results = {"analysis": analysis_result}
            primary_source = "thegraph_mcp"
        
        # Create response
        response = TheGraphTradingResponse(
            agent="NeuroTrade The Graph AI",
            query=msg.query,
            response=response_text,
            tools_used=tools_used,
            tool_results=tool_results,
            data_source=primary_source,
            timestamp=datetime.now().isoformat(),
            chain=msg.chain,
            success=True
        )
        
        await ctx.send(sender, response)
        
    except Exception as e:
        ctx.logger.error(f"❌ The Graph trading query error: {e}")
        
        # Send error response
        error_response = TheGraphTradingResponse(
            agent="NeuroTrade The Graph AI",
            query=msg.query,
            response=f"❌ **Hata**: {str(e)}",
            tools_used=[],
            tool_results={"error": str(e)},
            data_source="error",
            timestamp=datetime.now().isoformat(),
            chain=msg.chain,
            success=False
        )
        
        await ctx.send(sender, error_response)

def format_thegraph_tool_results(tool_results: Dict[str, Any], query: str) -> str:
    """Format The Graph tool results into readable response"""
    if not tool_results:
        return "❌ The Graph araç sonucu yok"
    
    response = f"🌐 **The Graph Araç Sonuçları**: {query}\n\n"
    
    for tool_name, result in tool_results.items():
        response += f"**{tool_name.upper()}**:\n"
        
        if "error" in result:
            response += f"❌ {result['error']}\n\n"
        else:
            source = result.get("source", "thegraph_mcp")
            response += f"📊 Kaynak: {source}\n"
            
            if isinstance(result, dict):
                for key, value in result.items():
                    if key != "source":
                        response += f"• {key}: {value}\n"
            else:
                response += f"• {result}\n"
            response += "\n"
    
    response += "---\n🌐 **NeuroTrade The Graph AI** - Blockchain Verilerinde Uzman"
    return response

# Direct The Graph tool calling handler
@neurotrade_agent.on_message(model=GraphToolRequest)
async def handle_graph_tool_call(ctx: Context, sender: str, msg: GraphToolRequest):
    """Handle direct The Graph tool calls"""
    try:
        ctx.logger.info(f"🌐 Direct The Graph tool call: {msg.tool_name}")
        
        # Call the tool via The Graph MCP
        result = await thegraph_client.call_tool(msg.tool_name, msg.parameters)
        
        # Create response
        response = GraphToolResponse(
            tool_name=msg.tool_name,
            result=result,
            data_source=result.get("source", "thegraph_mcp"),
            success="error" not in result,
            error=result.get("error") if "error" in result else None
        )
        
        await ctx.send(sender, response)
        
    except Exception as e:
        ctx.logger.error(f"❌ The Graph tool call error: {e}")
        
        error_response = GraphToolResponse(
            tool_name=msg.tool_name,
            result={},
            data_source="error",
            success=False,
            error=str(e)
        )
        
        await ctx.send(sender, error_response)

# Enhanced message handlers for backward compatibility
@neurotrade_agent.on_message(model=TheGraphTradingQuery)
async def handle_thegraph_query_message(ctx: Context, sender: str, msg: TheGraphTradingQuery):
    """Handle The Graph trading query messages"""
    await handle_thegraph_trading_query(ctx, sender, msg)

# Startup and periodic tasks
@neurotrade_agent.on_event("startup")
async def startup_event(ctx: Context):
    """Enhanced startup with The Graph MCP connection"""
    ctx.logger.info("🚀 NeuroTrade The Graph Agent starting up...")
    ctx.logger.info(f"🤖 Agent address: {neurotrade_agent.address}")
    ctx.logger.info(f"🌐 The Graph MCP Server: {THEGRAPH_MCP_URL}")
    
    # Connect to The Graph MCP server
    ctx.logger.info("🔌 Connecting to The Graph MCP server...")
    connected = await thegraph_client.initialize_session()
    
    if connected:
        ctx.logger.info("✅ The Graph MCP connection established")
        tools = await thegraph_client.list_tools()
        
        if tools:
            tool_names = [tool.get("name", "Unknown") for tool in tools]
            ctx.logger.info(f"📦 Available The Graph tools: {', '.join(tool_names)}")
            ctx.logger.info("🌐 Using real The Graph data via official MCP server")
        else:
            ctx.logger.info("📦 Available The Graph tools: None detected")
            ctx.logger.info("🔄 Using Maple Nodes API and fallback systems")
    else:
        ctx.logger.warning("⚠️ The Graph MCP connection failed - using fallback mode")
    
    ctx.logger.info("🎯 NeuroTrade The Graph Agent ready for enhanced blockchain queries!")

@neurotrade_agent.on_interval(period=300.0)  # Every 5 minutes
async def update_thegraph_data(ctx: Context):
    """Update data using available The Graph tools"""
    try:
        if thegraph_client.connected:
            ctx.logger.info("📊 Updating market data via The Graph MCP...")
            
            # Get available tools
            available_tools = await thegraph_client.list_tools()
            
            if available_tools:
                tool_names = [tool.get("name", "Unknown") for tool in available_tools]
                ctx.logger.info(f"🔧 Available tools: {', '.join(tool_names)}")
                
                # Try to get basic market data using fallback
                market_data = await thegraph_trading_data._fallback_market_data("ETH")
                
                if "error" not in market_data:
                    price = market_data.get("price_usd", "N/A")
                    source = market_data.get("source", "fallback")
                    ctx.logger.info(f"✅ ETH data updated: ${price} (Source: {source})")
                else:
                    ctx.logger.warning(f"⚠️ Market data update failed: {market_data['error']}")
            else:
                ctx.logger.warning("⚠️ No The Graph tools available")
                
        else:
            ctx.logger.info("🔄 Attempting to reconnect to The Graph MCP server...")
            await thegraph_client.initialize_session()
            
    except Exception as e:
        ctx.logger.error(f"❌ The Graph update error: {e}")

# Include chat protocols for UI integration
try:
    from chat_proto import chat_proto, struct_output_client_proto
    neurotrade_agent.include(chat_proto, publish_manifest=True)
    neurotrade_agent.include(struct_output_client_proto, publish_manifest=True)
    print("✅ Chat protocols loaded - 'Chat with Agent' enabled!")
except Exception as e:
    print(f"⚠️ Chat protocol loading failed: {e}")

# Graceful shutdown
async def shutdown_handler():
    """Gracefully shutdown The Graph MCP connections"""
    print("🔌 Shutting down The Graph MCP connections...")
    await thegraph_client.disconnect()
    print("✅ The Graph MCP shutdown complete")

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    print(f"\n🛑 Received signal {signum}, shutting down...")
    
    # Run shutdown in event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(shutdown_handler())
    
    sys.exit(0)

if __name__ == "__main__":
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("🔥 Starting NeuroTrade The Graph-Enhanced AI Agent...")
    print(f"🤖 Agent Address: {neurotrade_agent.address}")
    print(f"🌐 The Graph MCP Server: {THEGRAPH_MCP_URL}")
    print("🔧 Real The Graph data access enabled")
    print("📊 Maple Nodes API fallback configured")
    
    try:
        neurotrade_agent.run()
    except KeyboardInterrupt:
        print("\n🛑 Agent stopped by user")
    except Exception as e:
        print(f"\n❌ Agent error: {e}")
    finally:
        # Cleanup
        loop = asyncio.get_event_loop()
        loop.run_until_complete(shutdown_handler())
        print("👋 NeuroTrade The Graph Agent shutdown complete") 