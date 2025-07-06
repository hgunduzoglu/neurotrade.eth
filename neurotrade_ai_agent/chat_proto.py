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

# AI Agent Address for structured output processing
AI_AGENT_ADDRESS = 'agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y'

if not AI_AGENT_ADDRESS:
    raise ValueError("AI_AGENT_ADDRESS not set")

# Trading Request Model
class TradingRequest(Model):
    query: str
    action_type: str = "general"  # price, buy, sell, swap, analysis, general


# Trading analysis function
async def get_trading_info(query: str) -> str:
    """Get ETH trading information and analysis"""
    try:
        # Get real-time ETH price from CoinGecko
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
                    price = eth_data.get("usd", 2500)
                    change_24h = eth_data.get("usd_24h_change", 0)
                    volume_24h = eth_data.get("usd_24h_vol", 0)
                else:
                    price, change_24h, volume_24h = 2500, 0, 0
    except Exception as e:
        price, change_24h, volume_24h = 2500, 0, 0
    
    # Generate trading analysis
    query_lower = query.lower()
    
    analysis = f"🚀 **NeuroTrade AI Analysis**\n\n"
    analysis += f"💰 **Current ETH Price**: ${price:,.2f} USD\n"
    analysis += f"📈 **24h Change**: {change_24h:+.2f}%\n"
    analysis += f"💹 **24h Volume**: ${volume_24h:,.0f} USD\n\n"
    
    # Market sentiment
    sentiment = "🟢 Bullish" if change_24h > 0 else "🔴 Bearish" if change_24h < -2 else "🟡 Neutral"
    analysis += f"🎯 **Market Sentiment**: {sentiment}\n\n"
    
    if "price" in query_lower:
        analysis += f"📊 **Price Analysis**:\n"
        analysis += f"• ETH is {'up' if change_24h > 0 else 'down'} {abs(change_24h):.2f}% today\n"
        analysis += f"• Trading volume is {'high' if volume_24h > 10000000000 else 'normal'}\n"
        analysis += f"• Price momentum: {'Bullish' if change_24h > 1 else 'Bearish' if change_24h < -1 else 'Neutral'}\n\n"
    elif "buy" in query_lower:
        analysis += f"🔵 **Buy Signal Analysis**:\n"
        if change_24h > 0:
            analysis += f"✅ **Positive momentum** - Consider buying\n"
            analysis += f"• Entry point: Current levels look favorable\n"
            analysis += f"• Strategy: Dollar-cost averaging recommended\n"
        else:
            analysis += f"⚠️ **Negative momentum** - Wait for confirmation\n"
            analysis += f"• Entry point: Consider lower levels\n"
            analysis += f"• Strategy: Set buy orders below current price\n"
        analysis += f"• Risk Level: Moderate\n\n"
    elif "sell" in query_lower:
        analysis += f"🔴 **Sell Signal Analysis**:\n"
        if change_24h < -2:
            analysis += f"⚠️ **Strong downward pressure** - Consider selling\n"
            analysis += f"• Exit strategy: Take profits if in green\n"
            analysis += f"• Risk management: Set stop-losses\n"
        else:
            analysis += f"✅ **Price holding well** - Partial profit taking\n"
            analysis += f"• Exit strategy: Trailing stops recommended\n"
        analysis += f"• Risk Level: Moderate\n\n"
    elif "swap" in query_lower:
        analysis += f"🔄 **Swap Analysis**:\n"
        analysis += f"• Current ETH price: ${price:,.2f}\n"
        analysis += f"• Gas fees: Check current network congestion\n"
        analysis += f"• Liquidity: {'Good' if volume_24h > 5000000000 else 'Check DEX pools'}\n"
        analysis += f"• Timing: {'Favorable' if abs(change_24h) < 3 else 'Volatile - use limit orders'}\n\n"
    else:
        analysis += f"💡 **General Trading Info**:\n"
        analysis += f"• Ask me about 'ETH price', 'buy ETH', 'sell ETH', or 'swap ETH'\n"
        analysis += f"• I provide real-time analysis and recommendations\n"
        analysis += f"• Multi-chain support: Ethereum, Arbitrum, Polygon, Optimism, Base\n\n"
    
    analysis += f"---\n"
    analysis += f"🤖 **NeuroTrade AI** - Your Smart Trading Assistant\n"
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