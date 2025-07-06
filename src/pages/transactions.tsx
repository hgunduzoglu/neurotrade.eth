import { useEffect, useState } from 'react';
import { usePrivy } from '@privy-io/react-auth';
import { useAccount } from 'wagmi';
import styles from '../styles/Transactions.module.css';
import Sidebar from '../components/Sidebar';
import Image from 'next/image';
import Head from 'next/head';

// Mock data
const MOCK_TRANSACTIONS = [
  {
    transactionHash: '0x123...abc1',
    transactionType: 'buy',
    blockTimestamp: new Date(Date.now() - 3600000).toISOString(), // 1 hour ago
    exchangeName: 'Uniswap',
    exchangeLogo: 'https://assets.coingecko.com/markets/images/535/small/UniSwap.png',
    pairLabel: 'ETH/USDT',
    description: 'Bought Ethereum',
    bought: {
      address: '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',
      amount: '1.5',
      usdPrice: 3500,
      usdAmount: 5250,
      symbol: 'ETH',
      logo: 'https://assets.coingecko.com/coins/images/279/small/ethereum.png',
      name: 'Ethereum',
      tokenType: 'token1'
    },
    sold: {
      address: '0xdac17f958d2ee523a2206206994597c13d831ec7',
      amount: '5250',
      usdPrice: 1,
      usdAmount: 5250,
      symbol: 'USDT',
      logo: 'https://assets.coingecko.com/coins/images/325/small/Tether.png',
      name: 'Tether USD',
      tokenType: 'token0'
    },
    totalValueUsd: 5250
  },
  {
    transactionHash: '0x123...abc2',
    transactionType: 'sell',
    blockTimestamp: new Date(Date.now() - 7200000).toISOString(), // 2 hours ago
    exchangeName: 'Uniswap',
    exchangeLogo: 'https://assets.coingecko.com/markets/images/535/small/UniSwap.png',
    pairLabel: 'BTC/USDT',
    description: 'Sold Bitcoin',
    sold: {
      address: '0x2260fac5e5542a773aa44fbcfedf7c193bc2c599',
      amount: '0.25',
      usdPrice: 65000,
      usdAmount: 16250,
      symbol: 'BTC',
      logo: 'https://assets.coingecko.com/coins/images/1/small/bitcoin.png',
      name: 'Bitcoin',
      tokenType: 'token0'
    },
    bought: {
      address: '0xdac17f958d2ee523a2206206994597c13d831ec7',
      amount: '16250',
      usdPrice: 1,
      usdAmount: 16250,
      symbol: 'USDT',
      logo: 'https://assets.coingecko.com/coins/images/325/small/Tether.png',
      name: 'Tether USD',
      tokenType: 'token1'
    },
    totalValueUsd: 16250
  },
  {
    transactionHash: '0x123...abc3',
    transactionType: 'buy',
    blockTimestamp: new Date(Date.now() - 14400000).toISOString(), // 4 hours ago
    exchangeName: 'SushiSwap',
    exchangeLogo: 'https://assets.coingecko.com/markets/images/568/small/sushiswap.png',
    pairLabel: 'MATIC/USDT',
    description: 'Bought Polygon',
    bought: {
      address: '0x7d1afa7b718fb893db30a3abc0cfc608aacfebb0',
      amount: '1000',
      usdPrice: 0.85,
      usdAmount: 850,
      symbol: 'MATIC',
      logo: 'https://assets.coingecko.com/coins/images/4713/small/matic-token-icon.png',
      name: 'Polygon',
      tokenType: 'token1'
    },
    sold: {
      address: '0xdac17f958d2ee523a2206206994597c13d831ec7',
      amount: '850',
      usdPrice: 1,
      usdAmount: 850,
      symbol: 'USDT',
      logo: 'https://assets.coingecko.com/coins/images/325/small/Tether.png',
      name: 'Tether USD',
      tokenType: 'token0'
    },
    totalValueUsd: 850
  },
  {
    transactionHash: '0x123...abc4',
    transactionType: 'buy',
    blockTimestamp: new Date(Date.now() - 86400000).toISOString(), // 24 hours ago
    exchangeName: 'Uniswap',
    exchangeLogo: 'https://assets.coingecko.com/markets/images/535/small/UniSwap.png',
    pairLabel: 'SOL/USDT',
    description: 'Bought Solana',
    bought: {
      address: '0x7d1afa7b718fb893db30a3abc0cfc608aacfebb0',
      amount: '50',
      usdPrice: 125,
      usdAmount: 6250,
      symbol: 'SOL',
      logo: 'https://assets.coingecko.com/coins/images/4128/small/solana.png',
      name: 'Solana',
      tokenType: 'token1'
    },
    sold: {
      address: '0xdac17f958d2ee523a2206206994597c13d831ec7',
      amount: '6250',
      usdPrice: 1,
      usdAmount: 6250,
      symbol: 'USDT',
      logo: 'https://assets.coingecko.com/coins/images/325/small/Tether.png',
      name: 'Tether USD',
      tokenType: 'token0'
    },
    totalValueUsd: 6250
  },
  {
    transactionHash: '0x123...abc5',
    transactionType: 'sell',
    blockTimestamp: new Date(Date.now() - 172800000).toISOString(), // 48 hours ago
    exchangeName: 'SushiSwap',
    exchangeLogo: 'https://assets.coingecko.com/markets/images/568/small/sushiswap.png',
    pairLabel: 'LINK/USDT',
    description: 'Sold Chainlink',
    sold: {
      address: '0x514910771af9ca656af840dff83e8264ecf986ca',
      amount: '100',
      usdPrice: 18,
      usdAmount: 1800,
      symbol: 'LINK',
      logo: 'https://assets.coingecko.com/coins/images/877/small/chainlink-new-logo.png',
      name: 'Chainlink',
      tokenType: 'token0'
    },
    bought: {
      address: '0xdac17f958d2ee523a2206206994597c13d831ec7',
      amount: '1800',
      usdPrice: 1,
      usdAmount: 1800,
      symbol: 'USDT',
      logo: 'https://assets.coingecko.com/coins/images/325/small/Tether.png',
      name: 'Tether USD',
      tokenType: 'token1'
    },
    totalValueUsd: 1800
  }
];

interface TokenInfo {
  address: string;
  amount: string;
  usdPrice: number;
  usdAmount: number;
  symbol: string;
  logo: string;
  name: string;
  tokenType: string;
}

interface Transaction {
  transactionHash: string;
  transactionType: string;
  blockTimestamp: string;
  exchangeName: string;
  exchangeLogo: string;
  pairLabel: string;
  description: string;
  bought: TokenInfo;
  sold: TokenInfo;
  totalValueUsd: number;
}

export default function Transactions() {
  const { ready, authenticated, login } = usePrivy();
  const { address } = useAccount();
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Simulate loading delay
    const timer = setTimeout(() => {
      setTransactions(MOCK_TRANSACTIONS);
      setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60));
    
    if (diffInHours < 24) {
      return `${diffInHours} hours ago`;
    } else {
      const diffInDays = Math.floor(diffInHours / 24);
      return `${diffInDays} days ago`;
    }
  };

  const formatAmount = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(Math.abs(amount));
  };

  const renderUnauthenticatedContent = () => (
    <div className={styles.unauthenticatedContainer}>
      <div className={styles.connectBox}>
        <h2>Welcome to NeuroTrade.eth</h2>
        <p>Connect your wallet to view your transaction history and start trading with natural language!</p>
        <button onClick={login} className={styles.connectButton}>
          Connect Wallet
        </button>
      </div>
    </div>
  );

  const renderAuthenticatedContent = () => (
    <>
      <h1 className={styles.title}>Transaction History</h1>
      {loading ? (
        <div className={styles.loading}>
          <div className={styles.loadingSpinner}></div>
          <p>Your transactions are loading...</p>
        </div>
      ) : error ? (
        <div className={styles.error}>
          <p>Error: {error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className={styles.retryButton}
          >
            Retry
          </button>
        </div>
      ) : transactions.length === 0 ? (
        <div className={styles.noTransactions}>
          <p>There are no transactions for this address</p>
        </div>
      ) : (
        <div className={styles.transactionList}>
          {transactions.map((tx) => (
            <div key={tx.transactionHash} className={styles.transactionCard}>
              <div className={styles.transactionHeader}>
                <div className={styles.exchangeInfo}>
                  {tx.exchangeLogo && (
                    <Image
                      src={tx.exchangeLogo}
                      alt={tx.exchangeName}
                      width={24}
                      height={24}
                      className={styles.exchangeLogo}
                    />
                  )}
                  <span className={styles.exchangeName}>{tx.exchangeName}</span>
                </div>
                <span className={`${styles.transactionType} ${styles[tx.transactionType]}`}>
                  {tx.transactionType === 'buy' ? 'Buy' : 'Sell'}
                </span>
              </div>
              <div className={styles.transactionDescription}>
                {tx.description}
              </div>
              <div className={styles.transactionDetails}>
                <div className={styles.tokenExchange}>
                  <div className={styles.tokenInfo}>
                    <Image
                      src={tx.sold.logo}
                      alt={tx.sold.symbol}
                      width={20}
                      height={20}
                      className={styles.tokenLogo}
                    />
                    <span className={styles.tokenAmount}>
                      {parseFloat(tx.sold.amount).toLocaleString()} {tx.sold.symbol}
                    </span>
                  </div>
                  <div className={styles.exchangeArrow}>→</div>
                  <div className={styles.tokenInfo}>
                    <Image
                      src={tx.bought.logo}
                      alt={tx.bought.symbol}
                      width={20}
                      height={20}
                      className={styles.tokenLogo}
                    />
                    <span className={styles.tokenAmount}>
                      {parseFloat(tx.bought.amount).toLocaleString()} {tx.bought.symbol}
                    </span>
                  </div>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Transaction Value:</span>
                  <span className={styles.value}>{formatAmount(tx.totalValueUsd)}</span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Time:</span>
                  <span>{formatTimestamp(tx.blockTimestamp)}</span>
                </div>
              </div>
              <a
                href={`https://etherscan.io/tx/${tx.transactionHash}`}
                target="_blank"
                rel="noopener noreferrer"
                className={styles.viewMore}
              >
                View on Etherscan
              </a>
            </div>
          ))}
        </div>
      )}
    </>
  );

  return (
    <div className={styles.container}>
      <Head>
        <title>Transaction History - NeuroTrade.eth</title>
        <meta name="description" content="View your transaction history" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>
      <Sidebar />
      <main className={styles.main}>
        {authenticated ? renderAuthenticatedContent() : renderUnauthenticatedContent()}
      </main>
    </div>
  );
} 