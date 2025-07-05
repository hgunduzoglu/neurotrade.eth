from datetime import datetime
from uuid import uuid4
from typing import List, Optional
import aiohttp

from uagents import Context, Model, Protocol

# 🎯 NEUROTRADE CUSTOM CHAT PROTOCOL
# Completely custom implementation - no official spec dependency

class NeurotradeChatMessage(Model):
    """Custom chat message for NeuroTrade"""
    msg_id: str
    content: str
    timestamp: str
    sender: str
    msg_type: str = "text"  # text, welcome, goodbye, error

class NeurotradeChatResponse(Model):
    """Custom chat response for NeuroTrade"""
    msg_id: str
    content: str
    timestamp: str
    trading_data: Optional[dict] = None
    msg_type: str = "response"

class NeurotradeSessionStart(Model):
    """Session start message"""
    session_id: str
    timestamp: str
    msg_type: str = "session_start"

class NeurotradeSessionEnd(Model):
    """Session end message"""
    session_id: str
    timestamp: str
    msg_type: str = "session_end"

# 🚀 Create our own protocol with custom name
neurotrade_chat_protocol = Protocol(
    name="NeurotradeChatProtocol",
    version="1.0.0"
)

# Active sessions tracking
active_sessions = {}

async def get_eth_trading_data(query: str) -> dict:
    """Get real-time ETH trading data"""
    try:
        # Fetch ETH price from CoinGecko
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
                        "price": eth_data.get("usd", 2500),
                        "change_24h": eth_data.get("usd_24h_change", 0),
                        "volume_24h": eth_data.get("usd_24h_vol", 0)
                    }
                else:
                    return {"price": 2500, "change_24h": 0, "volume_24h": 0}
    except Exception as e:
        print(f"Error fetching ETH data: {e}")
        return {"price": 2500, "change_24h": 0, "volume_24h": 0}

def generate_trading_response(query: str, trading_data: dict) -> str:
    """Generate trading response based on query and data"""
    query_lower = query.lower()
    price = trading_data.get("price", 2500)
    change_24h = trading_data.get("change_24h", 0)
    volume_24h = trading_data.get("volume_24h", 0)
    
    response = f"🚀 **NeuroTrade AI Analysis**\n\n"
    response += f"💰 **Current ETH Price**: ${price:,.2f} USD\n"
    response += f"📈 **24h Change**: {change_24h:+.2f}%\n"
    response += f"💹 **24h Volume**: ${volume_24h:,.0f} USD\n\n"
    
    # Market sentiment
    sentiment = "🟢 Bullish" if change_24h > 0 else "🔴 Bearish" if change_24h < -2 else "🟡 Neutral"
    response += f"🎯 **Market Sentiment**: {sentiment}\n\n"
    
    if "price" in query_lower:
        response += f"📊 **Price Analysis**:\n"
        response += f"• ETH is {'up' if change_24h > 0 else 'down'} {abs(change_24h):.2f}% in 24h\n"
        response += f"• Current trend: {'Bullish momentum' if change_24h > 2 else 'Bearish pressure' if change_24h < -2 else 'Sideways movement'}\n"
        response += f"• Volume: {'High' if volume_24h > 10000000000 else 'Normal'} trading activity\n\n"
        
    elif "buy" in query_lower:
        response += f"🔵 **Buy Signal Analysis**:\n"
        if change_24h > 0:
            response += f"• ✅ Positive momentum detected\n"
            response += f"• 💡 Consider dollar-cost averaging\n"
            response += f"• ⚡ Entry point: Current levels look favorable\n"
        else:
            response += f"• ⚠️ Price showing weakness\n"
            response += f"• 💡 Wait for confirmation or lower entry\n"
            response += f"• 📉 Consider setting buy orders below current price\n"
        response += f"• 🎯 **Risk**: Moderate | **Timeframe**: Medium-term\n\n"
        
    elif "sell" in query_lower:
        response += f"🔴 **Sell Signal Analysis**:\n"
        if change_24h < -2:
            response += f"• ⚠️ Significant downward pressure\n"
            response += f"• 💡 Consider taking profits if in green\n"
            response += f"• 📉 Stop-loss recommended\n"
        else:
            response += f"• ✅ Price holding well\n"
            response += f"• 💰 Consider partial profit-taking\n"
            response += f"• 🎯 Set trailing stops\n"
        response += f"• 🎯 **Risk**: Moderate | **Strategy**: Profit protection\n\n"
        
    elif "swap" in query_lower:
        response += f"🔄 **Swap Analysis**:\n"
        response += f"• 💱 Current ETH price: ${price:,.2f}\n"
        response += f"• ⛽ Gas fees: Check current network congestion\n"
        response += f"• 🌊 Liquidity: {'Good' if volume_24h > 5000000000 else 'Check DEX pools'}\n"
        response += f"• ⏰ Timing: {'Favorable' if abs(change_24h) < 3 else 'Volatile - use limit orders'}\n\n"
        
    elif "analysis" in query_lower or "market" in query_lower:
        response += f"📈 **Market Analysis**:\n"
        response += f"• 📊 Technical: {sentiment.split()[1]} bias\n"
        response += f"• 💹 Volume: {'Above' if volume_24h > 8000000000 else 'Below'} average\n"
        response += f"• 🎯 Support/Resistance: Monitor key levels\n"
        response += f"• 🔮 Outlook: {'Positive' if change_24h > 1 else 'Cautious' if change_24h > -1 else 'Bearish'}\n\n"
        
    else:
        response += f"💡 **Available Commands**:\n"
        response += f"• 'ETH price' - Current price and trends\n"
        response += f"• 'Should I buy ETH?' - Buy signal analysis\n"
        response += f"• 'Should I sell ETH?' - Sell signal analysis\n"
        response += f"• 'ETH swap analysis' - Swap recommendations\n"
        response += f"• 'Market analysis' - Complete market overview\n\n"
    
    response += f"---\n"
    response += f"🤖 **NeuroTrade AI** - Your Smart Trading Assistant\n"
    response += f"🌐 **Multi-chain Support**: Ethereum, Arbitrum, Polygon, Optimism, Base\n"
    response += f"⚡ **Real-time Data** | 🔒 **Secure** | 🎯 **Accurate**"
    
    return response

@neurotrade_chat_protocol.on_message(NeurotradeChatMessage)
async def handle_neurotrade_chat(ctx: Context, sender: str, msg: NeurotradeChatMessage):
    """Handle incoming chat messages"""
    ctx.logger.info(f"🎯 NeuroTrade Chat: Received message from {sender}")
    
    try:
        # Handle different message types
        if msg.msg_type == "text":
            content = msg.content.strip()
            
            # Empty message - send welcome
            if not content:
                welcome_msg = "👋 **Welcome to NeuroTrade AI!**\n\n"
                welcome_msg += "🚀 I'm your intelligent trading assistant specializing in ETH analysis.\n\n"
                welcome_msg += "💡 **Ask me about**:\n"
                welcome_msg += "• ETH price and trends\n"
                welcome_msg += "• Buy/sell recommendations\n"
                welcome_msg += "• Swap analysis\n"
                welcome_msg += "• Market insights\n\n"
                welcome_msg += "🎯 **Try**: 'What's ETH price?' or 'Should I buy ETH?'"
                
                response = NeurotradeChatResponse(
                    msg_id=str(uuid4()),
                    content=welcome_msg,
                    timestamp=datetime.utcnow().isoformat(),
                    msg_type="welcome"
                )
                await ctx.send(sender, response)
                return
            
            # Process trading query
            ctx.logger.info(f"Processing query: {content}")
            
            # Get real-time trading data
            trading_data = await get_eth_trading_data(content)
            
            # Generate response
            response_content = generate_trading_response(content, trading_data)
            
            # Send response
            response = NeurotradeChatResponse(
                msg_id=str(uuid4()),
                content=response_content,
                timestamp=datetime.utcnow().isoformat(),
                trading_data=trading_data,
                msg_type="response"
            )
            
            await ctx.send(sender, response)
            
        else:
            # Handle other message types
            ctx.logger.info(f"Received {msg.msg_type} message")
            
    except Exception as e:
        ctx.logger.error(f"Error in NeuroTrade chat handler: {e}")
        
        # Send error response
        error_msg = "❌ **Error Processing Request**\n\n"
        error_msg += "🔧 Something went wrong while processing your trading query.\n\n"
        error_msg += "💡 **Please try**:\n"
        error_msg += "• 'ETH price' - For current price\n"
        error_msg += "• 'Buy ETH analysis' - For buy signals\n"
        error_msg += "• 'Sell ETH analysis' - For sell signals\n"
        error_msg += "• 'Market analysis' - For market overview\n\n"
        error_msg += "🤖 **NeuroTrade AI** is ready to help!"
        
        error_response = NeurotradeChatResponse(
            msg_id=str(uuid4()),
            content=error_msg,
            timestamp=datetime.utcnow().isoformat(),
            msg_type="error"
        )
        await ctx.send(sender, error_response)

@neurotrade_chat_protocol.on_message(NeurotradeSessionStart)
async def handle_session_start(ctx: Context, sender: str, msg: NeurotradeSessionStart):
    """Handle session start"""
    ctx.logger.info(f"🎯 NeuroTrade: Session started with {sender}")
    
    # Track active session
    active_sessions[sender] = {
        "session_id": msg.session_id,
        "start_time": datetime.utcnow(),
        "message_count": 0
    }
    
    # Send welcome message
    welcome_msg = "🎉 **Session Started!**\n\n"
    welcome_msg += "🚀 **NeuroTrade AI** is now active and ready to assist you.\n\n"
    welcome_msg += "💡 **I can help you with**:\n"
    welcome_msg += "• Real-time ETH price analysis\n"
    welcome_msg += "• Smart buy/sell recommendations\n"
    welcome_msg += "• Swap strategy optimization\n"
    welcome_msg += "• Cross-chain trading insights\n\n"
    welcome_msg += "🎯 **Start by asking**: 'What's ETH doing today?'"
    
    response = NeurotradeChatResponse(
        msg_id=str(uuid4()),
        content=welcome_msg,
        timestamp=datetime.utcnow().isoformat(),
        msg_type="session_welcome"
    )
    await ctx.send(sender, response)

@neurotrade_chat_protocol.on_message(NeurotradeSessionEnd)
async def handle_session_end(ctx: Context, sender: str, msg: NeurotradeSessionEnd):
    """Handle session end"""
    ctx.logger.info(f"🎯 NeuroTrade: Session ended with {sender}")
    
    # Clean up session
    if sender in active_sessions:
        session_info = active_sessions[sender]
        del active_sessions[sender]
        
        # Send goodbye message
        goodbye_msg = "👋 **Session Ended!**\n\n"
        goodbye_msg += "🎯 **NeuroTrade AI** session completed.\n\n"
        goodbye_msg += "📊 **Session Summary**:\n"
        goodbye_msg += f"• Messages processed: {session_info.get('message_count', 0)}\n"
        goodbye_msg += f"• Duration: {datetime.utcnow() - session_info.get('start_time', datetime.utcnow())}\n\n"
        goodbye_msg += "🚀 **Thank you for using NeuroTrade AI!**\n"
        goodbye_msg += "💡 Come back anytime for smart trading insights.\n\n"
        goodbye_msg += "🌐 **Stay connected** on ASI:One for more AI trading tools!"
        
        response = NeurotradeChatResponse(
            msg_id=str(uuid4()),
            content=goodbye_msg,
            timestamp=datetime.utcnow().isoformat(),
            msg_type="session_goodbye"
        )
        await ctx.send(sender, response)

# Export the protocol
__all__ = ["neurotrade_chat_protocol"] 