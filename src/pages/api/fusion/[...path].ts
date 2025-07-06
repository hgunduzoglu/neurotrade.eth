import { NextApiRequest, NextApiResponse } from 'next';

const FUSION_API_URL = 'https://api.1inch.dev/fusion-plus';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
    try {
        const { path } = req.query;
        const apiPath = Array.isArray(path) ? path.join('/') : path;
        
        // Construct the full URL including query parameters
        const queryString = new URLSearchParams(req.query as Record<string, string>);
        queryString.delete('path'); // Remove the path parameter from query string
        
        const url = `${FUSION_API_URL}/${apiPath}${queryString.toString() ? `?${queryString.toString()}` : ''}`;

        const headers = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${process.env.ONEINCH_API_KEY}`,
        };

        const response = await fetch(url, {
            method: req.method,
            headers,
            body: req.method !== 'GET' ? JSON.stringify(req.body) : undefined,
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Failed to fetch from 1inch API');
        }

        res.status(response.status).json(data);
    } catch (error: any) {
        console.error('Proxy error:', error);
        res.status(500).json({ error: error.message || 'Internal server error' });
    }
} 