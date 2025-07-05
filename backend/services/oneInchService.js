const axios = require('axios');
const config = require('../config');

class OneInchService {
  constructor() {
    this.baseUrl = config.oneInch.baseUrl;
    this.apiKey = config.oneInch.apiKey;
    this.defaultProvider = config.oneInch.defaultProvider;
    this.defaultCountry = config.oneInch.defaultCountry;
  }

  /**
   * Fetch token list from 1inch API
   * @param {string} provider - Token provider (default: '1inch')
   * @param {string} country - Country code (default: 'US')
   * @returns {Promise<Object>} Token list data
   */
  async getTokenList(provider = this.defaultProvider, country = this.defaultCountry) {
    try {
      const url = `${this.baseUrl}/token/v1.3/multi-chain/token-list`;
      
      const config = {
        headers: {
          "Authorization": `Bearer ${this.apiKey}`,
          "Content-Type": "application/json"
        },
        params: {
          provider,
          country
        },
        paramsSerializer: {
          indexes: null
        }
      };

      console.log(`Fetching token list from 1inch API...`);
      const response = await axios.get(url, config);
      
      // Debug: Log the raw response structure
      console.log('1inch API Response Structure:', {
        isArray: Array.isArray(response.data),
        type: typeof response.data,
        keys: response.data ? Object.keys(response.data) : [],
        sample: response.data ? JSON.stringify(response.data).slice(0, 200) + '...' : 'null'
      });

      // Ensure we have a valid response
      if (!response.data || typeof response.data !== 'object') {
        throw new Error('Invalid response from 1inch API');
      }

      // The 1inch API returns tokens as an object with chain IDs as keys
      const tokens = response.data.tokens || response.data;
      
      // Transform the response into our expected format
      const tokenArray = Object.entries(tokens).map(([address, token]) => ({
        address,
        ...token,
        chainId: parseInt(token.chainId || '1', 10) // Default to Ethereum mainnet if not specified
      }));

      console.log(`Processed ${tokenArray.length} tokens from 1inch API`);
      
      return {
        success: true,
        data: tokenArray,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      console.error('Error fetching token list:', error.response?.data || error.message);
      
      return {
        success: false,
        error: {
          message: error.response?.data?.message || error.message,
          status: error.response?.status || 500,
          code: error.response?.data?.code || 'UNKNOWN_ERROR'
        },
        timestamp: new Date().toISOString()
      };
    }
  }

  /**
   * Get tokens for specific chains
   * @param {Array} chainIds - Array of chain IDs to filter
   * @returns {Promise<Object>} Filtered token data
   */
  async getTokensByChains(chainIds = []) {
    try {
      const tokenListResponse = await this.getTokenList();
      
      if (!tokenListResponse.success) {
        return tokenListResponse;
      }

      const allTokens = tokenListResponse.data;
      
      if (!Array.isArray(allTokens)) {
        throw new Error('Invalid token data format received from 1inch API');
      }
      
      if (chainIds.length === 0) {
        return {
          success: true,
          data: allTokens,
          timestamp: new Date().toISOString(),
          filteredChains: [],
          totalTokens: allTokens.length,
          filteredCount: allTokens.length
        };
      }

      // Filter tokens by chain IDs
      const filteredTokens = allTokens.filter(token => 
        chainIds.includes(token.chainId)
      );

      console.log(`Filtered ${filteredTokens.length} tokens from ${allTokens.length} total for chains: ${chainIds.join(', ')}`);

      if (filteredTokens.length === 0) {
        throw new Error(`No tokens found for chain IDs: ${chainIds.join(', ')}`);
      }

      return {
        success: true,
        data: filteredTokens,
        timestamp: new Date().toISOString(),
        filteredChains: chainIds,
        totalTokens: allTokens.length,
        filteredCount: filteredTokens.length
      };
    } catch (error) {
      console.error('Error filtering tokens by chains:', error.message);
      return {
        success: false,
        error: {
          message: error.message,
          code: 'FILTER_ERROR'
        },
        timestamp: new Date().toISOString()
      };
    }
  }
}

module.exports = new OneInchService(); 