import { useState, useEffect } from 'react';
import { usePrivy } from '@privy-io/react-auth';
import { useRouter } from 'next/router';
import styles from '@/styles/Swap.module.css';
import { WagmiConfig, useAccount } from 'wagmi';
import { QueryClientProvider } from '@tanstack/react-query';
import { config, queryClient } from '@/config/wagmi';

interface Token {
  symbol: string;
  name: string;
  address: string;
  decimals: number;
}

interface QuoteResponse {
  toAmount: string;
  // Add other fields as needed from the 1inch API response
}

// Sepolia test tokens
const TOKENS: Record<string, Token> = {
  ETH: {
    symbol: 'ETH',
    name: 'Ethereum',
    address: '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE',
    decimals: 18
  },
  DAI: {
    symbol: 'DAI',
    name: 'Dai Stablecoin',
    address: '0x68194a729C2450ad26072b3D33ADaCbcef39D574',
    decimals: 18
  },
  USDC: {
    symbol: 'USDC',
    name: 'USD Coin',
    address: '0xda9d4f9b69ac6C22e444eD9aF0CfC043b7a7f53f',
    decimals: 6
  },
  WETH: {
    symbol: 'WETH',
    name: 'Wrapped Ether',
    address: '0x7b79995e5f793A07Bc00c21412e50Ecae098E7f9',
    decimals: 18
  }
};

function SwapComponent() {
  const { address } = useAccount();
  const [fromToken, setFromToken] = useState<Token>(TOKENS.ETH);
  const [toToken, setToToken] = useState<Token>(TOKENS.DAI);
  const [amount, setAmount] = useState('');
  const [quote, setQuote] = useState<QuoteResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const getQuote = async () => {
    if (!amount || !fromToken || !toToken || !address) return;
    
    setLoading(true);
    try {
      const response = await fetch(`https://api.1inch.dev/swap/v5.2/11155111/quote?src=${fromToken.address}&dst=${toToken.address}&amount=${parseFloat(amount) * Math.pow(10, fromToken.decimals)}&from=${address}`, {
        headers: {
          'Authorization': `Bearer ${process.env.NEXT_PUBLIC_1INCH_API_KEY}`
        }
      });
      
      const data = await response.json();
      setQuote(data);
    } catch (error) {
      console.error('Quote error:', error);
    }
    setLoading(false);
  };

  const handleSwap = async () => {
    if (!amount || !fromToken || !toToken || !address) return;
    
    try {
      const response = await fetch(`https://api.1inch.dev/swap/v5.2/11155111/swap?src=${fromToken.address}&dst=${toToken.address}&amount=${parseFloat(amount) * Math.pow(10, fromToken.decimals)}&from=${address}&slippage=1`, {
        headers: {
          'Authorization': `Bearer ${process.env.NEXT_PUBLIC_1INCH_API_KEY}`
        }
      });
      
      const data = await response.json();
      // Here you would typically send this transaction data to the wallet
      console.log('Swap data:', data);
    } catch (error) {
      console.error('Swap error:', error);
    }
  };

  useEffect(() => {
    if (amount) {
      getQuote();
    }
  }, [amount, fromToken, toToken, address]);

  const switchTokens = () => {
    const temp = fromToken;
    setFromToken(toToken);
    setToToken(temp);
  };

  return (
    <div className={styles.container}>
      <div className={styles.swapCard}>
        <h2>Swap Tokens</h2>
        
        <div className={styles.inputGroup}>
          <label>From</label>
          <select
            value={fromToken.symbol}
            onChange={(e) => setFromToken(TOKENS[e.target.value])}
            className={styles.select}
          >
            {Object.values(TOKENS).map((token) => (
              <option key={token.symbol} value={token.symbol}>
                {token.symbol} - {token.name}
              </option>
            ))}
          </select>
          <input
            type="number"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            placeholder="Amount"
            className={styles.input}
          />
        </div>

        <button className={styles.switchButton} onClick={switchTokens}>
          ↓
        </button>

        <div className={styles.inputGroup}>
          <label>To</label>
          <select
            value={toToken.symbol}
            onChange={(e) => setToToken(TOKENS[e.target.value])}
            className={styles.select}
          >
            {Object.values(TOKENS).map((token) => (
              <option key={token.symbol} value={token.symbol}>
                {token.symbol} - {token.name}
              </option>
            ))}
          </select>
          {quote && (
            <div className={styles.quoteInfo}>
              Expected output: {(Number(quote.toAmount) / Math.pow(10, toToken.decimals)).toFixed(6)} {toToken.symbol}
            </div>
          )}
        </div>

        <button 
          onClick={handleSwap} 
          className={styles.swapButton}
          disabled={!amount || loading}
        >
          {loading ? 'Loading...' : 'Swap'}
        </button>
      </div>
    </div>
  );
}

export default function Swap() {
  const router = useRouter();
  const { authenticated } = usePrivy();

  if (!authenticated) {
    typeof window !== 'undefined' && router.push('/');
    return null;
  }

  return (
    <QueryClientProvider client={queryClient}>
      <WagmiConfig config={config}>
        <SwapComponent />
      </WagmiConfig>
    </QueryClientProvider>
  );
} 