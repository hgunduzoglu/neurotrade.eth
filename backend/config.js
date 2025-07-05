require('dotenv').config();

const config = {
  port: process.env.PORT || 3001,
  nodeEnv: process.env.NODE_ENV || 'development',
  frontendUrl: process.env.FRONTEND_URL || 'http://localhost:3000',
  
  // 1inch API Configuration
  oneInch: {
    apiKey: process.env.INCH_API_KEY || 'undefined', // Default from your example
    baseUrl: 'https://api.1inch.dev',
    defaultProvider: '1inch',
    defaultCountry: 'US'
  }
};

module.exports = config; 