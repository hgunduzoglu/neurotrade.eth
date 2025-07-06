import React, { useEffect, useState } from 'react';
import Head from 'next/head';
import { usePrivy } from '@privy-io/react-auth';
import Sidebar from '../components/Sidebar';
import styles from '../styles/Belongings.module.css';

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

  useEffect(() => {
    const fetchTokensForChain = async (chain: string, displayName: string) => {
      if (!authenticated || !user?.wallet?.address) return;
      
      try {
        setChainTokens(prev => prev.map(ct => 
          ct.chain === chain ? { ...ct, loading: true, error: null } : ct
        ));

        const apiKey = process.env.NEXT_PUBLIC_GRAPH_API_KEY;
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
        
        setChainTokens(prev => prev.map(ct => 
          ct.chain === chain ? {
            ...ct,
            tokens: data.data || [],
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
  }, [authenticated, user?.wallet?.address]);

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

  const renderTokenList = (chainData: ChainTokens) => {
    if (chainData.loading) {
      return <div className={styles.loading}>Loading {chainData.displayName} tokens...</div>;
    }
    
    if (chainData.error) {
      return <div className={styles.error}>{chainData.error}</div>;
    }
    
    if (chainData.tokens.length === 0) {
      return <div className={styles.noTokens}>No tokens found on {chainData.displayName}</div>;
    }

    const chainTotal = calculateTotalValue(chainData.tokens);

    return (
      <>
        <div className={styles.chainHeader}>
          <div className={styles.chainInfo}>
            <img 
              src={CHAIN_LOGOS[chainData.chain as keyof typeof CHAIN_LOGOS]} 
              alt={chainData.displayName}
              width={32}
              height={32}
              className={styles.chainLogo}
            />
            <h2 className={styles.chainTitle}>{chainData.displayName}</h2>
          </div>
          <div className={styles.chainTotal}>
            Total Value: {formatUsdValue(chainTotal)}
          </div>
        </div>
        <div className={styles.tokenList}>
          {chainData.tokens.map((token) => (
            <div key={token.contract} className={styles.tokenItem}>
              <div className={styles.tokenSymbol}>
                {token.contract && (
                  <img 
                    src={CHAIN_LOGOS[token.network_id as keyof typeof CHAIN_LOGOS]} 
                    alt={token.symbol}
                    width={24}
                    height={24}
                    style={{ marginRight: '8px', verticalAlign: 'middle' }}
                  />
                )}
                {token.symbol}
              </div>
              <div className={styles.tokenBalance}>
                {Number(token.amount).toFixed(4)} {token.symbol}
              </div>
              <div className={styles.tokenInfo}>
                <div className={styles.tokenPrice}>
                  Price: {token.value ? `$${Number(token.value).toFixed(4)}` : '-'}
                </div>
                <div className={styles.tokenValue}>
                  Value: {formatUsdValue(token.value)}
                </div>
              </div>
            </div>
          ))}
        </div>
      </>
    );
  };

  const renderAuthenticatedContent = () => {
    const portfolioTotal = calculatePortfolioTotal();
    
    return (
      <div className={styles.authenticatedContainer}>
        <div className={styles.portfolioHeader}>
          <h1>Your Token Holdings</h1>
          <div className={styles.portfolioTotal}>
            Portfolio Total: {formatUsdValue(portfolioTotal)}
          </div>
        </div>
        <div className={styles.chainContainer}>
          {chainTokens.map((chainData) => (
            <div key={chainData.chain} className={styles.chainSection}>
              {renderTokenList(chainData)}
            </div>
          ))}
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
        <title>Your Belongings - NeuroTrade.eth</title>
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