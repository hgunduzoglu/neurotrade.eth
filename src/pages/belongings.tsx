import React, { useEffect, useState } from 'react';
import Head from 'next/head';
import { usePrivy } from '@privy-io/react-auth';
import Sidebar from '../components/Sidebar';
import styles from '../styles/Belongings.module.css';

interface TokenData {
  token_address: string;
  name: string;
  symbol: string;
  logo?: string;
  decimals: number;
  balance: string;
  balance_formatted: string;
  usd_price?: string;
  usd_value?: number;
}

const Belongings = () => {
  const { user, authenticated, login } = usePrivy();
  const [tokens, setTokens] = useState<TokenData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTokens = async () => {
      if (!authenticated || !user?.wallet?.address) return;
      
      try {
        setLoading(true);
        setError(null);
        
        const response = await fetch(
          `https://deep-index.moralis.io/api/v2.2/wallets/${user.wallet.address}/tokens?chain=eth&exclude_spam=true&exclude_unverified_contracts=true`,
          {
            headers: {
              'accept': 'application/json',
              'X-API-Key': process.env.MORALIS_API_KEY || ''
            }
          }
        );

        if (!response.ok) {
          throw new Error('Failed to fetch token data');
        }

        const data = await response.json();
        setTokens(data.result || []);
      } catch (error) {
        console.error('Error fetching tokens:', error);
        setError('Failed to fetch your tokens. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchTokens();
  }, [authenticated, user?.wallet?.address]);

  const formatUsdValue = (value?: number) => {
    if (!value) return '-';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(value);
  };

  const renderAuthenticatedContent = () => (
    <>
      <h1>Your Token Holdings</h1>
      {loading ? (
        <div className={styles.loading}>Loading your tokens...</div>
      ) : error ? (
        <div className={styles.connectPrompt}>{error}</div>
      ) : tokens.length === 0 ? (
        <div className={styles.noTokens}>No tokens found in your wallet</div>
      ) : (
        <div className={styles.tokenList}>
          {tokens.map((token) => (
            <div key={token.token_address} className={styles.tokenItem}>
              <div className={styles.tokenSymbol}>
                {token.logo && (
                  <img 
                    src={token.logo} 
                    alt={token.symbol}
                    width={24}
                    height={24}
                    style={{ marginRight: '8px', verticalAlign: 'middle' }}
                  />
                )}
                {token.symbol}
              </div>
              <div className={styles.tokenBalance}>
                {token.balance_formatted} {token.symbol}
              </div>
              <div className={styles.tokenInfo}>
                <div className={styles.tokenPrice}>
                  Price: {token.usd_price ? `$${token.usd_price}` : '-'}
                </div>
                <div className={styles.tokenValue}>
                  Value: {formatUsdValue(token.usd_value)}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </>
  );

  const renderUnauthenticatedContent = () => (
    <div className={styles.unauthenticatedContainer}>
      <div className={styles.connectBox}>
        <h2>Welcome to NeuroTrade.eth</h2>
        <p>Connect your wallet to view your token holdings and start trading</p>
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