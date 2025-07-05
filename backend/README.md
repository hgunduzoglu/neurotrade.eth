# NeuroTrade Backend API

Backend API for NeuroTrade cross-chain swap platform, integrating with 1inch Fusion+ SDK for token management and swapping functionality.

## Features

- 🪙 **Token Management**: Fetch available tokens from 1inch across multiple chains
- 🔗 **Cross-Chain Support**: Support for multiple blockchain networks
- 🛡️ **Security**: Helmet middleware for security headers
- 🌐 **CORS**: Configured for frontend integration
- 📝 **Request Logging**: Comprehensive logging for debugging
- ⚡ **Error Handling**: Robust error handling with proper HTTP status codes

## Quick Start

### Installation

```bash
cd backend
npm install
```

### Environment Configuration

Create a `.env` file in the backend directory:

```env
# 1inch API Configuration
ONEINCH_API_KEY=your_1inch_api_key_here

# Server Configuration
PORT=3001
NODE_ENV=development

# CORS Configuration (Frontend URL)
FRONTEND_URL=http://localhost:3000
```

**Note**: The API key in the example (`OxDeX7gMRlsxBKUA1yx1wO8mgteBPbLG`) is included as a fallback, but you should use your own 1inch API key for production.

### Start the Server

```bash
# Development mode with auto-restart
npm run dev

# Production mode
npm start
```

The server will start on `http://localhost:3001`

## API Endpoints

### Base URL
```
http://localhost:3001
```

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "OK",
  "message": "NeuroTrade Backend API is running",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "version": "1.0.0"
}
```

### Get All Tokens
```http
GET /api/tokens
```

**Query Parameters:**
- `provider` (optional): Token provider (default: "1inch")
- `country` (optional): Country code (default: "US")

**Example:**
```http
GET /api/tokens?provider=1inch&country=US
```

**Response:**
```json
{
  "success": true,
  "message": "Token list fetched successfully",
  "data": {
    "1": {
      "0x...": {
        "name": "Token Name",
        "symbol": "TKN",
        "decimals": 18,
        "address": "0x...",
        "logoURI": "https://..."
      }
    }
  },
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

### Get Tokens by Chain IDs
```http
GET /api/tokens/chains
```

**Query Parameters:**
- `chainIds` (required): Comma-separated chain IDs (e.g., "1,137,56")
- `provider` (optional): Token provider (default: "1inch")
- `country` (optional): Country code (default: "US")

**Example:**
```http
GET /api/tokens/chains?chainIds=1,137,56
```

**Response:**
```json
{
  "success": true,
  "message": "Tokens fetched successfully for chains: 1, 137, 56",
  "data": {
    "1": { "0x...": { "name": "Token", "symbol": "TKN" } },
    "137": { "0x...": { "name": "Token", "symbol": "TKN" } },
    "56": { "0x...": { "name": "Token", "symbol": "TKN" } }
  },
  "filteredChains": ["1", "137", "56"],
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

## Supported Chain IDs

Common chain IDs for testing:
- **1**: Ethereum Mainnet
- **137**: Polygon
- **56**: BNB Smart Chain
- **42161**: Arbitrum One
- **10**: Optimism
- **43114**: Avalanche C-Chain

## Frontend Integration

### Example Fetch Usage

```javascript
// Fetch all tokens
const response = await fetch('http://localhost:3001/api/tokens');
const data = await response.json();

// Fetch tokens for specific chains
const chainResponse = await fetch('http://localhost:3001/api/tokens/chains?chainIds=1,137');
const chainData = await chainResponse.json();
```

### React Hook Example

```javascript
import { useState, useEffect } from 'react';

export const useTokens = (chainIds = []) => {
  const [tokens, setTokens] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTokens = async () => {
      try {
        setLoading(true);
        const url = chainIds.length > 0 
          ? `http://localhost:3001/api/tokens/chains?chainIds=${chainIds.join(',')}`
          : 'http://localhost:3001/api/tokens';
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.success) {
          setTokens(data.data);
        } else {
          setError(data.error);
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchTokens();
  }, [chainIds]);

  return { tokens, loading, error };
};
```

## Error Handling

All endpoints return consistent error responses:

```json
{
  "success": false,
  "message": "Error description",
  "error": {
    "message": "Detailed error message",
    "status": 404,
    "code": "ERROR_CODE"
  },
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

## Development

### Project Structure

```
backend/
├── config.js              # Environment configuration
├── server.js              # Main Express server
├── services/
│   └── oneInchService.js   # 1inch API integration
├── routes/
│   └── tokens.js           # Token-related endpoints
├── package.json
└── README.md
```

### Adding New Endpoints

1. Create a new route file in `/routes/`
2. Import and use it in `server.js`
3. Add corresponding service methods if needed

### Testing

Test the API using curl:

```bash
# Health check
curl http://localhost:3001/health

# Get all tokens
curl http://localhost:3001/api/tokens

# Get tokens for specific chains
curl "http://localhost:3001/api/tokens/chains?chainIds=1,137"
```

## Next Steps

This token endpoint provides the foundation for 1inch Fusion+ SDK integration. Next steps include:

1. **Quote Endpoint**: Implement swap quote calculation
2. **Order Creation**: Create and submit swap orders
3. **Order Status**: Track order execution status
4. **Transaction History**: Store and retrieve swap history
5. **Gas Estimation**: Provide gas cost estimates

## Security Notes

- Never commit your actual API keys to version control
- Use environment variables for all sensitive configuration
- The current setup includes basic security headers via Helmet
- Consider adding rate limiting for production use
- Validate all user inputs and sanitize data

## Support

For issues related to:
- **1inch API**: Check [1inch Developer Portal](https://portal.1inch.dev/)
- **Backend Setup**: Review this README and check server logs
- **CORS Issues**: Verify frontend URL in configuration 