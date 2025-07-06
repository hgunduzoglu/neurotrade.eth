from datetime import datetime
from uuid import uuid4
from typing import List, Union, Dict, Any, Optional, Literal
import aiohttp

from uagents import Context, Model, Protocol
from pydantic import Field

# Import the enhanced AI agent
from enhanced_ai_agent import enhanced_analyzer

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
async def get_enhanced_trading_analysis(query: str) -> str:
    """Get comprehensive trading analysis using enhanced AI agent"""
    try:
        # Use the enhanced analyzer for sophisticated analysis
        analysis = await enhanced_analyzer.generate_trading_response(query)
        return analysis
    except Exception as e:
        # Fallback to basic analysis if enhanced fails
        return f"❌ **Error**: Failed to generate enhanced analysis - {str(e)}\n\n" \
               f"💡 **Try asking about**: ETH price, buy/sell signals, or market analysis"

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
        analysis = await get_enhanced_trading_analysis(user_text)
        
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