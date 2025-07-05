#!/usr/bin/env python3
"""
Demo script showing how to interact with the NeuroTrade AI Agent
This script demonstrates programmatic interaction with the agent
"""

import asyncio
import json
from datetime import datetime
try:
    from neurotrade_agent import TradingData
except ImportError as e:
    print(f"❌ Failed to import TradingData: {e}")
    print("💡 Make sure uagents is properly installed")
    exit(1)

async def demo_ai_capabilities():
    """Demonstrate the AI capabilities of the NeuroTrade agent"""
    print("🤖 NeuroTrade AI Agent Demo")
    print("="*60)
    
    # Initialize the trading data component
    trading_data = TradingData()
    
    # Demo queries that users might ask
    demo_queries = [
        {
            "query": "What's the current ETH price?",
            "description": "Price inquiry"
        },
        {
            "query": "Should I buy ETH now?",
            "description": "Buy recommendation"
        },
        {
            "query": "Should I swap USDC to ETH?",
            "description": "Swap analysis"
        },
        {
            "query": "Is it a good time to sell my tokens?",
            "description": "Sell signal"
        },
        {
            "query": "Tell me about cross-chain trading opportunities",
            "description": "Cross-chain analysis"
        },
        {
            "query": "What are the current market conditions?",
            "description": "Market analysis"
        }
    ]
    
    print("🚀 Fetching real-time market data...")
    
    # Get current market data
    try:
        eth_price = await trading_data.get_eth_price()
        market_data = {
            "eth_price": eth_price,
            "timestamp": datetime.now().isoformat(),
            "chain": "ethereum"
        }
        print(f"✅ Current ETH Price: ${eth_price:.2f}")
    except Exception as e:
        print(f"⚠️  Using fallback data due to: {e}")
        market_data = {
            "eth_price": 2456.78,
            "timestamp": datetime.now().isoformat(),
            "chain": "ethereum"
        }
    
    print("\n🎯 Testing AI Recommendations...")
    print("="*60)
    
    # Test each query
    for i, demo in enumerate(demo_queries, 1):
        print(f"\n{i}. {demo['description'].upper()}")
        print(f"   Query: '{demo['query']}'")
        
        # Generate recommendation
        recommendation = trading_data.generate_trading_recommendation(
            demo['query'], 
            market_data
        )
        
        print(f"   AI Response: {recommendation}")
        
        # Simulate agent response format
        response = {
            "agent": "NeuroTrade AI Agent",
            "query": demo['query'],
            "recommendation": recommendation,
            "market_data": market_data,
            "timestamp": datetime.now().isoformat(),
            "chain": "ethereum"
        }
        
        print(f"   Response Format: {json.dumps(response, indent=2)[:100]}...")
        await asyncio.sleep(0.5)  # Small delay for demo purposes
    
    print("\n🔍 Testing Market Analysis...")
    print("="*40)
    
    # Test market analysis with different volume scenarios
    test_scenarios = [
        {"volumeUSD": "2500000", "description": "High Volume Market"},
        {"volumeUSD": "500000", "description": "Medium Volume Market"},
        {"volumeUSD": "50000", "description": "Low Volume Market"}
    ]
    
    for scenario in test_scenarios:
        trend = trading_data.analyze_market_trend(scenario)
        print(f"📊 {scenario['description']}: {trend}")
    
    print("\n🌐 Multi-Chain Support Demo...")
    print("="*40)
    
    # Show supported chains
    from config import GRAPH_ENDPOINTS
    print("Supported Networks:")
    for chain, endpoint in GRAPH_ENDPOINTS.items():
        print(f"   🔗 {chain.upper()}: {endpoint[:50]}...")
    
    print("\n🎉 Demo completed!")
    print("="*60)
    
    return True

async def simulate_user_conversation():
    """Simulate a realistic user conversation with the agent"""
    print("\n💬 Simulating User Conversation...")
    print("="*50)
    
    trading_data = TradingData()
    
    # Simulate a conversation flow
    conversation = [
        {
            "user": "Hello! I'm new to trading. Can you help me?",
            "agent_response": "🤖 NeuroTrade AI: Welcome! I'm here to help with trading analysis and recommendations. What would you like to know about the markets?"
        },
        {
            "user": "What's the current ETH price?",
            "agent_response": None  # Will be generated
        },
        {
            "user": "Should I buy ETH now?",
            "agent_response": None  # Will be generated
        },
        {
            "user": "What about swapping USDC to ETH?",
            "agent_response": None  # Will be generated
        },
        {
            "user": "Can you help with cross-chain trading?",
            "agent_response": None  # Will be generated
        }
    ]
    
    # Get market data for responses
    try:
        eth_price = await trading_data.get_eth_price()
        market_data = {"eth_price": eth_price}
    except:
        market_data = {"eth_price": 2456.78}
    
    print("User-Agent Conversation:")
    print("-" * 30)
    
    for i, turn in enumerate(conversation):
        print(f"\n👤 User: {turn['user']}")
        
        if turn['agent_response'] is None:
            # Generate response
            response = trading_data.generate_trading_recommendation(
                turn['user'], 
                market_data
            )
            print(f"🤖 Agent: {response}")
        else:
            print(f"🤖 Agent: {turn['agent_response']}")
        
        await asyncio.sleep(1)  # Simulate conversation timing
    
    print("\n✅ Conversation simulation completed!")

async def main():
    """Main demo function"""
    print("🚀 NeuroTrade AI Agent Interactive Demo")
    print("="*70)
    
    # Run AI capabilities demo
    await demo_ai_capabilities()
    
    # Run conversation simulation
    await simulate_user_conversation()
    
    print("\n🎯 How to use this agent:")
    print("="*40)
    print("1. 🔧 Set up your environment:")
    print("   python setup.py")
    print()
    print("2. 🧪 Test the agent:")
    print("   python test_agent.py")
    print()
    print("3. 🚀 Run the agent:")
    print("   python neurotrade_agent.py")
    print()
    print("4. 🌐 Find it on ASI:One:")
    print("   https://asi1.ai")
    print("   Search for 'NeuroTrade' or 'trading'")
    print()
    print("5. 💬 Start chatting:")
    print("   Ask questions like:")
    print("   - 'What's the ETH price?'")
    print("   - 'Should I buy ETH?'")
    print("   - 'Cross-chain trading advice'")
    print()
    print("🎉 Happy trading with NeuroTrade AI!")

if __name__ == "__main__":
    asyncio.run(main()) 