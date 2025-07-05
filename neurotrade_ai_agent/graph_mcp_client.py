import os
import json
import asyncio
import aiohttp
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class GraphMCPClient:
    """The Graph MCP Client using SSE (Server-Sent Events)"""
    
    def __init__(self):
        self.base_url = "https://token-api.mcp.thegraph.com"
        self.sse_url = "https://token-api.mcp.thegraph.com/sse"
        self.jwt_token = os.getenv("GRAPH_JWT")
        
        if not self.jwt_token:
            raise ValueError("GRAPH_JWT environment variable not found")
        
        self.headers = {
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
            "Cache-Control": "no-cache"
        }
        
        self.session = None
        self.available_tools = []
        self.connected = False
        self.session_id = None

    async def _get_session(self):
        """Get or create HTTP session"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session

    async def close(self):
        """Close the session"""
        if self.session:
            await self.session.close()
            self.session = None
        self.connected = False

    async def initialize_session(self) -> bool:
        """Initialize SSE session with The Graph MCP server"""
        try:
            logger.info("🔌 Initializing SSE session with The Graph MCP server...")
            session = await self._get_session()
            
            # Start SSE connection
            async with session.get(
                self.sse_url,
                headers=self.headers
            ) as response:
                
                if response.status == 200:
                    logger.info("✅ SSE connection established")
                    self.connected = True
                    
                    # Read initial SSE events
                    async for line in response.content:
                        line = line.decode('utf-8').strip()
                        
                        if line.startswith('data: '):
                            data_str = line[6:]  # Remove 'data: ' prefix
                            try:
                                data = json.loads(data_str)
                                if data.get("type") == "session_initialized":
                                    self.session_id = data.get("session_id")
                                    logger.info(f"✅ Session initialized: {self.session_id}")
                                    return True
                                elif data.get("type") == "tools_available":
                                    self.available_tools = data.get("tools", [])
                                    logger.info(f"📋 Available tools: {[t.get('name') for t in self.available_tools]}")
                                    
                            except json.JSONDecodeError as e:
                                logger.debug(f"Non-JSON SSE data: {data_str}")
                                continue
                        
                        # Break after getting session info
                        if self.session_id:
                            break
                    
                    return True
                else:
                    logger.error(f"SSE connection failed: {response.status}")
                    error_text = await response.text()
                    logger.error(f"Error response: {error_text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error initializing SSE session: {e}")
            return False

    async def list_tools(self) -> Optional[List[Dict]]:
        """List available tools"""
        if not self.connected:
            await self.initialize_session()
        
        if self.available_tools:
            return self.available_tools
            
        try:
            # Make tools/list request
            session = await self._get_session()
            
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list",
                "params": {}
            }
            
            async with session.post(
                self.base_url,
                json=payload,
                headers=self.headers
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    if "result" in data and "tools" in data["result"]:
                        self.available_tools = data["result"]["tools"]
                        return self.available_tools
                    else:
                        logger.error(f"Unexpected tools response: {data}")
                else:
                    logger.error(f"Tools list failed: {response.status}")
                    
        except Exception as e:
            logger.error(f"Error listing tools: {e}")
            
        return None

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any] = None) -> Optional[Dict]:
        """Call a specific tool"""
        if not self.connected:
            await self.initialize_session()
        
        try:
            session = await self._get_session()
            
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments or {}
                }
            }
            
            async with session.post(
                self.base_url,
                json=payload,
                headers=self.headers
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    if "result" in data:
                        return data["result"]
                    elif "error" in data:
                        return {"error": data["error"]}
                    else:
                        return {"error": "Unexpected response format"}
                else:
                    error_text = await response.text()
                    return {"error": f"HTTP {response.status}: {error_text}"}
                    
        except Exception as e:
            logger.error(f"Error calling tool {tool_name}: {e}")
            return {"error": str(e)}

    # Convenience methods for common tools
    async def get_token_data(self, token_address: str, chain: str = "ethereum") -> Optional[Dict]:
        """Get token data"""
        return await self.call_tool("get_token_data", {
            "token_address": token_address,
            "chain": chain
        })

    async def get_indexer_info(self, indexer_address: str = None) -> Optional[Dict]:
        """Get indexer information"""
        args = {}
        if indexer_address:
            args["indexer_address"] = indexer_address
        return await self.call_tool("get_indexer_info", args)

    async def get_allocations(self, indexer_address: str = None) -> Optional[Dict]:
        """Get allocation data"""
        args = {}
        if indexer_address:
            args["indexer_address"] = indexer_address
        return await self.call_tool("get_allocations", args)

    async def get_network_stats(self) -> Optional[Dict]:
        """Get network statistics"""
        return await self.call_tool("get_network_stats")

class GraphMCPQueryDispatcher:
    """Query dispatcher for The Graph MCP client"""
    
    def __init__(self, client: GraphMCPClient):
        self.client = client

    async def initialize(self):
        """Initialize the dispatcher"""
        await self.client.initialize_session()

    async def dispatch_query(self, query: str) -> str:
        """Dispatch a query to the appropriate tool"""
        query_lower = query.lower()
        
        try:
            # Token data queries
            if any(keyword in query_lower for keyword in ["token", "price", "eth", "usdc", "btc"]):
                if "eth" in query_lower:
                    result = await self.client.get_token_data("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")  # WETH
                elif "usdc" in query_lower:
                    result = await self.client.get_token_data("0xA0b86a33E6409eB80b4d3c6e34b85bd95e1d84E7")  # USDC
                else:
                    result = await self.client.get_token_data("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")  # Default ETH
                
                if result and "error" not in result:
                    return self._format_token_response(result)
                else:
                    return f"❌ Token data not available: {result.get('error', 'Unknown error')}"
            
            # Indexer queries
            elif "indexer" in query_lower:
                result = await self.client.get_indexer_info()
                if result and "error" not in result:
                    return self._format_indexer_response(result)
                else:
                    return f"❌ Indexer data not available: {result.get('error', 'Unknown error')}"
            
            # Allocation queries
            elif "allocation" in query_lower:
                result = await self.client.get_allocations()
                if result and "error" not in result:
                    return self._format_allocation_response(result)
                else:
                    return f"❌ Allocation data not available: {result.get('error', 'Unknown error')}"
            
            # Network stats queries
            elif any(keyword in query_lower for keyword in ["network", "stats", "statistics"]):
                result = await self.client.get_network_stats()
                if result and "error" not in result:
                    return self._format_network_response(result)
                else:
                    return f"❌ Network stats not available: {result.get('error', 'Unknown error')}"
            
            # General help
            else:
                tools = await self.client.list_tools()
                tool_names = [tool.get("name", "Unknown") for tool in tools] if tools else ["No tools available"]
                
                return f"""🤖 **The Graph MCP Client**

Available queries:
• **Token data**: "ETH price", "USDC token data"
• **Indexer info**: "show indexer information"
• **Allocations**: "allocation data"
• **Network stats**: "network statistics"

🔧 **Available tools**: {', '.join(tool_names)}

💡 Ask me about token prices, indexer metrics, or network data!"""
        
        except Exception as e:
            logger.error(f"Error dispatching query: {e}")
            return f"❌ Error processing query: {str(e)}"

    def _format_token_response(self, data: Dict) -> str:
        """Format token data response"""
        try:
            if "content" in data and data["content"]:
                content = data["content"][0]
                if "text" in content:
                    return f"💰 **Token Data**\n\n{content['text']}"
            
            return f"💰 **Token Data**\n\n{json.dumps(data, indent=2)}"
        except Exception:
            return f"💰 **Token Data**\n\nRaw response: {str(data)}"

    def _format_indexer_response(self, data: Dict) -> str:
        """Format indexer data response"""
        try:
            if "content" in data and data["content"]:
                content = data["content"][0]
                if "text" in content:
                    return f"🔍 **Indexer Information**\n\n{content['text']}"
            
            return f"🔍 **Indexer Information**\n\n{json.dumps(data, indent=2)}"
        except Exception:
            return f"🔍 **Indexer Information**\n\nRaw response: {str(data)}"

    def _format_allocation_response(self, data: Dict) -> str:
        """Format allocation data response"""
        try:
            if "content" in data and data["content"]:
                content = data["content"][0]
                if "text" in content:
                    return f"📊 **Allocation Data**\n\n{content['text']}"
            
            return f"📊 **Allocation Data**\n\n{json.dumps(data, indent=2)}"
        except Exception:
            return f"📊 **Allocation Data**\n\nRaw response: {str(data)}"

    def _format_network_response(self, data: Dict) -> str:
        """Format network stats response"""
        try:
            if "content" in data and data["content"]:
                content = data["content"][0]
                if "text" in content:
                    return f"🌐 **Network Statistics**\n\n{content['text']}"
            
            return f"🌐 **Network Statistics**\n\n{json.dumps(data, indent=2)}"
        except Exception:
            return f"🌐 **Network Statistics**\n\nRaw response: {str(data)}"

    async def close(self):
        """Close the dispatcher"""
        await self.client.close()

# Global instance
graph_mcp_client = None
graph_mcp_dispatcher = None

async def get_graph_mcp_client():
    """Get global MCP client instance"""
    global graph_mcp_client
    if graph_mcp_client is None:
        graph_mcp_client = GraphMCPClient()
        await graph_mcp_client.initialize_session()
    return graph_mcp_client

async def get_graph_mcp_dispatcher():
    """Get global MCP dispatcher instance"""
    global graph_mcp_dispatcher
    if graph_mcp_dispatcher is None:
        client = await get_graph_mcp_client()
        graph_mcp_dispatcher = GraphMCPQueryDispatcher(client)
    return graph_mcp_dispatcher

# Test function
async def test_graph_mcp_connection():
    """Test The Graph MCP connection"""
    print("🧪 Testing The Graph MCP connection...")
    
    try:
        client = GraphMCPClient()
        success = await client.initialize_session()
        
        if success:
            print("✅ SSE session initialized successfully")
            
            # List tools
            tools = await client.list_tools()
            if tools:
                print(f"📋 Available tools: {[t.get('name') for t in tools]}")
            
            # Test a tool
            if tools:
                first_tool = tools[0]["name"]
                print(f"🔧 Testing tool: {first_tool}")
                result = await client.call_tool(first_tool)
                if result and "error" not in result:
                    print("✅ Tool call successful")
                else:
                    print(f"❌ Tool call failed: {result}")
        else:
            print("❌ Failed to initialize SSE session")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(test_graph_mcp_connection()) 