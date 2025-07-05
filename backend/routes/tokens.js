const express = require('express');
const router = express.Router();
const oneInchService = require('../services/oneInchService');

/**
 * GET /api/tokens
 * Fetch all available tokens from 1inch
 * Query parameters:
 * - provider: Token provider (optional, default: '1inch')
 * - country: Country code (optional, default: 'US')
 */
router.get('/', async (req, res) => {
  try {
    const { provider, country } = req.query;
    
    console.log('Fetching token list with params:', { provider, country });
    
    const result = await oneInchService.getTokenList(provider, country);
    
    if (result.success) {
      res.json({
        success: true,
        message: 'Token list fetched successfully',
        data: result.data,
        timestamp: result.timestamp
      });
    } else {
      res.status(result.error.status || 500).json({
        success: false,
        message: 'Failed to fetch token list',
        error: result.error,
        timestamp: result.timestamp
      });
    }
  } catch (error) {
    console.error('Unexpected error in tokens route:', error);
    res.status(500).json({
      success: false,
      message: 'Internal server error',
      error: {
        message: error.message,
        code: 'INTERNAL_ERROR'
      },
      timestamp: new Date().toISOString()
    });
  }
});

/**
 * GET /api/tokens/chains
 * Fetch tokens for specific chain IDs
 * Query parameters:
 * - chainIds: Comma-separated chain IDs (e.g., "1,137,56")
 * - provider: Token provider (optional, default: '1inch')
 * - country: Country code (optional, default: 'US')
 */
router.get('/chains', async (req, res) => {
  try {
    const { chainIds, provider, country } = req.query;
    
    let chainIdArray = [];
    if (chainIds) {
      // Validate and convert chain IDs
      chainIdArray = chainIds.split(',')
        .map(id => id.trim())
        .filter(id => id && !isNaN(parseInt(id, 10)))
        .map(id => parseInt(id, 10));
      
      if (chainIdArray.length === 0) {
        throw new Error('No valid chain IDs provided');
      }
    }
    
    console.log('Fetching tokens for chains:', chainIdArray);
    
    const result = await oneInchService.getTokensByChains(chainIdArray);
    
    if (result.success) {
      res.json({
        success: true,
        message: chainIdArray.length > 0 
          ? `Tokens fetched successfully for chains: ${chainIdArray.join(', ')}` 
          : 'All tokens fetched successfully',
        data: result.data,
        filteredChains: result.filteredChains,
        totalTokens: result.totalTokens,
        filteredCount: result.filteredCount,
        timestamp: result.timestamp
      });
    } else {
      res.status(result.error?.status || 500).json({
        success: false,
        message: 'Failed to fetch tokens for specified chains',
        error: result.error,
        timestamp: result.timestamp
      });
    }
  } catch (error) {
    console.error('Unexpected error in tokens/chains route:', error);
    res.status(500).json({
      success: false,
      message: 'Failed to fetch tokens for specified chains',
      error: {
        message: error.message,
        code: 'INTERNAL_ERROR'
      },
      timestamp: new Date().toISOString()
    });
  }
});

module.exports = router; 