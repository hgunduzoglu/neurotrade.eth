from datetime import datetime
from uuid import uuid4
from typing import List, Optional
import aiohttp

from uagents import Context, Model, Protocol

# Import the enhanced AI agent
from enhanced_ai_agent import enhanced_analyzer

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

async def get_enhanced_neurotrade_analysis(query: str) -> str:
    """Generate enhanced trading analysis using the AI agent"""
    try:
        # Use the enhanced analyzer for sophisticated analysis
        analysis = await enhanced_analyzer.generate_trading_response(query)
        return analysis
    except Exception as e:
        # Fallback to basic error message
        return f"❌ **Error**: Failed to generate enhanced analysis - {str(e)}\n\n" \
               f"💡 **Try asking about**: ETH price, buy/sell signals, or market analysis"

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
            
            # Get enhanced trading analysis
            response_content = await get_enhanced_neurotrade_analysis(content)
            
            # Send response
            response = NeurotradeChatResponse(
                msg_id=str(uuid4()),
                content=response_content,
                timestamp=datetime.utcnow().isoformat(),
                trading_data=None,  # Enhanced analysis includes all data internally
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