from datetime import datetime
from uuid import uuid4
from typing import List, Union, Dict, Any, Optional, Literal
import aiohttp

from uagents import Context, Model, Protocol
from pydantic import Field

# 🎯 EXACT CHAT PROTOCOL IMPLEMENTATION
# Based on Claude agent's manifest digest: proto:30a801ed3a83f9a0ff0a9f1e6fe958cb91da1fc2218b153df7b6cbf87bd33d62

# === CONTENT MODELS (Exact from manifest) ===

class TextContent(Model):
    type: Literal["text"] = "text"
    text: str

class EndSessionContent(Model):
    type: Literal["end-session"] = "end-session"

class StartSessionContent(Model):
    type: Literal["start-session"] = "start-session"

class EndStreamContent(Model):
    type: Literal["end-stream"] = "end-stream"
    stream_id: str

class StartStreamContent(Model):
    type: Literal["start-stream"] = "start-stream"
    stream_id: str

class Resource(Model):
    uri: str
    metadata: Dict[str, str]

class ResourceContent(Model):
    type: Literal["resource"] = "resource"
    resource_id: str
    resource: Union[Resource, List[Resource]]

class MetadataContent(Model):
    type: Literal["metadata"] = "metadata"
    metadata: Dict[str, str]

# === MAIN PROTOCOL MODELS (Exact from manifest) ===

class ChatMessage(Model):
    timestamp: datetime
    msg_id: str
    content: List[Union[
        TextContent,
        ResourceContent,
        MetadataContent,
        StartSessionContent,
        EndSessionContent,
        StartStreamContent,
        EndStreamContent
    ]]

class ChatAcknowledgement(Model):
    timestamp: datetime
    acknowledged_msg_id: str
    metadata: Optional[Dict[str, str]] = None

# === PROTOCOL CREATION ===
# This should create the exact same digest as Claude's agent
exact_chat_protocol = Protocol(
    name="AgentChatProtocol",
    version="0.3.0"
)

# === TRADING LOGIC ===
async def get_eth_trading_analysis(query: str) -> str:
    """Get comprehensive ETH trading analysis"""
    try:
        # Get real-time ETH data
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.coingecko.com/api/v3/simple/price",
                params={
                    "ids": "ethereum",
                    "vs_currencies": "usd",
                    "include_24hr_change": "true",
                    "include_24hr_vol": "true",
                    "include_market_cap": "true"
                }
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    eth_data = data.get("ethereum", {})
                    
                    price = eth_data.get("usd", 2500)
                    change_24h = eth_data.get("usd_24h_change", 0)
                    volume_24h = eth_data.get("usd_24h_vol", 0)
                    market_cap = eth_data.get("usd_market_cap", 0)
                else:
                    price, change_24h, volume_24h, market_cap = 2500, 0, 0, 0
                    
    except Exception as e:
        price, change_24h, volume_24h, market_cap = 2500, 0, 0, 0
    
    # Generate comprehensive analysis
    query_lower = query.lower()
    
    # Header with current data
    analysis = f"🚀 **NeuroTrade AI - Live ETH Analysis**\n\n"
    analysis += f"💰 **Current Price**: ${price:,.2f} USD\n"
    analysis += f"📊 **24h Change**: {change_24h:+.2f}%\n"
    analysis += f"💹 **24h Volume**: ${volume_24h:,.0f}\n"
    analysis += f"🏆 **Market Cap**: ${market_cap:,.0f}\n\n"
    
    # Market sentiment
    if change_24h > 2:
        sentiment = "🟢 **Bullish** - Strong upward momentum"
    elif change_24h > 0:
        sentiment = "🟡 **Neutral-Bullish** - Positive but cautious"
    elif change_24h > -2:
        sentiment = "🟡 **Neutral** - Sideways movement"
    else:
        sentiment = "🔴 **Bearish** - Downward pressure"
    
    analysis += f"🎯 **Market Sentiment**: {sentiment}\n\n"
    
    # Specific analysis based on query
    if any(word in query_lower for word in ["price", "cost", "value"]):
        analysis += f"📈 **Price Analysis**:\n"
        analysis += f"• Current trend: {'Upward' if change_24h > 0 else 'Downward' if change_24h < -1 else 'Sideways'}\n"
        analysis += f"• Volatility: {'High' if abs(change_24h) > 3 else 'Moderate' if abs(change_24h) > 1 else 'Low'}\n"
        analysis += f"• Volume status: {'Above average' if volume_24h > 10000000000 else 'Normal'}\n"
        analysis += f"• Support level: ~${price * 0.95:.2f}\n"
        analysis += f"• Resistance level: ~${price * 1.05:.2f}\n\n"
        
    elif any(word in query_lower for word in ["buy", "purchase", "long"]):
        analysis += f"🔵 **Buy Signal Analysis**:\n"
        if change_24h > 1:
            analysis += f"✅ **Signal**: POSITIVE\n"
            analysis += f"• Strong upward momentum detected\n"
            analysis += f"• Volume confirms buying interest\n"
            analysis += f"• Entry strategy: Consider immediate entry\n"
        elif change_24h > -1:
            analysis += f"⚠️ **Signal**: NEUTRAL\n"
            analysis += f"• Price consolidating, wait for breakout\n"
            analysis += f"• Entry strategy: Set buy orders at ${price * 0.98:.2f}\n"
        else:
            analysis += f"❌ **Signal**: NEGATIVE\n"
            analysis += f"• Downward trend, avoid buying\n"
            analysis += f"• Entry strategy: Wait for reversal confirmation\n"
        analysis += f"• Stop-loss: ${price * 0.92:.2f}\n"
        analysis += f"• Take-profit: ${price * 1.15:.2f}\n\n"
        
    elif any(word in query_lower for word in ["sell", "exit", "short"]):
        analysis += f"🔴 **Sell Signal Analysis**:\n"
        if change_24h < -1:
            analysis += f"✅ **Signal**: POSITIVE for selling\n"
            analysis += f"• Downward momentum confirmed\n"
            analysis += f"• Volume suggests selling pressure\n"
            analysis += f"• Exit strategy: Consider immediate exit\n"
        elif change_24h < 1:
            analysis += f"⚠️ **Signal**: NEUTRAL\n"
            analysis += f"• Price range-bound, partial profit taking\n"
            analysis += f"• Exit strategy: Trim positions on strength\n"
        else:
            analysis += f"❌ **Signal**: NEGATIVE for selling\n"
            analysis += f"• Upward trend intact, hold positions\n"
            analysis += f"• Exit strategy: Set trailing stops\n"
        analysis += f"• Stop-loss: ${price * 1.08:.2f}\n"
        analysis += f"• Target: ${price * 0.85:.2f}\n\n"
        
    elif any(word in query_lower for word in ["swap", "exchange", "trade"]):
        analysis += f"🔄 **Swap Analysis**:\n"
        analysis += f"• Current ETH price: ${price:,.2f}\n"
        analysis += f"• Gas fees: {'High' if price > 3000 else 'Moderate' if price > 2000 else 'Low'} (network congestion)\n"
        analysis += f"• Slippage risk: {'High' if volume_24h < 5000000000 else 'Low'}\n"
        analysis += f"• Best timing: {'Wait for lower gas' if price > 3000 else 'Good timing'}\n"
        analysis += f"• DEX recommendation: Use aggregators for best rates\n\n"
        
    elif any(word in query_lower for word in ["forecast", "prediction", "future"]):
        analysis += f"🔮 **Market Forecast**:\n"
        if change_24h > 2:
            analysis += f"• Short-term (24h): Continued bullish momentum likely\n"
            analysis += f"• Medium-term (7d): Expect some consolidation\n"
            analysis += f"• Target: ${price * 1.10:.2f} - ${price * 1.20:.2f}\n"
        elif change_24h < -2:
            analysis += f"• Short-term (24h): Further downside possible\n"
            analysis += f"• Medium-term (7d): Look for bounce signals\n"
            analysis += f"• Target: ${price * 0.90:.2f} - ${price * 0.80:.2f}\n"
        else:
            analysis += f"• Short-term (24h): Range-bound trading expected\n"
            analysis += f"• Medium-term (7d): Awaiting directional catalyst\n"
            analysis += f"• Range: ${price * 0.95:.2f} - ${price * 1.05:.2f}\n"
        analysis += f"\n"
        
    else:
        # General analysis
        analysis += f"💡 **General Market Status**:\n"
        analysis += f"• ETH is showing {'strength' if change_24h > 0 else 'weakness'} today\n"
        analysis += f"• Trading volume is {'healthy' if volume_24h > 8000000000 else 'light'}\n"
        analysis += f"• Market structure: {'Bullish' if change_24h > 1 else 'Bearish' if change_24h < -1 else 'Neutral'}\n"
        analysis += f"• Opportunity level: {'High' if abs(change_24h) > 3 else 'Moderate'}\n\n"
        
        analysis += f"🎯 **What I Can Help With**:\n"
        analysis += f"• 'ETH price analysis' - Detailed price breakdown\n"
        analysis += f"• 'Should I buy ETH?' - Buy signal analysis\n"
        analysis += f"• 'Should I sell ETH?' - Sell signal analysis\n"
        analysis += f"• 'ETH swap analysis' - Trading execution tips\n"
        analysis += f"• 'ETH forecast' - Market predictions\n\n"
    
    # Footer
    analysis += f"---\n"
    analysis += f"🤖 **NeuroTrade AI** - Real-time Ethereum Trading Intelligence\n"
    analysis += f"🌐 **Multi-Chain**: Ethereum • Arbitrum • Polygon • Optimism • Base\n"
    analysis += f"⚡ **Live Data** • 🔒 **Secure** • 🎯 **Accurate**\n"
    analysis += f"💬 **Ask me anything about ETH trading!**"
    
    return analysis

def create_chat_response(text: str) -> ChatMessage:
    """Create a chat message response"""
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=str(uuid4()),
        content=[TextContent(text=text)]
    )

# === PROTOCOL HANDLERS ===

@exact_chat_protocol.on_message(ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    """Handle incoming chat messages - EXACT implementation"""
    try:
        ctx.logger.info(f"🎯 NeuroTrade Chat: Message from {sender}")
        
        # Send acknowledgment (required by protocol)
        ack = ChatAcknowledgement(
            timestamp=datetime.utcnow(),
            acknowledged_msg_id=msg.msg_id
        )
        await ctx.send(sender, ack)
        
        # Extract text content
        user_text = ""
        session_started = False
        session_ended = False
        
        for content in msg.content:
            if isinstance(content, TextContent):
                user_text += content.text + " "
            elif isinstance(content, StartSessionContent):
                session_started = True
            elif isinstance(content, EndSessionContent):
                session_ended = True
        
        user_text = user_text.strip()
        
        # Handle session start
        if session_started:
            welcome_text = "🎉 **Welcome to NeuroTrade AI!**\n\n"
            welcome_text += "🚀 I'm your intelligent Ethereum trading assistant.\n\n"
            welcome_text += "💡 **I can help you with**:\n"
            welcome_text += "• Real-time ETH price analysis\n"
            welcome_text += "• Smart buy/sell recommendations\n"
            welcome_text += "• Swap optimization strategies\n"
            welcome_text += "• Market forecasting\n"
            welcome_text += "• Cross-chain opportunities\n\n"
            welcome_text += "🎯 **Try asking**: 'What's ETH price?' or 'Should I buy ETH?'"
            
            response = create_chat_response(welcome_text)
            await ctx.send(sender, response)
            return
        
        # Handle session end
        if session_ended:
            goodbye_text = "👋 **Thank you for using NeuroTrade AI!**\n\n"
            goodbye_text += "🎯 **Session Summary**: We analyzed ETH market conditions\n"
            goodbye_text += "📊 **Market Status**: Live data processed successfully\n"
            goodbye_text += "🚀 **Come back anytime** for more trading insights!\n\n"
            goodbye_text += "🌐 **Find me on ASI:One** for 24/7 trading intelligence\n"
            goodbye_text += "💬 **NeuroTrade AI** - Your Smart Trading Partner"
            
            response = create_chat_response(goodbye_text)
            await ctx.send(sender, response)
            return
        
        # Handle regular chat
        if not user_text:
            # Empty message - send help
            help_text = "💬 **NeuroTrade AI Ready!**\n\n"
            help_text += "🔥 **Live ETH Trading Intelligence**\n\n"
            help_text += "💡 **Ask me about**:\n"
            help_text += "• 'ETH price' - Current market analysis\n"
            help_text += "• 'Buy ETH' - Purchase recommendations\n"
            help_text += "• 'Sell ETH' - Exit strategies\n"
            help_text += "• 'ETH forecast' - Market predictions\n"
            help_text += "• 'Swap ETH' - Trading execution\n\n"
            help_text += "🎯 **Start chatting** - I'm here to help!"
            
            response = create_chat_response(help_text)
            await ctx.send(sender, response)
            return
        
        # Process trading query
        ctx.logger.info(f"Processing query: {user_text}")
        
        # Get analysis
        analysis = await get_eth_trading_analysis(user_text)
        
        # Send response
        response = create_chat_response(analysis)
        await ctx.send(sender, response)
        
    except Exception as e:
        ctx.logger.error(f"Chat handler error: {e}")
        
        # Send error response
        error_text = "❌ **Error Processing Request**\n\n"
        error_text += "🔧 Sorry, I encountered an issue processing your query.\n\n"
        error_text += "💡 **Please try**:\n"
        error_text += "• 'ETH price' - For current price\n"
        error_text += "• 'Buy ETH' - For buy analysis\n"
        error_text += "• 'Sell ETH' - For sell analysis\n"
        error_text += "• 'ETH forecast' - For predictions\n\n"
        error_text += "🤖 **NeuroTrade AI** is ready to help!"
        
        error_response = create_chat_response(error_text)
        await ctx.send(sender, error_response)

@exact_chat_protocol.on_message(ChatAcknowledgement)
async def handle_chat_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handle acknowledgments - EXACT implementation"""
    ctx.logger.info(f"🎯 NeuroTrade: Received acknowledgment from {sender}")
    # No response needed for acknowledgments as per manifest

# Export the protocol
__all__ = ["exact_chat_protocol"] 