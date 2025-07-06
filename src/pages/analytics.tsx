import React, { useEffect, useState, useCallback } from 'react';
import Head from 'next/head';
import { useAccount } from 'wagmi';
import { usePrivy } from '@privy-io/react-auth';
import { Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
} from 'chart.js';
import styles from '../styles/Analytics.module.css';
import Sidebar from '../components/Sidebar';

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
);

interface TokenData {
  block_num: number;
  datetime: string;
  contract: string;
  amount: string;
  value: number;
  decimals: number;
  symbol: string;
  network_id: string;
}

interface ChainTokens {
  chain: string;
  displayName: string;
  tokens: TokenData[];
  loading: boolean;
  error: string | null;
}

interface ChartDataset {
  data: number[];
  backgroundColor: string[];
}

interface CustomChartData {
  labels: string[];
  datasets: ChartDataset[];
}

const CHAIN_COLORS = {
  'mainnet': '#627EEA',
  'matic': '#8247E5',
  'bsc': '#F3BA2F',
  'arbitrum-one': '#28A0F0',
  'optimism': '#FF0420',
  'avalanche': '#E84142',
  'base': '#0052FF',
  'unichain': '#FF007A'
};

const SUPPORTED_CHAINS = [
  { id: 'mainnet', name: 'Ethereum' },
  { id: 'matic', name: 'Polygon' },
  { id: 'bsc', name: 'BNB Chain' },
  { id: 'arbitrum-one', name: 'Arbitrum' },
  { id: 'optimism', name: 'Optimism' },
  { id: 'avalanche', name: 'Avalanche' },
  { id: 'base', name: 'Base' },
  { id: 'unichain', name: 'UniChain' },
];

const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes in milliseconds

const Analytics = () => {
  const { user, authenticated, login } = usePrivy();
  const [chainTokens, setChainTokens] = useState<ChainTokens[]>(
    SUPPORTED_CHAINS.map(chain => ({
      chain: chain.id,
      displayName: chain.name,
      tokens: [],
      loading: true,
      error: null
    }))
  );
  const [tokenData, setTokenData] = useState<CustomChartData>({
    labels: [],
    datasets: [{
      data: [],
      backgroundColor: [],
    }],
  });
  const [networkData, setNetworkData] = useState<CustomChartData>({
    labels: [],
    datasets: [{
      data: [],
      backgroundColor: [],
    }],
  });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const updateChartData = useCallback((tokens: ChainTokens[]) => {
    // Token Distribution Chart
    const tokenValues: { [key: string]: number } = {};
    const tokenColors: { [key: string]: string } = {};

    tokens.forEach(chain => {
      chain.tokens.forEach(token => {
        if (token.value && token.value > 0) {
          const key = token.symbol;
          tokenValues[key] = (tokenValues[key] || 0) + token.value;
          if (!tokenColors[key]) {
            tokenColors[key] = `#${Math.floor(Math.random()*16777215).toString(16).padStart(6, '0')}`;
          }
        }
      });
    });

    const sortedTokens = Object.entries(tokenValues)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 10);

    setTokenData({
      labels: sortedTokens.map(([symbol]) => symbol),
      datasets: [{
        data: sortedTokens.map(([, value]) => value),
        backgroundColor: sortedTokens.map(([symbol]) => tokenColors[symbol]),
      }],
    });

    // Network Distribution Chart
    const networkValues = tokens.reduce((acc, chain) => {
      const chainTotal = chain.tokens.reduce((sum, token) => sum + (token.value || 0), 0);
      if (chainTotal > 0) {
        acc[chain.displayName] = chainTotal;
      }
      return acc;
    }, {} as { [key: string]: number });

    const sortedNetworks = Object.entries(networkValues)
      .sort(([,a], [,b]) => b - a);

    setNetworkData({
      labels: sortedNetworks.map(([name]) => name),
      datasets: [{
        data: sortedNetworks.map(([, value]) => value),
        backgroundColor: sortedNetworks.map(([name]) => {
          const chain = SUPPORTED_CHAINS.find(c => c.name === name);
          return chain ? CHAIN_COLORS[chain.id as keyof typeof CHAIN_COLORS] : '#808080';
        }),
      }],
    });
  }, []);

  const fetchAllChainData = useCallback(async (address: string) => {
    try {
      const apiKey = process.env.NEXT_PUBLIC_GRAPH_API_KEY;
      if (!apiKey) {
        throw new Error('Graph API key is not configured');
      }

      const results = await Promise.all(
        SUPPORTED_CHAINS.map(async chain => {
          try {
            const response = await fetch(
              `https://token-api.thegraph.com/balances/evm/${address}?network_id=${chain.id}&limit=100&page=1`,
              {
                headers: {
                  'Accept': 'application/json',
                  'Authorization': `Bearer ${apiKey}`
                }
              }
            );

            if (!response.ok) {
              const errorData = await response.json().catch(() => ({}));
              console.error(`API Error (${chain.id}):`, errorData);
              throw new Error(`Failed to fetch ${chain.name} token data: ${response.status}`);
            }

            const data = await response.json();
            return {
              chain: chain.id,
              displayName: chain.name,
              tokens: data.data || [],
              loading: false,
              error: null
            };
          } catch (error) {
            console.error(`Error fetching ${chain.name} tokens:`, error);
            return {
              chain: chain.id,
              displayName: chain.name,
              tokens: [],
              loading: false,
              error: `Failed to fetch ${chain.name} tokens`
            };
          }
        })
      );

      return results;
    } catch (error) {
      console.error('Error fetching chain data:', error);
      throw error;
    }
  }, []);

  useEffect(() => {
    const loadData = async () => {
      if (!authenticated || !user?.wallet?.address) {
        setIsLoading(false);
        return;
      }

      const address = user.wallet.address;
      
      // Check cache first
      const cachedData = localStorage.getItem(`analytics_${address}`);
      if (cachedData) {
        try {
          const { data, timestamp } = JSON.parse(cachedData);
          if (Date.now() - timestamp < CACHE_DURATION) {
            setChainTokens(data);
            updateChartData(data);
            setIsLoading(false);
            return;
          }
          localStorage.removeItem(`analytics_${address}`);
        } catch (error) {
          console.error('Error parsing cached data:', error);
          localStorage.removeItem(`analytics_${address}`);
        }
      }

      // Fetch fresh data
      try {
        setIsLoading(true);
        setError(null);
        
        const data = await fetchAllChainData(address);
        setChainTokens(data);
        updateChartData(data);

        // Cache the new data
        localStorage.setItem(`analytics_${address}`, JSON.stringify({
          data,
          timestamp: Date.now()
        }));
      } catch (error) {
        console.error('Error loading data:', error);
        setError('Failed to load portfolio data. Please try again later.');
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, [authenticated, user?.wallet?.address, updateChartData, fetchAllChainData]);

  const formatUsdValue = (value?: number) => {
    if (!value) return '-';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(value);
  };

  const calculatePortfolioTotal = () => {
    return chainTokens.reduce((total, chain) => 
      total + chain.tokens.reduce((chainTotal, token) => 
        chainTotal + (token.value || 0), 0), 0);
  };

  const renderCharts = () => {
    if (isLoading) {
      return <div className={styles.loading}>Loading portfolio data...</div>;
    }

    if (error) {
      return <div className={styles.error}>{error}</div>;
    }

    const portfolioTotal = calculatePortfolioTotal();

    return (
      <div className={styles.authenticatedContainer}>
        <div className={styles.portfolioHeader}>
          <h1 className={styles.title}>Portfolio Analytics</h1>
          <div className={styles.portfolioTotal}>
            Portfolio Total: {formatUsdValue(portfolioTotal)}
          </div>
        </div>
        <div className={styles.chartsContainer}>
          <div className={styles.chartBox}>
            <h2>Top 10 Token Distribution</h2>
            <div className={styles.chart}>
              <Pie 
                data={tokenData} 
                options={{ 
                  responsive: true,
                  plugins: {
                    legend: {
                      position: 'bottom',
                      labels: {
                        color: 'white',
                        font: { size: 12 }
                      }
                    },
                    tooltip: {
                      callbacks: {
                        label: (context) => {
                          const value = context.raw as number;
                          const percentage = ((value / portfolioTotal) * 100).toFixed(1);
                          return `${context.label}: ${formatUsdValue(value)} (${percentage}%)`;
                        }
                      },
                      backgroundColor: 'rgba(0, 0, 0, 0.8)',
                      titleColor: '#00ffff',
                      bodyColor: 'white',
                      borderColor: 'rgba(255, 255, 255, 0.1)',
                      borderWidth: 1
                    }
                  }
                }} 
              />
            </div>
          </div>
          <div className={styles.chartBox}>
            <h2>Network Distribution</h2>
            <div className={styles.chart}>
              <Pie 
                data={networkData} 
                options={{ 
                  responsive: true,
                  plugins: {
                    legend: {
                      position: 'bottom',
                      labels: {
                        color: 'white',
                        font: { size: 12 }
                      }
                    },
                    tooltip: {
                      callbacks: {
                        label: (context) => {
                          const value = context.raw as number;
                          const percentage = ((value / portfolioTotal) * 100).toFixed(1);
                          return `${context.label}: ${formatUsdValue(value)} (${percentage}%)`;
                        }
                      },
                      backgroundColor: 'rgba(0, 0, 0, 0.8)',
                      titleColor: '#00ffff',
                      bodyColor: 'white',
                      borderColor: 'rgba(255, 255, 255, 0.1)',
                      borderWidth: 1
                    }
                  }
                }} 
              />
            </div>
          </div>
        </div>
      </div>
    );
  };

  const renderUnauthenticatedContent = () => (
    <div className={styles.unauthenticatedContainer}>
      <div className={styles.connectBox}>
        <h2>Welcome to NeuroTrade.eth</h2>
        <p>Connect your wallet to view your portfolio analytics and start trading with natural language!</p>
        <button onClick={login} className={styles.connectButton}>
          Connect Wallet
        </button>
      </div>
    </div>
  );

  return (
    <>
      <Head>
        <title>Portfolio Analytics - NeuroTrade.eth</title>
        <meta name="description" content="View your portfolio analytics" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div className={styles.container}>
        <Sidebar />
        <main className={styles.main}>
          {authenticated ? renderCharts() : renderUnauthenticatedContent()}
        </main>
      </div>
    </>
  );
};

export default Analytics; 