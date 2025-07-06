import { Hono } from "hono";

interface Env {
  ONEINCH_API_KEY: string;
}

const app = new Hono<{ Bindings: Env }>();

const FUSION_API_URL = 'https://api.1inch.dev/fusion-plus';

/**
 * A generic function to relay requests to the 1inch Fusion+ API.
 * It forwards headers, body, and query parameters.
 */
const relayRequest = async (c: any, endpoint: string, method: string = 'GET') => {
  const url = new URL(`${FUSION_API_URL}${endpoint}`);

  const incomingUrl = new URL(c.req.url);
  url.search = incomingUrl.search;

  const headers = {
    'Authorization': `Bearer ${c.env.ONEINCH_API_KEY}`,
    'Content-Type': 'application/json'
  };

  const options: RequestInit = {
    method,
    headers,
  };

  if (method === 'POST') {
    const body = await c.req.json();
    options.body = JSON.stringify(body);
  }

  const response = await fetch(url.toString(), options);

  return new Response(response.body, {
    headers: response.headers,
    status: response.status,
  });
};

app.get("/api/", (c) => c.json({ name: "Cloudflare" }));

/**
 * Proxies the get quote request to the 1inch Fusion+ API.
 * Forwards all query parameters from the client.
 * e.g. /api/quote?srcChain=137&srcTokenAddress=...
 */
app.get('/api/quote', (c) => {
  return relayRequest(c, '/quoter/v1.0/quote/receive', 'GET');
});

app.post('/api/quote/build', (c) => {
  return relayRequest(c, '/quoter/v1.0/quote/build', 'POST');
});

/**
 * Proxies the create order request to the 1inch Fusion+ API.
 */
app.post('/api/order/create', (c) => {
  return relayRequest(c, '/order/create', 'POST');
});

/**
 * Proxies the submit order request to the 1inch Fusion+ API.
 */
app.post('/api/order/submit', (c) => {
  return relayRequest(c, '/relayer/v1.0/submit', 'POST');
});

/**
 * Proxies the get order status request to the 1inch Fusion+ API.
 * e.g. /api/order/status/0x123...
 */
app.get('/api/order/status/:hash', (c) => {
  const orderHash = c.req.param('hash');
  return relayRequest(c, `/orders/v1.0/order/status/${orderHash}`);
});

/**
 * Proxies the get ready-to-accept secret fills request to the 1inch Fusion+ API.
 * e.g. /api/order/secret-fills/0x123...
 */
app.get('/api/order/secret-fills/:hash', (c) => {
  const orderHash = c.req.param('hash');
  return relayRequest(c, `/orders/v1.0/secret-fills/${orderHash}`);
});

app.post('/api/order/reveal-secrets', (c) => {
  return relayRequest(c, '/relayer/v1.0/submit/secret', 'POST');
});

/**
 * Proxies the submit secret request to the 1inch Fusion+ API.
 */
app.post('/api/order/secret/submit', (c) => {
  return relayRequest(c, '/relayer/v1.0/submit/secret', 'POST');
});


export default app;
