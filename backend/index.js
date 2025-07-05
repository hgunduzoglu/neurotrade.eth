require('dotenv').config();
const express = require('express');
const cors = require('cors');
const axios = require('axios');

const app = express();
const port = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

// Test endpoint
app.get('/test', (req, res) => {
  res.json({ message: 'Backend is working!' });
});

// Quote endpoint
app.get('/quote', async (req, res) => {
  try {
    const { 
      // Support both old and new parameter names
      fromTokenAddress,
      toTokenAddress,
      srcTokenAddress = fromTokenAddress,
      dstTokenAddress = toTokenAddress,
      srcChain = process.env.CHAIN_ID || '1',  // Default to Ethereum mainnet
      dstChain = process.env.CHAIN_ID || '1',  // Default to Ethereum mainnet
      amount,
      walletAddress,
      enableEstimate = false,
      fee = 0,
      isPermit2,
      permit
    } = req.query;

    // Validate required parameters
    if (!srcTokenAddress || !dstTokenAddress || !amount || !walletAddress) {
      return res.status(400).json({ 
        error: 'Missing required parameters',
        required: ['srcTokenAddress or fromTokenAddress', 'dstTokenAddress or toTokenAddress', 'amount', 'walletAddress']
      });
    }

    // Ensure wallet address is properly formatted
    if (!walletAddress.match(/^0x[a-fA-F0-9]{40}$/)) {
      return res.status(400).json({
        error: 'Invalid wallet address format',
        walletAddress
      });
    }

    const baseUrl = 'https://api.1inch.dev/fusion-plus/quoter/v1.0';
    const quoteUrl = `${baseUrl}/quote/receive`;
    
    // Format parameters with explicit string conversions
    const params = {
      srcChain: String(srcChain),
      dstChain: String(dstChain),
      srcTokenAddress: srcTokenAddress.toLowerCase(),
      dstTokenAddress: dstTokenAddress.toLowerCase(),
      amount: String(amount),
      walletAddress: walletAddress.toLowerCase(),
      enableEstimate: String(enableEstimate),
      fee: String(fee),
      ...(isPermit2 && { isPermit2: String(isPermit2) }),
      ...(permit && { permit })
    };

    console.log('Fetching quote from:', quoteUrl);
    console.log('Request params:', params);
    console.log('Request headers:', {
      'Accept': 'application/json',
      'Authorization': `Bearer ${process.env.INCH_API_KEY.slice(0, 5)}...`
    });

    const response = await axios.get(quoteUrl, {
      headers: {
        'Accept': 'application/json',
        'Authorization': `Bearer ${process.env.INCH_API_KEY}`
      },
      params
    });

    res.json(response.data);

  } catch (error) {
    console.error('Quote error:', error.response?.data || error.message);
    console.error('Full error object:', error);
    
    res.status(error.response?.status || 500).json({
      error: 'Failed to fetch quote',
      details: error.response?.data || error.message,
      requestInfo: {
        url: error.config?.url,
        method: error.config?.method,
        headers: error.config?.headers,
        params: error.config?.params
      }
    });
  }
});

// Build swap order endpoint
app.post('/swap/build', async (req, res) => {
  try {
    const { 
      srcChain,
      dstChain,
      srcTokenAddress,
      dstTokenAddress,
      amount,
      walletAddress,
      fee = 0,
      source = 'Frontend',
      isPermit2,
      isMobile = false,
      feeReceiver,
      permit,
      preset = 'fast'
    } = req.body;

    // Validate required parameters
    if (!srcChain || !dstChain || !srcTokenAddress || !dstTokenAddress || !amount || !walletAddress) {
      return res.status(400).json({ 
        error: 'Missing required parameters',
        required: ['srcChain', 'dstChain', 'srcTokenAddress', 'dstTokenAddress', 'amount', 'walletAddress']
      });
    }

    // Ensure wallet address is properly formatted
    if (!walletAddress.match(/^0x[a-fA-F0-9]{40}$/)) {
      return res.status(400).json({
        error: 'Invalid wallet address format',
        walletAddress
      });
    }

    const baseUrl = 'https://api.1inch.dev/fusion-plus/quoter/v1.0';
    const buildUrl = `${baseUrl}/quote/build`;
    
    console.log('Building swap order at:', buildUrl);
    
    // Format request body with explicit string conversions
    const requestBody = {
      srcChain: String(srcChain),
      dstChain: String(dstChain),
      srcTokenAddress: srcTokenAddress.toLowerCase(),
      dstTokenAddress: dstTokenAddress.toLowerCase(),
      amount: String(amount),
      walletAddress: walletAddress.toLowerCase(),
      fee: String(fee),
      source,
      preset,
      ...(isPermit2 && { isPermit2: String(isPermit2) }),
      ...(isMobile && { isMobile: String(isMobile) }),
      ...(feeReceiver && { feeReceiver }),
      ...(permit && { permit })
    };

    console.log('Request body:', requestBody);
    console.log('Request headers:', {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.INCH_API_KEY.slice(0, 5)}...`
    });

    const response = await axios.post(buildUrl, requestBody, {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.INCH_API_KEY}`
      }
    });

    res.json(response.data);

  } catch (error) {
    console.error('Build swap error:', error.response?.data || error.message);
    console.error('Full error object:', error);
    
    // Enhanced error response
    res.status(error.response?.status || 500).json({
      error: 'Failed to build swap order',
      details: error.response?.data || error.message,
      requestInfo: {
        url: error.config?.url,
        method: error.config?.method,
        headers: error.config?.headers,
        data: error.config?.data
      }
    });
  }
});

app.listen(port, () => {
  console.log(`Backend server running on port ${port}`);
}); 