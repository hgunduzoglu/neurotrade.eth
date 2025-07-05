"""
NeuroTrade AI Agent Configuration
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Agent Configuration
AGENT_MAILBOX_KEY = os.getenv("AGENT_MAILBOX_KEY", "")
AGENT_SEED = os.getenv("AGENT_SEED", "neurotrade_ai_agent_seed_2024")
AGENT_PORT = int(os.getenv("AGENT_PORT", "8000"))

# The Graph API Configuration
GRAPH_API_KEY = os.getenv("GRAPH_API_KEY", "")

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# The Graph endpoints for different chains
GRAPH_ENDPOINTS = {
    "ethereum": "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3",
    "arbitrum": "https://api.thegraph.com/subgraphs/name/ianlapham/arbitrum-minimal", 
    "polygon": "https://api.thegraph.com/subgraphs/name/ianlapham/uniswap-v3-polygon",
    "optimism": "https://api.thegraph.com/subgraphs/name/ianlapham/optimism-post-regenesis",
    "base": "https://api.thegraph.com/subgraphs/name/ianlapham/uniswap-v3-base"
}

# Trading pairs and token addresses
COMMON_TOKENS = {
    "ETH": "0x0000000000000000000000000000000000000000",
    "USDC": "0xa0b86a33e6160cd60e0f34cf62aa6b7442b5b8b7",
    "USDT": "0xdac17f958d2ee523a2206206994597c13d831ec7",
    "WETH": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
}

# Default trading parameters
DEFAULT_SLIPPAGE = 0.5  # 0.5%
DEFAULT_GAS_LIMIT = 300000
MIN_LIQUIDITY_USD = 10000  # Minimum liquidity for recommendations 