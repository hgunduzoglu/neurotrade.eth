export interface TokenPrice {
  [key: string]: string; // token address -> price mapping
}

export interface NetworkTokenPrices {
  [key: string]: {
    nativePrice: string;
    arbPrice?: string;
  };
}

export const SUBGRAPH_ENDPOINTS = {
  'mainnet': 'HMuAwufqZ1YCRmzL2SfHTVkzZovC9VL2UAKhjvRqKiR1',
  'arbitrum-one': 'HyW7A86UEdYVt5b9Lrw8W2F98yKecerHKutZTRbSCX27',
  'base': 'HNCFA9TyBqpo5qpe6QreQABAA1kV8g46mhkCcicu6v2R',
  'matic': 'BvYimJ6vCLkk63oWZy7WB5cVDTVVMugUAF35RAUZpQXE'
};

// ARB token contract address on Arbitrum
export const ARB_TOKEN_ADDRESS = '0x912ce59144191c1204e64559fe8253a0e49e6548';

// Network specific GraphQL queries
export const PRICE_QUERIES = {
  'mainnet': `{
    bundles(first: 1) {
      nativePriceUSD
    }
  }`,
  'arbitrum-one': `{
    bundles(first: 1) {
      ethPriceUSD
    }
    token(id: "${ARB_TOKEN_ADDRESS}") {
      derivedETH
    }
  }`,
  'base': `{
    bundles(first: 1) {
      ethPriceUSD
    }
  }`,
  'matic': `{
    bundles(first: 1) {
      maticPriceUSD
    }
  }`
};

export const fetchNetworkPrice = async (network: string): Promise<string | null> => {
  try {
    const subgraphId = SUBGRAPH_ENDPOINTS[network as keyof typeof SUBGRAPH_ENDPOINTS];
    if (!subgraphId) return null;

    const response = await fetch(`https://gateway.thegraph.com/api/subgraphs/id/${subgraphId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.NEXT_PUBLIC_GRAPH_API_KEY}`
      },
      body: JSON.stringify({
        query: PRICE_QUERIES[network as keyof typeof PRICE_QUERIES]
      })
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch ${network} price`);
    }

    const data = await response.json();
    const priceField = network === 'mainnet' ? 'nativePriceUSD' : 'ethPriceUSD';
    return data.data?.bundles?.[0]?.[priceField] || null;
  } catch (error) {
    console.error(`Error fetching ${network} price:`, error);
    return null;
  }
};

export const fetchArbPrice = async (ethPrice: string): Promise<string | null> => {
  try {
    const response = await fetch(`https://gateway.thegraph.com/api/subgraphs/id/${SUBGRAPH_ENDPOINTS['arbitrum-one']}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.NEXT_PUBLIC_GRAPH_API_KEY}`
      },
      body: JSON.stringify({
        query: `{
          token(id: "${ARB_TOKEN_ADDRESS}") {
            derivedETH
          }
        }`
      })
    });

    if (!response.ok) {
      throw new Error('Failed to fetch ARB price');
    }

    const data = await response.json();
    if (data.data?.token?.derivedETH) {
      const arbPriceInEth = parseFloat(data.data.token.derivedETH);
      const arbPriceInUsd = arbPriceInEth * parseFloat(ethPrice);
      return arbPriceInUsd.toString();
    }
    return null;
  } catch (error) {
    console.error('Error fetching ARB price:', error);
    return null;
  }
};

export const fetchTokenPrice = async (tokenAddress: string, network: string, networkPrice: string): Promise<string | null> => {
  try {
    const subgraphId = SUBGRAPH_ENDPOINTS[network as keyof typeof SUBGRAPH_ENDPOINTS];
    if (!subgraphId) return null;

    const response = await fetch(`https://gateway.thegraph.com/api/subgraphs/id/${subgraphId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.NEXT_PUBLIC_GRAPH_API_KEY}`
      },
      body: JSON.stringify({
        query: `{
          token(id: "${tokenAddress.toLowerCase()}") {
            derivedETH
          }
        }`
      })
    });

    if (!response.ok) {
      throw new Error('Failed to fetch token price');
    }

    const data = await response.json();
    if (data.data?.token?.derivedETH) {
      const priceInEth = parseFloat(data.data.token.derivedETH);
      const priceInUsd = priceInEth * parseFloat(networkPrice);
      return priceInUsd.toString();
    }
    return null;
  } catch (error) {
    console.error('Error fetching token price:', error);
    return null;
  }
}; 