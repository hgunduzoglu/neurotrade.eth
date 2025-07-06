# Cross-Chain Swap Feature

This document describes the cross-chain swap feature implemented using 1inch Fusion+ API in NeuroTrade.eth.

## Overview

The cross-chain swap feature allows users to swap tokens between different blockchain networks in a single transaction. This is powered by 1inch Fusion+ API, which provides secure and efficient cross-chain swaps with competitive rates.

## Features

- Swap tokens across multiple chains (Ethereum, Polygon, BSC, Arbitrum, Optimism)
- Real-time quotes and price updates
- Multiple speed presets (fast, medium, slow)
- Transaction status tracking
- Automatic network switching
- Token approval management

## Setup

1. Start the swap API service:
   ```bash
   cd swap_api
   npm install
   npm run dev
   ```

2. Configure environment variables in `.env.local`:
   ```
   NEXT_PUBLIC_SWAP_API_URL=http://localhost:5173
   NEXT_PUBLIC_ETHEREUM_RPC_URL=your_ethereum_rpc_url
   NEXT_PUBLIC_POLYGON_RPC_URL=your_polygon_rpc_url
   NEXT_PUBLIC_BSC_RPC_URL=your_bsc_rpc_url
   NEXT_PUBLIC_ARBITRUM_RPC_URL=your_arbitrum_rpc_url
   NEXT_PUBLIC_OPTIMISM_RPC_URL=your_optimism_rpc_url
   ```

## Usage

1. Connect your wallet
2. Select source and destination chains
3. Choose tokens to swap
4. Enter the amount
5. Select speed preset
6. Get quote and review details
7. Approve token spending (if needed)
8. Submit the swap order
9. Monitor transaction status

## Architecture

The feature consists of two main components:

1. Swap API Service (`swap_api/`)
   - Handles communication with 1inch Fusion+ API
   - Manages order lifecycle
   - Handles secret management for orders

2. Frontend Integration (`src/pages/swap.tsx`)
   - User interface for swap operations
   - Wallet connection and network management
   - Transaction status monitoring
   - Token approval handling

## Error Handling

The implementation includes comprehensive error handling for:
- Network connection issues
- Insufficient balance
- Token approval failures
- Network switching errors
- Order submission failures
- Quote expiration

## Security Considerations

1. Token Approvals
   - Uses standard ERC20 approve mechanism
   - Implements allowance checking
   - Supports revoking approvals

2. Transaction Signing
   - Uses typed data signing (EIP-712)
   - Validates all signatures client-side
   - Implements proper nonce management

3. Network Security
   - Validates chain IDs
   - Verifies contract addresses
   - Implements proper error handling

## Limitations

1. Supported Chains
   - Currently limited to Ethereum, Polygon, BSC, Arbitrum, and Optimism
   - Adding new chains requires configuration updates

2. Token Support
   - Limited to tokens supported by 1inch Fusion+
   - Some tokens might not be available for cross-chain swaps

3. Speed Presets
   - Trade-off between speed and cost
   - Actual transaction times may vary based on network conditions

## Future Improvements

1. Additional Features
   - Price alerts
   - Swap history
   - Favorite token pairs
   - Custom speed presets

2. Performance Optimizations
   - Caching token lists
   - Optimizing network requests
   - Implementing batch quotes

3. User Experience
   - Better error messages
   - Transaction progress visualization
   - Price impact warnings
   - Gas cost estimations 