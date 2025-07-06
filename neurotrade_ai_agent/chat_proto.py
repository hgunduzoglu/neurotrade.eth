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

# Import the enhanced AI agent
from enhanced_ai_agent import enhanced_analyzer

# AI Agent Address for structured output processing
AI_AGENT_ADDRESS = 'agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y'

if not AI_AGENT_ADDRESS:
    raise ValueError("AI_AGENT_ADDRESS not set")

# Trading Request Model
class TradingRequest(Model):
    query: str
    action_type: str = "general"  # price, buy, sell, swap, analysis, general


# Enhanced trading analysis function
async def get_enhanced_trading_info(query: str) -> str:
    """Get comprehensive trading information using enhanced AI agent"""
    try:
        # Use the enhanced analyzer for sophisticated analysis
        analysis = await enhanced_analyzer.generate_trading_response(query)
        return analysis
    except Exception as e:
        # Fallback to basic error message
        return f"❌ **Error**: Failed to generate enhanced analysis - {str(e)}\n\n" \
               f"💡 **Try asking about**: ETH price, buy/sell signals, or market analysis"

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
        trading_info = await get_enhanced_trading_info(trading_request.query)
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