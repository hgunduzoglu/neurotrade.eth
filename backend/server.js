const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const config = require('./config');

// Import routes
const tokensRoutes = require('./routes/tokens');

const app = express();

// Middleware
app.use(helmet()); // Security headers
app.use(express.json()); // Parse JSON bodies
app.use(express.urlencoded({ extended: true })); // Parse URL-encoded bodies

// CORS configuration
const corsOptions = {
  origin: [
    config.frontendUrl,
    'http://localhost:3000',
    'http://127.0.0.1:3000'
  ],
  credentials: true,
  optionsSuccessStatus: 200,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With']
};

app.use(cors(corsOptions));

// Request logging middleware
app.use((req, res, next) => {
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] ${req.method} ${req.url}`);
  if (Object.keys(req.query).length > 0) {
    console.log('Query params:', req.query);
  }
  next();
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'OK',
    message: 'NeuroTrade Backend API is running',
    timestamp: new Date().toISOString(),
    version: '1.0.0'
  });
});

// API routes
app.use('/api/tokens', tokensRoutes);

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    message: 'NeuroTrade Backend API',
    version: '1.0.0',
    endpoints: [
      {
        path: '/health',
        method: 'GET',
        description: 'Health check endpoint'
      },
      {
        path: '/api/tokens',
        method: 'GET',
        description: 'Fetch all available tokens from 1inch',
        parameters: ['provider (optional)', 'country (optional)']
      },
      {
        path: '/api/tokens/chains',
        method: 'GET',
        description: 'Fetch tokens for specific chain IDs',
        parameters: ['chainIds (comma-separated)', 'provider (optional)', 'country (optional)']
      }
    ],
    timestamp: new Date().toISOString()
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({
    success: false,
    message: 'Endpoint not found',
    path: req.originalUrl,
    timestamp: new Date().toISOString()
  });
});

// Global error handler
app.use((error, req, res, next) => {
  console.error('Global error handler:', error);
  res.status(500).json({
    success: false,
    message: 'Internal server error',
    error: config.nodeEnv === 'development' ? error.message : 'Something went wrong',
    timestamp: new Date().toISOString()
  });
});

// Start server
const PORT = config.port;
app.listen(PORT, () => {
  console.log(`
🚀 NeuroTrade Backend API Server Started
📍 Server running on: http://localhost:${PORT}
🌍 Environment: ${config.nodeEnv}
🔗 Frontend URL: ${config.frontendUrl}
📚 API Documentation: http://localhost:${PORT}

Available endpoints:
• GET  /health                - Health check
• GET  /api/tokens           - Get all tokens
• GET  /api/tokens/chains    - Get tokens by chain IDs

Example requests:
• GET  /api/tokens
• GET  /api/tokens?provider=1inch&country=US
• GET  /api/tokens/chains?chainIds=1,137,56
  `);
});

module.exports = app; 