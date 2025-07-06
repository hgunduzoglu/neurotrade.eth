#!/usr/bin/env python3
"""
Test script for The Graph MCP Integration
Tests the official MCP Python SDK implementation
"""
import asyncio
import logging
from dotenv import load_dotenv

from thegraph_mcp_client import (
    TheGraphMCPClient,
    TheGraphMCPDispatcher,
    get_graph_mcp_client,
    get_graph_mcp_dispatcher,
    test_graph_mcp_connection
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_mcp_client_direct():
    """Test The Graph MCP client directly"""
    print("\n🧪 Testing The Graph MCP Client Direct Connection...")
    
    try:
        # Create client
        client = TheGraphMCPClient()
        
        # Test connection
        connected = await client.test_connection("token-api")
        
        if connected:
            print("✅ Connected to The Graph Token API MCP server")
            
            # Test available tools (loaded during connection test)
            if client.tools:
                print(f"📋 Available tools ({len(client.tools)}):")
                for tool in client.tools:
                    print(f"  - {tool.name}: {tool.description if hasattr(tool, 'description') else 'No description'}")
            else:
                print("⚠️ No tools available")
            
            # Test available resources (loaded during connection test)
            if client.resources:
                print(f"📋 Available resources ({len(client.resources)}):")
                for resource in client.resources:
                    print(f"  - {resource.uri}")
            else:
                print("⚠️ No resources available")
            
            # Test token price query
            print("\n🔍 Testing token price query...")
            result = await client.get_token_price("ETH")
            print(f"ETH Price Result: {result}")
            
            # Test generic tool call
            print("\n🔍 Testing generic tool call...")
            result = await client.call_tool("get_token_price", {"symbol": "BTC"})
            print(f"BTC Price Result: {result}")
            
            print("✅ Client test completed successfully")
            
        else:
            print("❌ Failed to connect to The Graph MCP server")
            
    except Exception as e:
        print(f"❌ Client test failed: {e}")
        import traceback
        traceback.print_exc()

async def test_mcp_dispatcher():
    """Test The Graph MCP dispatcher"""
    print("\n🧪 Testing The Graph MCP Dispatcher...")
    
    try:
        # Create dispatcher
        dispatcher = TheGraphMCPDispatcher()
        
        # Initialize
        await dispatcher.initialize()
        
        if dispatcher.token_api_connected:
            print("✅ Dispatcher initialized and connected")
            
            # Test various query types
            test_queries = [
                "What's the current ETH price?",
                "Show me Bitcoin price",
                "USDC token price",
                "Check wallet balance",
                "Recent transfers",
                "Top token holders",
                "General trading info"
            ]
            
            for query in test_queries:
                print(f"\n🔍 Testing query: '{query}'")
                result = await dispatcher.dispatch_query(query)
                print(f"Response: {result[:200]}...")  # Show first 200 chars
                
            print("✅ Dispatcher test completed successfully")
            
        else:
            print("❌ Dispatcher failed to connect")
            
    except Exception as e:
        print(f"❌ Dispatcher test failed: {e}")
        import traceback
        traceback.print_exc()

async def test_convenience_functions():
    """Test convenience functions"""
    print("\n🧪 Testing Convenience Functions...")
    
    try:
        # Test get_graph_mcp_client
        print("Testing get_graph_mcp_client()...")
        client = await get_graph_mcp_client()
        
        if client.connection_tested:
            print("✅ Convenience client function works")
        else:
            print("⚠️ Convenience client function returned untested client")
        
        # Test get_graph_mcp_dispatcher  
        print("Testing get_graph_mcp_dispatcher()...")
        dispatcher = await get_graph_mcp_dispatcher()
        
        if dispatcher.token_api_connected:
            print("✅ Convenience dispatcher function works")
            
            # Test a quick query
            result = await dispatcher.dispatch_query("ETH price")
            print(f"Quick query result: {result[:100]}...")
            
        else:
            print("⚠️ Convenience dispatcher function returned disconnected dispatcher")
            
    except Exception as e:
        print(f"❌ Convenience functions test failed: {e}")

async def test_chat_protocol_integration():
    """Test integration with chat protocol"""
    print("\n🧪 Testing Chat Protocol Integration...")
    
    try:
        # Test importing chat protocol with updated MCP client
        from chat_proto import get_trading_info
        
        # Test trading info function
        result = await get_trading_info("What's the ETH price?")
        print(f"Trading info result: {result[:200]}...")
        
        result = await get_trading_info("Show me Bitcoin price")
        print(f"Bitcoin price result: {result[:200]}...")
        
        print("✅ Chat protocol integration test completed")
        
    except Exception as e:
        print(f"❌ Chat protocol integration test failed: {e}")
        import traceback
        traceback.print_exc()

async def run_all_tests():
    """Run all tests"""
    print("🚀 Starting The Graph MCP Integration Tests...")
    print("=" * 60)
    
    # Test basic connection
    await test_graph_mcp_connection()
    
    # Test client directly
    await test_mcp_client_direct()
    
    # Test dispatcher
    await test_mcp_dispatcher()
    
    # Test convenience functions
    await test_convenience_functions()
    
    # Test chat protocol integration
    await test_chat_protocol_integration()
    
    print("\n" + "=" * 60)
    print("🎯 All The Graph MCP Integration Tests Completed!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_all_tests()) 