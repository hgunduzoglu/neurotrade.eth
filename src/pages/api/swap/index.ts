import { NextApiRequest, NextApiResponse } from 'next';

const FUSION_API_URL = 'https://api.1inch.dev/fusion-plus';
const API_KEY = process.env.ONEINCH_API_KEY;

async function relayRequest(
  req: NextApiRequest,
  res: NextApiResponse,
  endpoint: string,
  method: string = 'GET'
) {
  try {
    const url = new URL(`${FUSION_API_URL}${endpoint}`);
    
    // Forward query parameters
    const queryString = new URLSearchParams(req.query as Record<string, string>).toString();
    if (queryString) {
      url.search = queryString;
    }

    const headers = {
      'Authorization': `Bearer ${API_KEY}`,
      'Content-Type': 'application/json',
    };

    const options: RequestInit = {
      method,
      headers,
    };

    if (method === 'POST' && req.body) {
      options.body = JSON.stringify(req.body);
    }

    const response = await fetch(url.toString(), options);
    const data = await response.json();

    return res.status(response.status).json(data);
  } catch (error: any) {
    return res.status(500).json({ error: error?.message || 'Unknown error' });
  }
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  // Handle OPTIONS request for CORS
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // Route the request based on the path
  const path = req.query.path as string;
  
  switch (path) {
    case 'quote':
      return relayRequest(req, res, '/quoter/v1.0/quote/receive', 'GET');
    
    case 'quote/build':
      return relayRequest(req, res, '/quoter/v1.0/quote/build', 'POST');
    
    case 'order/create':
      return relayRequest(req, res, '/order/create', 'POST');
    
    case 'order/submit':
      return relayRequest(req, res, '/relayer/v1.0/submit', 'POST');
    
    case 'order/status':
      const orderHash = req.query.hash as string;
      return relayRequest(req, res, `/orders/v1.0/order/status/${orderHash}`);
    
    case 'order/secret-fills':
      const hash = req.query.hash as string;
      return relayRequest(req, res, `/orders/v1.0/secret-fills/${hash}`);
    
    case 'order/reveal-secrets':
      return relayRequest(req, res, '/relayer/v1.0/submit/secret', 'POST');
    
    case 'order/secret/submit':
      return relayRequest(req, res, '/relayer/v1.0/submit/secret', 'POST');
    
    default:
      return res.status(404).json({ error: 'Not found' });
  }
} 