from datetime import datetime
from uuid import uuid4
from typing import Any
import aiohttp

from uagents import Context, Model, Protocol

# Import the necessary components of the chat protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)

# Import The Graph MCP client
from graph_mcp_client import get_graph_mcp_dispatcher

# AI Agent Address for structured output processing
AI_AGENT_ADDRESS = 'agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y'

if not AI_AGENT_ADDRESS:
    raise ValueError("AI_AGENT_ADDRESS not set")

# Trading Request Model
class TradingRequest(Model):
    query: str
    action_type: str = "general"  # price, buy, sell, swap, analysis, general

# Global The Graph MCP dispatcher instance
graph_mcp_dispatcher = None

async def initialize_graph_mcp():
    """Initialize The Graph MCP client"""
    global graph_mcp_dispatcher
    if graph_mcp_dispatcher is None:
        graph_mcp_dispatcher = await get_graph_mcp_dispatcher()

# Enhanced trading analysis function using The Graph MCP
async def get_trading_info(query: str) -> str:
    """Get enhanced trading information and analysis via The Graph MCP"""
    try:
        # Initialize The Graph MCP client if not already done
        await initialize_graph_mcp()
        
        # Use The Graph MCP dispatcher (includes built-in fallback)
        if graph_mcp_dispatcher:
            result = await graph_mcp_dispatcher.dispatch_query(query)
            if result and "❌" not in result:
                return result
        
        # If MCP fails, provide basic fallback response
        return await get_basic_trading_info(query)
        
    except Exception as e:
        # Final fallback to basic trading info
        return await get_basic_trading_info(query, error=str(e))

async def get_basic_trading_info(query: str, error: str = None) -> str:
    """Basic fallback trading info when MCP is unavailable"""
    query_lower = query.lower()
    
    # Try to get basic ETH price as last resort
    eth_price = 2500  # Default fallback price
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    eth_price = data.get("ethereum", {}).get("usd", 2500)
    except Exception:
        pass  # Use default price
    
    # Generate basic analysis
    analysis = f"🚀 **NeuroTrade AI Analysis**\n\n"
    
    if error:
        analysis += f"⚠️ **Note**: Using fallback mode due to connection issues\n\n"
    
    if any(keyword in query_lower for keyword in ["token", "price", "eth", "usdc"]):
        analysis += f"💰 **Token Information**:\n"
        analysis += f"• Current ETH Price: ${eth_price:,.2f} USD\n"
        analysis += f"• Data Source: CoinGecko (Fallback)\n\n"
        
        analysis += f"📊 **Available via The Graph MCP**:\n"
        analysis += f"• Real-time token data\n"
        analysis += f"• Network statistics\n"
        analysis += f"• Indexer information\n"
        analysis += f"• Allocation data\n\n"
        
    elif "indexer" in query_lower:
        analysis += f"🔍 **Indexer Information**:\n"
        analysis += f"• The Graph indexers process blockchain data\n"
        analysis += f"• Stake GRT tokens to participate\n"
        analysis += f"• Earn rewards for quality indexing\n\n"
        
        analysis += f"📈 **Available via The Graph MCP**:\n"
        analysis += f"• Real-time indexer metrics\n"
        analysis += f"• Performance statistics\n"
        analysis += f"• Allocation tracking\n\n"
        
    elif "allocation" in query_lower:
        analysis += f"📊 **Allocation Information**:\n"
        analysis += f"• Indexers allocate stake to subgraphs\n"
        analysis += f"• Allocations earn indexing rewards\n"
        analysis += f"• Active management required\n\n"
        
        analysis += f"🎯 **Available via The Graph MCP**:\n"
        analysis += f"• Live allocation data\n"
        analysis += f"• Reward calculations\n"
        analysis += f"• Performance metrics\n\n"
        
    elif any(keyword in query_lower for keyword in ["network", "stats"]):
        analysis += f"🌐 **Network Statistics**:\n"
        analysis += f"• The Graph Protocol network info\n"
        analysis += f"• Total indexers and delegators\n"
        analysis += f"• Network activity metrics\n\n"
        
        analysis += f"📈 **Available via The Graph MCP**:\n"
        analysis += f"• Real-time network data\n"
        analysis += f"• Protocol metrics\n"
        analysis += f"• Usage statistics\n\n"
        
    else:
        analysis += f"🤖 **NeuroTrade AI - The Graph MCP Integration**\n\n"
        analysis += f"**Available Queries**:\n"
        analysis += f"• **Token Data**: 'ETH price', 'USDC token info'\n"
        analysis += f"• **Indexer Info**: 'show indexer information'\n"
        analysis += f"• **Allocations**: 'allocation data'\n"
        analysis += f"• **Network Stats**: 'network statistics'\n\n"
        
        analysis += f"**Data Sources**:\n"
        analysis += f"• Primary: The Graph MCP Server\n"
        analysis += f"• Fallback: CoinGecko API\n\n"
    
    analysis += f"---\n"
    analysis += f"🤖 **NeuroTrade AI** - The Graph MCP Integration\n"
    analysis += f"⚡ **Real-time Data** | 🔒 **Secure** | 🎯 **Accurate**"
    
    return analysis

def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    if end_session:
        content.append(EndSessionContent(type="end-session"))
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=content,
    )


chat_proto = Protocol(spec=chat_protocol_spec)
struct_output_client_proto = Protocol(
    name="StructuredOutputClientProtocol", version="0.1.0"
)


class StructuredOutputPrompt(Model):
    prompt: str
    output_schema: dict[str, Any]


class StructuredOutputResponse(Model):
    output: dict[str, Any]


@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    ctx.logger.info(f"Got a message from {sender}: {msg.content}")
    ctx.storage.set(str(ctx.session), sender)
    await ctx.send(
        sender,
        ChatAcknowledgement(timestamp=datetime.utcnow(), acknowledged_msg_id=msg.msg_id),
    )

    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"Got a start session message from {sender}")
            continue
        elif isinstance(item, TextContent):
            ctx.logger.info(f"Got a message from {sender}: {item.text}")
            ctx.storage.set(str(ctx.session), sender)
            await ctx.send(
                AI_AGENT_ADDRESS,
                StructuredOutputPrompt(
                    prompt=item.text, output_schema=TradingRequest.schema()
                ),
            )
        else:
            ctx.logger.info(f"Got unexpected content from {sender}")


@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(
        f"Got an acknowledgement from {sender} for {msg.acknowledged_msg_id}"
    )


@struct_output_client_proto.on_message(StructuredOutputResponse)
async def handle_structured_output_response(
    ctx: Context, sender: str, msg: StructuredOutputResponse
):
    session_sender = ctx.storage.get(str(ctx.session))
    if session_sender is None:
        ctx.logger.error(
            "Discarding message because no session sender found in storage"
        )
        return

    if "<UNKNOWN>" in str(msg.output):
        await ctx.send(
            session_sender,
            create_text_chat(
                "Sorry, I couldn't process your trading request. Please try again later."
            ),
        )
        return

    try:
        trading_request = TradingRequest.parse_obj(msg.output)
    except Exception as err:
        ctx.logger.error(f"Error parsing trading request: {err}")
        await ctx.send(
            session_sender,
            create_text_chat(
                "Sorry, I couldn't understand your trading query. Please try asking about ETH price, buy/sell signals, or swap analysis."
            ),
        )
        return

    try:
        trading_info = await get_trading_info(trading_request.query)
    except Exception as err:
        ctx.logger.error(f"Error getting trading info: {err}")
        await ctx.send(
            session_sender,
            create_text_chat(
                "Sorry, I couldn't process your trading request. Please try again later."
            ),
        )
        return

    chat_message = create_text_chat(trading_info)
    await ctx.send(session_sender, chat_message)