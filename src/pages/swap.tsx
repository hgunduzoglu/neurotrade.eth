import { useState, useEffect } from 'react';
import { useAccount, useChainId } from 'wagmi';
import Image from 'next/image';
import styles from '../styles/Swap.module.css';

interface Token {
    address: string;
    symbol: string;
    decimals: number;
    name: string;
    logoURI?: string;
}

const SwapPage = () => {
    const { address } = useAccount();
    const chainId = useChainId();
    const [fromToken, setFromToken] = useState('');
    const [toToken, setToToken] = useState('');
    const [amount, setAmount] = useState('');
    const [quote, setQuote] = useState(null);
    const [loading, setLoading] = useState(false);
    const [availableTokens, setAvailableTokens] = useState<Token[]>([]);
    const [error, setError] = useState<string>('');
    const [isHydrated, setIsHydrated] = useState(false);

    // Handle hydration
    useEffect(() => {
        setIsHydrated(true);
    }, []);

    useEffect(() => {
        const fetchTokens = async () => {
            try {
                setLoading(true);
                setError('');
                
                // Backend endpoint URL
                const backendUrl = 'http://localhost:3001';
                const response = await fetch(`${backendUrl}/api/tokens/chains?chainIds=${chainId}`);
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const result = await response.json();
                
                // Debug: Log the full API response
                console.log('Backend API Response:', {
                    success: result.success,
                    isArray: Array.isArray(result.data),
                    tokenCount: Array.isArray(result.data) ? result.data.length : 'not array',
                    filteredChains: result.filteredChains,
                    requestedChainId: chainId
                });
                
                if (!result.success) {
                    throw new Error(result.error?.message || 'Failed to fetch tokens');
                }
                
                // Transform backend response to Token array
                const tokens: Token[] = [];
                
                // New API format: result.data is already an array of filtered tokens for the requested chain
                if (!Array.isArray(result.data)) {
                    throw new Error('Invalid token data format received from backend');
                }
                
                result.data.forEach((tokenData: any) => {
                    tokens.push({
                        address: tokenData.address,
                        symbol: tokenData.symbol,
                        decimals: tokenData.decimals,
                        name: tokenData.name,
                        logoURI: tokenData.logoURI || ''
                    });
                });
                
                setAvailableTokens(tokens);
                console.log(`Loaded ${tokens.length} tokens for chain ${chainId}`, tokens.slice(0, 3));
                
            } catch (error: any) {
                console.error('Error fetching tokens:', error);
                const errorMessage = error.message || 'Failed to fetch tokens';
                setError(errorMessage);
                setAvailableTokens([]);
            } finally {
                setLoading(false);
            }
        };

        if (chainId && isHydrated) {
            fetchTokens();
        }
    }, [chainId, isHydrated]);

    const getQuote = async () => {
        try {
            setLoading(true);
            const response = await fetch('/api/swap/quote', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    fromToken,
                    toToken,
                    amount,
                    walletAddress: address,
                }),
            });
            const data = await response.json();
            setQuote(data);
        } catch (error) {
            console.error('Error getting quote:', error);
        } finally {
            setLoading(false);
        }
    };

    const createOrder = async () => {
        try {
            setLoading(true);
            const response = await fetch('/api/swap/order', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    fromToken,
                    toToken,
                    amount,
                    walletAddress: address,
                }),
            });
            const order = await response.json();
            console.log('Order created:', order);
        } catch (error) {
            console.error('Error creating order:', error);
        } finally {
            setLoading(false);
        }
    };

    const TokenOption = ({ token }: { token: Token }) => (
        <div className={styles.tokenOption}>
            {token.logoURI && (
                <Image
                    src={token.logoURI}
                    alt={token.symbol}
                    width={24}
                    height={24}
                    className={styles.tokenLogo}
                />
            )}
            <span className={styles.tokenSymbol}>{token.symbol}</span>
            <span className={styles.tokenName}>{token.name}</span>
        </div>
    );

    return (
        <div className={styles.container}>
            <h1>Swap Tokens</h1>
            
            {/* Connection Status */}
            {isHydrated && (
                <div className={styles.connectionStatus}>
                    {address ? (
                        <p>Connected: {address} (Chain: {chainId})</p>
                    ) : (
                        <p>Please connect your wallet to start swapping</p>
                    )}
                </div>
            )}

            {/* Error Display */}
            {error && (
                <div className={styles.error}>
                    <p>⚠️ {error}</p>
                </div>
            )}

            {/* Loading Indicator */}
            {loading && (
                <div className={styles.loading}>
                    <p>🔄 Loading tokens for chain {chainId}...</p>
                </div>
            )}

            <div className={styles.swapForm}>
                <div className={styles.inputGroup}>
                    <label>From Token: {availableTokens.length > 0 && `(${availableTokens.length} available)`}</label>
                    <select
                        value={fromToken}
                        onChange={(e) => setFromToken(e.target.value)}
                        className={styles.select}
                        disabled={loading || !availableTokens.length || !address || !isHydrated}
                    >
                        <option value="">
                            {!isHydrated
                                ? "Loading..."
                                : loading 
                                ? "Loading tokens..." 
                                : !address 
                                ? "Connect wallet first" 
                                : availableTokens.length === 0 
                                ? "No tokens available for this chain" 
                                : "Select token"
                            }
                        </option>
                        {availableTokens.map((token) => (
                            <option key={token.address} value={token.address}>
                                {token.symbol} - {token.name}
                            </option>
                        ))}
                    </select>
                    {fromToken && (
                        <div className={styles.selectedToken}>
                            <TokenOption token={availableTokens.find(t => t.address === fromToken)!} />
                        </div>
                    )}
                </div>
                <div className={styles.inputGroup}>
                    <label>To Token: {availableTokens.length > 0 && `(${availableTokens.length} available)`}</label>
                    <select
                        value={toToken}
                        onChange={(e) => setToToken(e.target.value)}
                        className={styles.select}
                        disabled={loading || !availableTokens.length || !address || !isHydrated}
                    >
                        <option value="">
                            {!isHydrated
                                ? "Loading..."
                                : loading 
                                ? "Loading tokens..." 
                                : !address 
                                ? "Connect wallet first" 
                                : availableTokens.length === 0 
                                ? "No tokens available for this chain" 
                                : "Select token"
                            }
                        </option>
                        {availableTokens.map((token) => (
                            <option key={token.address} value={token.address}>
                                {token.symbol} - {token.name}
                            </option>
                        ))}
                    </select>
                    {toToken && (
                        <div className={styles.selectedToken}>
                            <TokenOption token={availableTokens.find(t => t.address === toToken)!} />
                        </div>
                    )}
                </div>
                <div className={styles.inputGroup}>
                    <label>Amount:</label>
                    <input
                        type="text"
                        value={amount}
                        onChange={(e) => setAmount(e.target.value)}
                        placeholder="0.0"
                        className={styles.input}
                        disabled={loading}
                    />
                </div>
                <button
                    onClick={getQuote}
                    disabled={loading || !fromToken || !toToken || !amount}
                    className={styles.button}
                >
                    {loading ? 'Loading...' : 'Get Quote'}
                </button>
                {quote && (
                    <>
                        <div className={styles.quoteInfo}>
                            <h3>Quote Information</h3>
                            <pre>{JSON.stringify(quote, null, 2)}</pre>
                        </div>
                        <button
                            onClick={createOrder}
                            disabled={loading}
                            className={styles.button}
                        >
                            {loading ? 'Creating Order...' : 'Create Order'}
                        </button>
                    </>
                )}
            </div>
        </div>
    );
};

export default SwapPage; 