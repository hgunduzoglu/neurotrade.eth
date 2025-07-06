import { NextApiRequest, NextApiResponse } from 'next';

const WORKER_URL = 'http://localhost:8787';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    const { proxy } = req.query;
    const path = Array.isArray(proxy) ? proxy.join('/') : proxy;
    
    const url = `${WORKER_URL}/${path}${req.url?.includes('?') ? req.url.substring(req.url.indexOf('?')) : ''}`;
    
    const response = await fetch(url, {
      method: req.method,
      headers: {
        'Content-Type': 'application/json',
      },
      body: req.method !== 'GET' ? JSON.stringify(req.body) : undefined,
    });

    const data = await response.json();
    res.status(response.status).json(data);
  } catch (error: any) {
    res.status(500).json({ error: error?.message || 'Internal server error' });
  }
} 