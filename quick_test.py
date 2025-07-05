#!/usr/bin/env python3
"""
Quick test to verify NeuroTrade AI Agent can start
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_imports():
    """Test that all imports work"""
    print("🧪 Testing imports...")
    
    try:
        from uagents import Agent, Context, Model
        print("✅ uAgents imports successful")
    except ImportError as e:
        print(f"❌ uAgents import failed: {e}")
        return False
    
    try:
        import aiohttp
        print("✅ aiohttp import successful")
    except ImportError as e:
        print(f"❌ aiohttp import failed: {e}")
        return False
    
    try:
        from neurotrade_agent import TradingData, TradingQueryMessage
        print("✅ NeuroTrade agent imports successful")
    except ImportError as e:
        print(f"❌ NeuroTrade agent import failed: {e}")
        return False
    
    return True

def test_agent_creation():
    """Test that agent can be created without errors"""
    print("\n🤖 Testing agent creation...")
    
    try:
        from uagents import Agent
        
        # Try creating a simple agent
        test_agent = Agent(
            name="Test Agent",
            seed="test_seed_123",
            port=8001,
        )
        
        print(f"✅ Test agent created successfully")
        print(f"   Address: {test_agent.address}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        return False

def test_configuration():
    """Test configuration loading"""
    print("\n🔧 Testing configuration...")
    
    try:
        from config import GRAPH_ENDPOINTS, COMMON_TOKENS
        print(f"✅ Configuration loaded successfully")
        print(f"   Supported chains: {len(GRAPH_ENDPOINTS)}")
        print(f"   Common tokens: {len(COMMON_TOKENS)}")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 NeuroTrade AI Agent Quick Test")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Agent Creation Test", test_agent_creation),
        ("Configuration Test", test_configuration),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
        
        print("-" * 30)
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Agent should start successfully.")
        print("\n💡 Next steps:")
        print("1. Set up your .env file with AGENT_MAILBOX_KEY")
        print("2. Run: python neurotrade_agent.py")
        return True
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 