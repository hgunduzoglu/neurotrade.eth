#!/usr/bin/env python3
"""
Test script for NeuroTrade AI Agent
This script tests the agent's functionality without running the full agent
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from neurotrade_agent import TradingData
except ImportError as e:
    print(f"❌ Failed to import TradingData: {e}")
    print("💡 Make sure uagents is properly installed")
    exit(1)

async def test_trading_data():
    """Test the TradingData class functionality"""
    print("🧪 Testing NeuroTrade AI Agent Components...")
    print("=" * 50)
    
    # Initialize trading data
    trading_data = TradingData()
    
    # Test 1: ETH Price Fetching
    print("\n1. Testing ETH Price Fetching...")
    try:
        eth_price = await trading_data.get_eth_price()
        if eth_price:
            print(f"   ✅ ETH Price: ${eth_price:.2f}")
        else:
            print("   ❌ Failed to fetch ETH price")
    except Exception as e:
        print(f"   ❌ Error fetching ETH price: {e}")
    
    # Test 2: Market Analysis
    print("\n2. Testing Market Analysis...")
    try:
        # Test with mock data
        mock_data = {"volumeUSD": "1500000"}
        trend = trading_data.analyze_market_trend(mock_data)
        print(f"   ✅ Market Trend: {trend}")
    except Exception as e:
        print(f"   ❌ Error in market analysis: {e}")
    
    # Test 3: AI Recommendations
    print("\n3. Testing AI Recommendations...")
    try:
        test_queries = [
            "Should I buy ETH now?",
            "What's the current ETH price?",
            "Should I swap USDC to ETH?",
            "Cross-chain trading advice",
            "Is it good time to sell?"
        ]
        
        market_data = {"eth_price": 2456.78}
        
        for query in test_queries:
            recommendation = trading_data.generate_trading_recommendation(query, market_data)
            print(f"   Query: {query}")
            print(f"   Response: {recommendation}")
            print()
    except Exception as e:
        print(f"   ❌ Error in AI recommendations: {e}")
    
    # Test 4: Configuration
    print("\n4. Testing Configuration...")
    try:
        from config import GRAPH_ENDPOINTS, COMMON_TOKENS
        print(f"   ✅ Graph Endpoints: {len(GRAPH_ENDPOINTS)} chains supported")
        print(f"   ✅ Common Tokens: {len(COMMON_TOKENS)} tokens configured")
        for chain in GRAPH_ENDPOINTS:
            print(f"      - {chain.upper()}: {GRAPH_ENDPOINTS[chain][:50]}...")
    except Exception as e:
        print(f"   ❌ Error in configuration: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Test completed!")

def test_agent_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing Agent Imports...")
    print("=" * 30)
    
    try:
        from uagents import Agent, Context, Protocol
        print("   ✅ uAgents framework imported successfully")
    except ImportError as e:
        print(f"   ❌ uAgents import failed: {e}")
        print("   💡 Run: pip install uagents")
        return False
    
    try:
        import aiohttp
        print("   ✅ aiohttp imported successfully")
    except ImportError as e:
        print(f"   ❌ aiohttp import failed: {e}")
        print("   💡 Run: pip install aiohttp")
        return False
    
    try:
        import requests
        print("   ✅ requests imported successfully")
    except ImportError as e:
        print(f"   ❌ requests import failed: {e}")
        print("   💡 Run: pip install requests")
        return False
    
    try:
        from dotenv import load_dotenv
        print("   ✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"   ❌ python-dotenv import failed: {e}")
        print("   💡 Run: pip install python-dotenv")
        return False
    
    print("   ✅ All imports successful!")
    return True

def check_environment():
    """Check environment setup"""
    print("\n🔧 Checking Environment...")
    print("=" * 30)
    
    # Check for .env file
    if os.path.exists('.env'):
        print("   ✅ .env file found")
    else:
        print("   ⚠️  .env file not found")
        print("   💡 Create a .env file with your AGENT_MAILBOX_KEY")
    
    # Check environment variables
    mailbox_key = os.getenv('AGENT_MAILBOX_KEY')
    if mailbox_key:
        print(f"   ✅ AGENT_MAILBOX_KEY configured (length: {len(mailbox_key)})")
    else:
        print("   ⚠️  AGENT_MAILBOX_KEY not set")
        print("   💡 Set your Agentverse mailbox key in .env")
    
    # Check Python version
    python_version = sys.version_info
    if python_version >= (3, 10):
        print(f"   ✅ Python version: {python_version.major}.{python_version.minor}")
    else:
        print(f"   ❌ Python version: {python_version.major}.{python_version.minor}")
        print("   💡 Python 3.10+ required")

async def main():
    """Main test function"""
    print("🚀 NeuroTrade AI Agent Test Suite")
    print("=" * 50)
    
    # Test imports
    if not test_agent_imports():
        print("\n❌ Import tests failed. Please install required dependencies.")
        return
    
    # Check environment
    check_environment()
    
    # Test trading data functionality
    await test_trading_data()
    
    print("\n🎯 Next Steps:")
    print("1. Set up your .env file with AGENT_MAILBOX_KEY")
    print("2. Run: python neurotrade_agent.py")
    print("3. Check ASI:One at https://asi1.ai for agent discovery")
    print("4. Test queries through the agent interface")

if __name__ == "__main__":
    asyncio.run(main()) 