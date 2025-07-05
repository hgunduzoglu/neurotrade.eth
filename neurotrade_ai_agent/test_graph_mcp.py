#!/usr/bin/env python3
"""
Test script for The Graph MCP SSE client
"""
import asyncio
import os
from dotenv import load_dotenv
from graph_mcp_client import GraphMCPClient, GraphMCPQueryDispatcher

load_dotenv()

async def test_sse_connection():
    """Test SSE connection to The Graph MCP server"""
    print("🧪 Testing The Graph MCP SSE Connection")
    print("=" * 50)
    
    # Check JWT token
    jwt_token = os.getenv("GRAPH_JWT")
    if not jwt_token:
        print("❌ GRAPH_JWT not found in environment!")
        print("💡 Add your JWT token to .env file")
        return
    
    print(f"✅ JWT Token found: {jwt_token[:20]}...")
    
    try:
        client = GraphMCPClient()
        print("📡 Initializing SSE session...")
        
        # Initialize session
        success = await client.initialize_session()
        
        if success:
            print(f"✅ SSE session initialized. Session ID: {client.session_id}")
            
            # Test tool listing
            print("\n📋 Listing available tools...")
            tools = await client.list_tools()
            
            if tools:
                print(f"✅ Found {len(tools)} tools:")
                for i, tool in enumerate(tools, 1):
                    name = tool.get("name", "Unknown")
                    description = tool.get("description", "No description")
                    print(f"   {i}. {name} - {description}")
            else:
                print("❌ No tools found")
                
            print("\n🔧 Testing individual tools...")
            
            # Test each tool
            if tools:
                for tool in tools:
                    tool_name = tool.get("name")
                    print(f"\n🧪 Testing {tool_name}...")
                    
                    try:
                        result = await client.call_tool(tool_name)
                        if result and "error" not in result:
                            print(f"✅ {tool_name}: Success")
                            # Print preview
                            result_str = str(result)
                            if len(result_str) > 200:
                                print(f"   Preview: {result_str[:200]}...")
                            else:
                                print(f"   Result: {result_str}")
                        else:
                            print(f"❌ {tool_name}: {result}")
                    except Exception as e:
                        print(f"❌ {tool_name}: Error - {e}")
                        
        else:
            print("❌ Failed to initialize SSE session")
            
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        
    finally:
        await client.close()

async def test_query_dispatcher():
    """Test query dispatcher"""
    print("\n🤖 Testing Query Dispatcher")
    print("=" * 50)
    
    try:
        client = GraphMCPClient()
        await client.initialize_session()
        
        dispatcher = GraphMCPQueryDispatcher(client)
        
        # Test queries
        test_queries = [
            "show me indexer information",
            "get network statistics",
            "ETH token data",
            "allocation data",
            "help"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Query: '{query}'")
            try:
                response = await dispatcher.dispatch_query(query)
                print(f"📝 Response: {response[:300]}..." if len(response) > 300 else response)
            except Exception as e:
                print(f"❌ Error: {e}")
                
    except Exception as e:
        print(f"❌ Dispatcher test failed: {e}")
        
    finally:
        await client.close()

async def interactive_test():
    """Interactive test mode"""
    print("\n🎮 Interactive Test Mode")
    print("Type your queries or 'quit' to exit")
    print("=" * 50)
    
    try:
        client = GraphMCPClient()
        await client.initialize_session()
        
        if not client.connected:
            print("❌ Failed to connect to MCP server")
            return
            
        dispatcher = GraphMCPQueryDispatcher(client)
        
        while True:
            query = input("\n🔍 Enter query: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                break
                
            if not query:
                continue
                
            try:
                response = await dispatcher.dispatch_query(query)
                print(f"\n📝 Response:\n{response}")
            except Exception as e:
                print(f"❌ Error: {e}")
                
    except KeyboardInterrupt:
        print("\n👋 Exiting...")
    except Exception as e:
        print(f"❌ Interactive test failed: {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    print("🚀 The Graph MCP SSE Test Suite")
    print("1. Connection test")
    print("2. Query dispatcher test")
    print("3. Interactive test")
    print("4. All tests")
    
    choice = input("\nSelect test mode (1-4): ").strip()
    
    if choice == "1":
        asyncio.run(test_sse_connection())
    elif choice == "2":
        asyncio.run(test_query_dispatcher())
    elif choice == "3":
        asyncio.run(interactive_test())
    elif choice == "4":
        asyncio.run(test_sse_connection())
        asyncio.run(test_query_dispatcher())
    else:
        print("Invalid choice, running connection test...")
        asyncio.run(test_sse_connection()) 