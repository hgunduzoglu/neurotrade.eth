# mcpsdk_try.py
import os
import asyncio
from mcp.client.streamable_http import streamablehttp_client
from mcp.client.session import ClientSession

async def main():
    token = "eyJhbGciOiJLTVNFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3ODc3Mzc2NjMsImp0aSI6ImQ2Y2M0MTU5LTE4MDctNDM5My04NGJkLWM3NjczOThhMjhlYSIsImlhdCI6MTc1MTczNzY2MywiaXNzIjoiZGZ1c2UuaW8iLCJzdWIiOiIwbWF0YWIxMTgzMmQwZDhjYmQ3NWIiLCJ2IjoxLCJha2kiOiIxOGRjNTUxMGYxOTc5MWQwNzU0NDYxZGJmYjllNDk2NzNiYTZkMjIwZjc0ZGJhYWUzNTVjYWFiMTU1M2ZiOTdlIiwidWlkIjoiMG1hdGFiMTE4MzJkMGQ4Y2JkNzViIn0.FEY8Q0xkhit8SirTBaiORr1-Xc_plFA4qHqbHzhp9KEZFhhCE347HuU3vqgPGaU4zRe0WklyqS2YZkAkmnE0cg"          # .env veya ortam değişkeniniz
    if not token:
        raise RuntimeError("GRAPH_JWT env var missing")

    async with streamablehttp_client(
        "https://token-api.mcp.thegraph.com/mcp",
        headers={"Authorization": f"Bearer {token}"}
    ) as (read, write, _):

        async with ClientSession(read, write) as session:
            await session.initialize()      # handshake
            tools = await session.list_tools()
            print("Available tools:")
            for t in tools.tools:
                print(" •", t.name)

if __name__ == "__main__":
    asyncio.run(main())
