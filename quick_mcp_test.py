#!/usr/bin/env python3
"""
Quick test for The Graph MCP connection
Run this after adding GRAPH_JWT to your .env file
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def quick_test():
    """Quick test of MCP connection"""
    
    # Check if JWT token is available
    jwt_token = os.getenv("GRAPH_JWT")
    
    if not jwt_token:
        print("❌ GRAPH_JWT not found in environment!")
        print("💡 Steps to fix:")
        print("   1. Copy env_template.txt to .env")
        print("   2. Add your JWT token to GRAPH_JWT in .env")
        print("   3. Run this test again")
        return
    
    print(f"✅ JWT Token found: {jwt_token[:20]}...")
    print("🧪 Testing The Graph MCP connection...")
    
    try:
        # Import after checking JWT
        from neurotrade_ai_agent.graph_mcp_client import GraphMCPClient
        
        client = GraphMCPClient()
        
        # Test connection
        print("📡 Connecting to https://token-api.mcp.thegraph.com/sse ...")
        success = await client.initialize_session()
        
        if success:
            print("✅ SSE connection successful!")
            print(f"Session ID: {client.session_id}")
            
            # List tools
            tools = await client.list_tools()
            if tools:
                print(f"✅ Found {len(tools)} tools:")
                for tool in tools:
                    name = tool.get("name", "Unknown")
                    print(f"   • {name}")
                
                # Test first tool
                if tools:
                    first_tool = tools[0]["name"]
                    print(f"\n🔧 Testing tool: {first_tool}")
                    result = await client.call_tool(first_tool)
                    
                    if result and "error" not in result:
                        print("✅ Tool call successful!")
                    else:
                        print(f"⚠️ Tool call returned: {result}")
            else:
                print("❌ No tools found - check your JWT token")
        else:
            print("❌ SSE connection failed - check your JWT token")
        
        await client.close()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're in the right directory")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("💡 Check your JWT token and internet connection")

if __name__ == "__main__":
    print("🚀 NeuroTrade MCP Quick Test")
    print("-" * 30)
    asyncio.run(quick_test()) 