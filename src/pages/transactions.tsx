import { useEffect, useState } from 'react';
import { usePrivy } from '@privy-io/react-auth';
import { useAccount } from 'wagmi';
import styles from '../styles/Transactions.module.css';
import Sidebar from '../components/Sidebar';
import Image from 'next/image';
import Head from 'next/head';

interface ApiTransaction {
  block_num: number;
  datetime: string;
  timestamp: number;
  transaction_id: string;
  contract: string;
  from: string;
  to: string;
  decimals: number;
  symbol: string;
  value: number;
}

interface ApiResponse {
  data: ApiTransaction[];
  statistics: {
    bytes_read: number;
    rows_read: number;
    elapsed: number;
  };
  pagination: {
    previous_page: number;
    current_page: number;
    next_page: number;
    total_pages: number;
  };
  results: number;
  total_results: number;
  request_time: string;
  duration_ms: number;
}

interface Transaction {
  transactionHash: string;
  blockNumber: number;
  timestamp: number;
  datetime: string;
  from: string;
  to: string;
  symbol: string;
  value: number;
  decimals: number;
}

export default function Transactions() {
  const { ready, authenticated, login } = usePrivy();
  const { address } = useAccount();
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTransactions = async (walletAddress: string) => {
    try {
      const response = await fetch(
        `https://token-api.thegraph.com/transfers/evm?network_id=mainnet&from=${walletAddress}&orderBy=timestamp&orderDirection=desc`,
        {
          headers: {
            'Authorization': 'Bearer eyJhbGciOiJLTVNFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3ODc3NjExODksImp0aSI6Ijk1ZmMyMjg0LTQzNDYtNDVmOC05OTgwLTgxZWQxNWE3MmE1NCIsImlhdCI6MTc1MTc2MTE4OSwiaXNzIjoiZGZ1c2UuaW8iLCJzdWIiOiIwbWF0YWIxMTgzMmQwZDhjYmQ3NWIiLCJ2IjoxLCJha2kiOiJiY2RkYjNiYjBmNzY1Y2Q1OTdiOGFkMGZhYTZlMGZlNDMzNzY4Y2M5MjZjNDRmZjUxODY1YjFkOTg5YTgyODA1IiwidWlkIjoiMG1hdGFiMTE4MzJkMGQ4Y2JkNzViIn0.4EV1at8CDk_Dq5IDnztQblRZIE9khs7bBtzWQzD0Seqg5sfIfQH5UlN1Gn3fO30kDpeygh0hP56IbUHJZmLB_Q'
          }
        }
      );

      if (!response.ok) {
        throw new Error('Failed to fetch transactions');
      }

      const data: ApiResponse = await response.json();
      
      const formattedTransactions: Transaction[] = data.data.map(tx => ({
        transactionHash: tx.transaction_id,
        blockNumber: tx.block_num,
        timestamp: tx.timestamp,
        datetime: tx.datetime,
        from: tx.from,
        to: tx.to,
        symbol: tx.symbol,
        value: tx.value,
        decimals: tx.decimals
      }));

      setTransactions(formattedTransactions);
      setLoading(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred while fetching transactions');
      setLoading(false);
    }
  };

  useEffect(() => {
    if (authenticated && address) {
      fetchTransactions(address);
    }
  }, [authenticated, address]);

  const formatTimestamp = (timestamp: number) => {
    const date = new Date(timestamp * 1000);
    const now = new Date();
    const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60));
    
    if (diffInHours < 24) {
      return `${diffInHours} hours ago`;
    } else {
      const diffInDays = Math.floor(diffInHours / 24);
      return `${diffInDays} days ago`;
    }
  };

  const formatAmount = (value: number, decimals: number) => {
    const formattedValue = value / Math.pow(10, decimals);
    return formattedValue.toLocaleString(undefined, {
      minimumFractionDigits: 4,
      maximumFractionDigits: 4,
      useGrouping: true
    });
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
            onClick={() => {
              setLoading(true);
              setError(null);
              if (address) fetchTransactions(address);
            }} 
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
                <div className={styles.transactionType}>
                  {tx.symbol} Transfer
                </div>
                <span className={styles.timestamp}>
                  {formatTimestamp(tx.timestamp)}
                </span>
              </div>
              <div className={styles.transactionDetails}>
                <div className={styles.amountDetail}>
                  <span className={styles.label}>Amount:</span>
                  <div className={styles.amountValue}>
                    <span className={styles.tokenAmount}>
                      {tx.value.toFixed(6)}
                    </span>
                    <span className={styles.tokenSymbol}>{tx.symbol}</span>
                  </div>
                </div>
                <div className={styles.addressDetail}>
                  <span className={styles.label}>To:</span>
                  <span className={styles.value} title={tx.to}>
                    {tx.to.slice(0, 6)}...{tx.to.slice(-4)}
                  </span>
                </div>
                <div className={styles.detail}>
                  <span className={styles.label}>Block:</span>
                  <span className={styles.value}>{tx.blockNumber}</span>
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