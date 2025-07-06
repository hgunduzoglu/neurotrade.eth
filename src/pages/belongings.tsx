import React, { useEffect, useState } from 'react';
import Head from 'next/head';
import { usePrivy } from '@privy-io/react-auth';
import Sidebar from '../components/Sidebar';
import styles from '../styles/Belongings.module.css';
import {
  TokenPrice,
  NetworkTokenPrices,
  fetchNetworkPrice,
  fetchArbPrice,
  fetchTokenPrice
} from '../utils/priceFeeds';

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

interface CopyStatus {
  [key: string]: boolean;
}

const CHAIN_LOGOS = {
  'mainnet': 'https://assets.coingecko.com/coins/images/279/small/ethereum.png',
  'matic': 'https://assets.coingecko.com/coins/images/4713/small/matic-token-icon.png',
  'bsc': 'https://assets.coingecko.com/coins/images/825/small/bnb-icon2_2x.png',
  'arbitrum-one': 'https://assets.coingecko.com/coins/images/16547/small/photo_2023-03-29_21.47.00.jpeg',
  'optimism': 'https://assets.coingecko.com/coins/images/25244/small/Optimism.png',
  'avalanche': 'https://assets.coingecko.com/coins/images/12559/small/Avalanche_Circle_RedWhite_Trans.png',
  'base': 'https://assets.coingecko.com/coins/images/28241/small/base.png',
  'unichain': 'https://assets.coingecko.com/coins/images/279/small/ethereum.png',
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

const Belongings = () => {
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
  const [copyStatus, setCopyStatus] = useState<CopyStatus>({});
  const [selectedChain, setSelectedChain] = useState<string | null>(null);
  const [networkPrices, setNetworkPrices] = useState<NetworkTokenPrices>({});
  const [tokenPrices, setTokenPrices] = useState<TokenPrice>({});

  // Fetch network prices periodically
  useEffect(() => {
    const fetchAllNetworkPrices = async () => {
      const supportedNetworks = ['mainnet', 'arbitrum-one', 'base', 'matic'];
      
      for (const network of supportedNetworks) {
        const nativePrice = await fetchNetworkPrice(network);
        
        if (nativePrice) {
          if (network === 'arbitrum-one') {
            const arbPrice = await fetchArbPrice(nativePrice);
            setNetworkPrices(prev => ({
              ...prev,
              [network]: {
                nativePrice,
                arbPrice: arbPrice || undefined
              }
            }));
          } else {
            setNetworkPrices(prev => ({
              ...prev,
              [network]: {
                nativePrice
              }
            }));
          }
        }
      }
    };

    fetchAllNetworkPrices();
    const interval = setInterval(fetchAllNetworkPrices, 30000);
    return () => clearInterval(interval);
  }, []);

  const isTokenValid = (token: TokenData): boolean => {
    return token.symbol.length <= 6;
  };

  useEffect(() => {
    const fetchTokensForChain = async (chain: string, displayName: string) => {
      if (!authenticated || !user?.wallet?.address) return;
      
      try {
        setChainTokens(prev => prev.map(ct => 
          ct.chain === chain ? { ...ct, loading: true, error: null } : ct
        ));

        const apiKey = process.env.NEXT_PUBLIC_GRAPH_JWT_TOKEN;
        if (!apiKey) {
          throw new Error('Graph API key is not configured');
        }
        
        const response = await fetch(
          `https://token-api.thegraph.com/balances/evm/${user.wallet.address}?network_id=${chain}&limit=100&page=1`,
          {
            headers: {
              'Accept': 'application/json',
              'Authorization': `Bearer ${apiKey}`
            }
          }
        );

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          console.error(`API Error (${chain}):`, errorData);
          throw new Error(`Failed to fetch ${displayName} token data: ${response.status}`);
        }

        const data = await response.json();
        
        // Filter out invalid tokens
        const validTokens = (data.data || []).filter(isTokenValid);
        
        // Fetch prices for all tokens in parallel
        const tokensWithPrices = await Promise.all(
          validTokens.map(async (token: TokenData) => {
            if (chain === 'mainnet' || chain === 'arbitrum-one' || chain === 'base') {
              const networkPrice = networkPrices[chain]?.nativePrice;
              
              if (networkPrice) {
                if (token.symbol.toLowerCase() === 'eth' || token.symbol.toLowerCase() === 'weth') {
                  const amount = parseFloat(formatTokenAmount(token.amount, token.decimals));
                  return {
                    ...token,
                    value: amount * parseFloat(networkPrice)
                  };
                } else {
                  // Try to get cached price first
                  let tokenPrice = tokenPrices[`${chain}-${token.contract.toLowerCase()}`];
                  
                  // If no cached price, fetch from API
                  if (!tokenPrice) {
                    const price = await fetchTokenPrice(token.contract, chain, networkPrice);
                    if (price !== null) {
                      setTokenPrices(prev => ({
                        ...prev,
                        [`${chain}-${token.contract.toLowerCase()}`]: price
                      }));
                      const amount = parseFloat(formatTokenAmount(token.amount, token.decimals));
                      return {
                        ...token,
                        value: amount * parseFloat(price)
                      };
                    }
                  } else {
                    const amount = parseFloat(formatTokenAmount(token.amount, token.decimals));
                    return {
                      ...token,
                      value: amount * parseFloat(tokenPrice)
                    };
                  }
                }
              }
            }
            return token;
          })
        );
        
        setChainTokens(prev => prev.map(ct => 
          ct.chain === chain ? {
            ...ct,
            tokens: tokensWithPrices,
            loading: false,
            error: null
          } : ct
        ));
      } catch (error) {
        console.error(`Error fetching ${displayName} tokens:`, error);
        setChainTokens(prev => prev.map(ct => 
          ct.chain === chain ? {
            ...ct,
            tokens: [],
            loading: false,
            error: `Failed to fetch your ${displayName} tokens. Please try again later.`
          } : ct
        ));
      }
    };

    if (authenticated && user?.wallet?.address) {
      SUPPORTED_CHAINS.forEach(chain => {
        fetchTokensForChain(chain.id, chain.name);
      });
    }
  }, [authenticated, user?.wallet?.address, networkPrices, tokenPrices]);

  const formatUsdValue = (value?: number) => {
    if (!value) return '-';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(value);
  };

  const calculateTotalValue = (tokens: TokenData[]) => {
    return tokens.reduce((total, token) => total + (token.value || 0), 0);
  };

  const calculatePortfolioTotal = () => {
    return chainTokens.reduce((total, chain) => total + calculateTotalValue(chain.tokens), 0);
  };

  const formatTokenAmount = (amount: string, decimals: number) => {
    try {
      const value = parseFloat(amount);
      if (isNaN(value)) return '0';
      return (value / Math.pow(10, decimals)).toFixed(6);
    } catch (error) {
      console.error('Error formatting token amount:', error);
      return '0';
    }
  };

  const maskAddress = (address: string) => {
    if (!address) return '';
    return `${address.slice(0, 6)}...${address.slice(-4)}`;
  };

  const copyToClipboard = async (contract: string) => {
    try {
      await navigator.clipboard.writeText(contract);
      setCopyStatus(prev => ({ ...prev, [contract]: true }));
      setTimeout(() => {
        setCopyStatus(prev => ({ ...prev, [contract]: false }));
      }, 2000);
    } catch (err) {
      console.error('Failed to copy address:', err);
    }
  };

  const renderTokenCard = (token: TokenData) => {
    const networkPrice = networkPrices[token.network_id]?.nativePrice;
    const arbPrice = networkPrices[token.network_id]?.arbPrice;
    const tokenPrice = tokenPrices[`${token.network_id}-${token.contract.toLowerCase()}`];
    const maticPrice = networkPrices[token.network_id]?.nativePrice;
    // Calculate unit price
    const amount = parseFloat(formatTokenAmount(token.amount, token.decimals));
    const unitPrice = token.value && amount ? (token.value / amount).toFixed(2) : null;

    return (
      <div 
        key={token.contract} 
        className={styles.tokenCard}
        onClick={() => copyToClipboard(token.contract)}
      >
        <div className={styles.tokenHeader}>
          <div className={styles.tokenSymbol}>
            <img 
              src={CHAIN_LOGOS[token.network_id as keyof typeof CHAIN_LOGOS]} 
              alt={token.symbol}
              width={24}
              height={24}
              className={styles.tokenLogo}
            />
            <span className={styles.symbolText}>{token.symbol}</span>
          </div>
          <div className={styles.tokenValue}>
            ${unitPrice || '0.00'}
          </div>
        </div>
        <div className={styles.tokenDetails}>
          <div className={styles.tokenBalance}>
            {formatTokenAmount(token.amount, token.decimals)} {token.symbol}
          </div>
          <div className={styles.priceInfo}>
            {networkPrice && (
              <div className={styles.nativePrice}>
                1 ETH = ${parseFloat(networkPrice).toFixed(2)}
              </div>
            )}
            {token.network_id === 'arbitrum-one' && arbPrice && (
              <div className={styles.nativePrice}>
                1 ARB = ${parseFloat(arbPrice).toFixed(2)}
              </div>
            )}
            {token.network_id === 'matic' && maticPrice && (
              <div className={styles.nativePrice}>
                1 MATIC = ${parseFloat(maticPrice).toFixed(2)}
              </div>
            )}
          </div>
          <div className={styles.contractAddress}>
            {copyStatus[token.contract] ? (
              <span className={styles.copiedText}>Copied!</span>
            ) : (
              <span className={styles.addressText}>{maskAddress(token.contract)}</span>
            )}
          </div>
        </div>
      </div>
    );
  };

  const renderChainSelector = () => (
    <div className={styles.chainSelector}>
      <button 
        className={`${styles.chainButton} ${!selectedChain ? styles.active : ''}`}
        onClick={() => setSelectedChain(null)}
      >
        All Chains
      </button>
      {SUPPORTED_CHAINS.map(chain => (
        <button
          key={chain.id}
          className={`${styles.chainButton} ${selectedChain === chain.id ? styles.active : ''}`}
          onClick={() => setSelectedChain(chain.id)}
        >
          <img 
            src={CHAIN_LOGOS[chain.id as keyof typeof CHAIN_LOGOS]} 
            alt={chain.name}
            width={20}
            height={20}
          />
          {chain.name}
        </button>
      ))}
    </div>
  );

  const renderChainSection = (chainData: ChainTokens) => {
    if (chainData.loading) {
      return <div className={styles.loadingCard}>Loading {chainData.displayName} tokens...</div>;
    }
    
    if (chainData.error) {
      return <div className={styles.errorCard}>{chainData.error}</div>;
    }
    
    if (chainData.tokens.length === 0) {
      return <div className={styles.emptyCard}>No tokens found on {chainData.displayName}</div>;
    }

    return (
      <div className={styles.chainSection}>
        <div className={styles.sectionHeader}>
          <div className={styles.chainInfo}>
            <img 
              src={CHAIN_LOGOS[chainData.chain as keyof typeof CHAIN_LOGOS]} 
              alt={chainData.displayName}
              width={24}
              height={24}
              className={styles.chainLogo}
            />
            <h3 className={styles.chainName}>{chainData.displayName}</h3>
          </div>
          <div className={styles.chainValue}>
            {formatUsdValue(calculateTotalValue(chainData.tokens))}
          </div>
        </div>
        <div className={styles.tokenGrid}>
          {chainData.tokens.map(renderTokenCard)}
        </div>
      </div>
    );
  };

  const renderAuthenticatedContent = () => {
    const portfolioTotal = calculatePortfolioTotal();
    const filteredChains = selectedChain 
      ? chainTokens.filter(chain => chain.chain === selectedChain)
      : chainTokens;
    
    return (
      <div className={styles.authenticatedContainer}>
        <div className={styles.portfolioHeader}>
          <div className={styles.headerLeft}>
            <h1>Portfolio</h1>
            <div className={styles.portfolioStats}>
              <div className={styles.statItem}>
                <span className={styles.statLabel}>Total Value</span>
                <span className={styles.statValue}>{formatUsdValue(portfolioTotal)}</span>
              </div>
              <div className={styles.statItem}>
                <span className={styles.statLabel}>Chains</span>
                <span className={styles.statValue}>{chainTokens.filter(chain => chain.tokens.length > 0).length}</span>
              </div>
              <div className={styles.statItem}>
                <span className={styles.statLabel}>Tokens</span>
                <span className={styles.statValue}>
                  {chainTokens.reduce((total, chain) => total + chain.tokens.length, 0)}
                </span>
              </div>
            </div>
          </div>
        </div>
        {renderChainSelector()}
        <div className={styles.contentGrid}>
          {filteredChains.map(renderChainSection)}
        </div>
      </div>
    );
  };

  const renderUnauthenticatedContent = () => (
    <div className={styles.unauthenticatedContainer}>
      <div className={styles.connectBox}>
        <h2>Welcome to NeuroTrade.eth</h2>
        <p>Connect your wallet to view your token holdings and start trading with natural language!</p>
        <button onClick={login} className={styles.connectButton}>
          Connect Wallet
        </button>
      </div>
    </div>
  );

  return (
    <>
      <Head>
        <title>Portfolio - NeuroTrade.eth</title>
        <meta name="description" content="View your token holdings" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div className={styles.container}>
        <Sidebar />
        <main className={styles.main}>
          {authenticated ? renderAuthenticatedContent() : renderUnauthenticatedContent()}
        </main>
      </div>
    </>
  );
};

export default Belongings; 