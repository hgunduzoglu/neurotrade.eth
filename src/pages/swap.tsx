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
  chainId?: number; // Add chainId for cross-chain support
}

interface GasCost {
  gasBumpEstimate: number;
  gasPriceEstimate: string;
}

interface PresetPoint {
  delay: number;
  coefficient: number;
}

interface PresetConfig {
  auctionDuration: number;
  startAuctionIn: number;
  initialRateBump: number;
  auctionStartAmount: string;
  startAmount: string;
  auctionEndAmount: string;
  exclusiveResolver: null | string;
  costInDstToken: string;
  points: PresetPoint[];
  allowPartialFills: boolean;
  allowMultipleFills: boolean;
  gasCost: GasCost;
  secretsCount: number;
}

interface FusionQuoteResponse {
  quoteId: string;
  srcTokenAmount: string;
  dstTokenAmount: string;
  presets: {
    fast: PresetConfig;
    medium: PresetConfig;
    slow: PresetConfig;
  };
  recommendedPreset: 'fast' | 'medium' | 'slow';
  prices: {
    usd: {
      srcToken: string;
      dstToken: string;
    };
  };
  volume: {
    usd: {
      srcToken: string;
      dstToken: string;
    };
  };
  priceImpactPercent: number;
}

interface BuildSwapResponse {
  quoteId: string;
  srcChainId: number;
  dstChainId: number;
  srcTokenAddress: string;
  dstTokenAddress: string;
  srcTokenAmount: string;
  dstTokenAmount: string;
  srcUsdValue: string;
  dstUsdValue: string;
  preset: string;
  deadline: number;
  auctionEndTime: number;
  points: Array<{
    delay: number;
    coefficient: number;
  }>;
  resolverContract: string;
  signature: string;
  orderHash: string;
  permitData?: any;
}

// Sepolia test tokens with chain IDs
const TOKENS: Record<string, Token> = {
  ETH: {
    symbol: 'ETH',
    name: 'Ethereum',
    address: '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE',
    decimals: 18,
    chainId: 1 // Ethereum mainnet
  },
  USDT: {
    symbol: 'USDT',
    name: 'Tether USD',
    address: '0xc2132D05D31c914a87C6611C10748AEb04B58e8F',
    decimals: 6,
    chainId: 137 // Polygon
  },
  // Add more tokens as needed
};

function SwapComponent() {
  const { address } = useAccount();
  const [fromToken, setFromToken] = useState<Token>(TOKENS.ETH);
  const [toToken, setToToken] = useState<Token>(TOKENS.USDT);
  const [amount, setAmount] = useState('');
  const [quote, setQuote] = useState<FusionQuoteResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedPreset, setSelectedPreset] = useState<'fast' | 'medium' | 'slow'>('fast');
  const [buildData, setBuildData] = useState<BuildSwapResponse | null>(null);
  const [buildLoading, setBuildLoading] = useState(false);

  useEffect(() => {
    console.log('Current wallet address:', address);
  }, [address]);

  const validateSwap = () => {
    console.log('Validating swap with address:', address);
    
    if (!amount || isNaN(parseFloat(amount)) || parseFloat(amount) <= 0) {
      setError('Please enter a valid amount');
      return false;
    }
    
    if (!fromToken || !toToken) {
      setError('Please select tokens');
      return false;
    }

    if (fromToken.address.toLowerCase() === toToken.address.toLowerCase() && 
        fromToken.chainId === toToken.chainId) {
      setError('Cannot swap a token for itself on the same chain');
      return false;
    }

    if (!address) {
      console.log('Wallet not connected');
      setError('Please connect your wallet');
      return false;
    }

    return true;
  };

  const getQuote = async () => {
    if (!validateSwap()) {
      setQuote(null);
      return;
    }
    
    setLoading(true);
    setError(null);
    try {
      const amountInWei = BigInt(parseFloat(amount) * Math.pow(10, fromToken.decimals)).toString();
      
      // Use our backend API endpoint
      const params = new URLSearchParams({
        srcChain: fromToken.chainId?.toString() || '1',
        dstChain: toToken.chainId?.toString() || '1',
        srcTokenAddress: fromToken.address,
        dstTokenAddress: toToken.address,
        amount: amountInWei,
        walletAddress: address || '',
        enableEstimate: 'true'
      });

      console.log('Requesting quote with params:', Object.fromEntries(params.entries()));
      
      const response = await fetch(`http://localhost:3001/quote?${params}`);
      
      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || `Failed to get quote: ${data.details || 'Unknown error'}`);
      }
      
      const data = await response.json();
      
      if (data.error) {
        throw new Error(data.error);
      }
      
      setQuote(data);
      setSelectedPreset(data.recommendedPreset);
    } catch (error) {
      console.error('Quote error:', error);
      setError(error instanceof Error ? error.message : 'Failed to get quote');
      setQuote(null);
    }
    setLoading(false);
  };

  const formatTokenAmount = (amount: string, decimals: number) => {
    return (Number(amount) / Math.pow(10, decimals)).toFixed(6);
  };

  const getPresetInfo = (preset: PresetConfig) => {
    return {
      duration: `${preset.auctionDuration / 60} minutes`,
      estimatedOutput: formatTokenAmount(preset.startAmount, toToken.decimals),
      gasCost: preset.gasCost.gasPriceEstimate
    };
  };

  const handleBuildSwap = async () => {
    console.log('Building swap with address:', address);
    
    if (!quote || !validateSwap() || !address) {
      console.log('Build swap validation failed:', { quote: !!quote, address: !!address });
      return;
    }

    setBuildLoading(true);
    setError(null);
    try {
      const amountInWei = BigInt(parseFloat(amount) * Math.pow(10, fromToken.decimals)).toString();
      
      const requestBody = {
        srcChain: fromToken.chainId,
        dstChain: toToken.chainId,
        srcTokenAddress: fromToken.address,
        dstTokenAddress: toToken.address,
        amount: amountInWei,
        walletAddress: address,
        preset: selectedPreset,
        source: 'Frontend'
      };

      console.log('Sending build request with body:', requestBody);
      
      // Update the API endpoint to use our backend server
      const response = await fetch('http://localhost:3001/swap/build', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok) {
        const data = await response.json();
        console.error('Build request failed:', data);
        throw new Error(data.error || `Failed to build swap: ${data.details || 'Unknown error'}`);
      }

      const data = await response.json();
      setBuildData(data);
      
      console.log('Build successful:', data);
      
    } catch (error) {
      console.error('Build error:', error);
      setError(error instanceof Error ? error.message : 'Failed to build swap');
    }
    setBuildLoading(false);
  };

  useEffect(() => {
    if (amount) {
      getQuote();
    } else {
      setQuote(null);
      setError(null);
    }
  }, [amount, fromToken, toToken, address]);

  return (
    <div className={styles.container}>
      <div className={styles.swapCard}>
        <h2>Cross-Chain Swap</h2>
        
        {error && (
          <div className={styles.error}>
            {error}
          </div>
        )}
        
        <div className={styles.inputGroup}>
          <label>From ({fromToken.chainId})</label>
          <select
            value={fromToken.symbol}
            onChange={(e) => setFromToken(TOKENS[e.target.value])}
            className={styles.select}
            disabled={loading}
          >
            {Object.values(TOKENS).map((token) => (
              <option key={token.symbol} value={token.symbol}>
                {token.symbol} - {token.name} (Chain {token.chainId})
              </option>
            ))}
          </select>
          <input
            type="number"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            placeholder="Amount"
            className={styles.input}
            disabled={loading}
          />
        </div>

        <div className={styles.inputGroup}>
          <label>To ({toToken.chainId})</label>
          <select
            value={toToken.symbol}
            onChange={(e) => setToToken(TOKENS[e.target.value])}
            className={styles.select}
            disabled={loading}
          >
            {Object.values(TOKENS).map((token) => (
              <option key={token.symbol} value={token.symbol}>
                {token.symbol} - {token.name} (Chain {token.chainId})
              </option>
            ))}
          </select>
        </div>

        {quote && (
          <div className={styles.quoteInfo}>
            <h3>Quote Details</h3>
            <div>Expected Output: {formatTokenAmount(quote.dstTokenAmount, toToken.decimals)} {toToken.symbol}</div>
            <div>Price Impact: {quote.priceImpactPercent.toFixed(2)}%</div>
            
            <div className={styles.presetSelector}>
              <h4>Speed Options</h4>
              {Object.entries(quote.presets).map(([speed, preset]) => {
                const info = getPresetInfo(preset);
                return (
                  <div 
                    key={speed}
                    className={`${styles.preset} ${selectedPreset === speed ? styles.selectedPreset : ''}`}
                    onClick={() => setSelectedPreset(speed as 'fast' | 'medium' | 'slow')}
                  >
                    <div className={styles.presetTitle}>{speed.toUpperCase()}</div>
                    <div>Duration: {info.duration}</div>
                    <div>Output: {info.estimatedOutput} {toToken.symbol}</div>
                    <div>Gas: {info.gasCost} GWEI</div>
                  </div>
                );
              })}
            </div>

            <div className={styles.actionButtons}>
              <button 
                onClick={getQuote} 
                className={styles.quoteButton}
                disabled={!amount || loading || !!error}
              >
                {loading ? 'Loading...' : 'Refresh Quote'}
              </button>

              <button 
                onClick={handleBuildSwap}
                className={styles.swapButton}
                disabled={!quote || buildLoading || !!error}
              >
                {buildLoading ? 'Building...' : 'Swap Now'}
              </button>
            </div>
          </div>
        )}

        {!quote && (
          <button 
            onClick={getQuote} 
            className={styles.quoteButton}
            disabled={!amount || loading || !!error}
          >
            {loading ? 'Loading...' : 'Get Quote'}
          </button>
        )}

        {buildData && (
          <div className={styles.buildInfo}>
            <h3>Swap Order Ready</h3>
            <div>Order Hash: {buildData.orderHash}</div>
            <div>Deadline: {new Date(buildData.deadline * 1000).toLocaleString()}</div>
            <div>Auction End: {new Date(buildData.auctionEndTime * 1000).toLocaleString()}</div>
          </div>
        )}
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