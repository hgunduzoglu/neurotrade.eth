import { useState, useEffect } from 'react';
import { useAccount, useChainId, useConnect } from 'wagmi';
import { ethers } from 'ethers';
import Image from 'next/image';
import styles from '../styles/Swap.module.css';
import { SUPPORTED_CHAINS, SWAP_PRESETS, SwapPreset } from '../config/chains';
import { SwapService, Quote, BuildQuoteResponse, OrderStatus } from '../services/swapService';
import Sidebar from '../components/Sidebar';
import { tokens } from '../config/tokens';
import { Token } from '../types/swap';

const SwapPage = () => {
    const { address } = useAccount();
    const chainId = useChainId();
    const { connectAsync } = useConnect();
    
    const [fromToken, setFromToken] = useState('');
    const [toToken, setToToken] = useState('');
    const [amount, setAmount] = useState('');
    const [quote, setQuote] = useState<Quote | null>(null);
    const [builtQuote, setBuiltQuote] = useState<BuildQuoteResponse | null>(null);
    const [loading, setLoading] = useState(false);
    const [availableTokens, setAvailableTokens] = useState<Token[]>([]);
    const [error, setError] = useState<string>('');
    const [isHydrated, setIsHydrated] = useState(false);
    const [srcChain, setSrcChain] = useState(SUPPORTED_CHAINS[0]);
    const [dstChain, setDstChain] = useState(SUPPORTED_CHAINS[1]);
    const [preset, setPreset] = useState<SwapPreset>('fast');
    const [allowance, setAllowance] = useState<string | null>(null);
    const [orderHash, setOrderHash] = useState<string | null>(null);
    const [orderStatus, setOrderStatus] = useState<OrderStatus | null>(null);
    const [secrets, setSecrets] = useState<string[]>([]);

    // Handle hydration
    useEffect(() => {
        setIsHydrated(true);
    }, []);

    useEffect(() => {
        if (srcChain && isHydrated) {
            const chainTokens = tokens[srcChain.id] || [];
            setAvailableTokens(chainTokens);
            setError('');
        }
    }, [srcChain, isHydrated]);

    const handleNetworkSwitch = async () => {
        try {
            if (!window.ethereum) {
                throw new Error('MetaMask is not installed');
            }

            await window.ethereum.request({
                method: 'wallet_switchEthereumChain',
                params: [{ chainId: `0x${srcChain.id.toString(16)}` }],
            });
        } catch (error: any) {
            if (error.code === 4902) {
                try {
                    await window.ethereum.request({
                        method: 'wallet_addEthereumChain',
                        params: [
                            {
                                chainId: `0x${srcChain.id.toString(16)}`,
                                chainName: srcChain.name,
                                rpcUrls: [srcChain.rpc],
                            },
                        ],
                    });
                } catch (addError) {
                    console.error('Failed to add network:', addError);
                    setError('Failed to add network. Please try manually.');
                }
            } else {
                console.error('Failed to switch network:', error);
                setError('Failed to switch network. Please try manually.');
            }
        }
    };

    const handleGetQuote = async () => {
        if (!address || !fromToken || !toToken || !amount) {
            setError('Please fill in all fields');
            return;
        }

        try {
            setLoading(true);
            setError('');

            const amountWei = ethers.parseUnits(
                amount,
                availableTokens.find(t => t.address === fromToken)?.decimals || 18
            ).toString();

            const quoteResult = await SwapService.getQuote({
                srcChain: srcChain.id,
                srcTokenAddress: fromToken,
                dstChain: dstChain.id,
                dstTokenAddress: toToken,
                amount: amountWei,
                walletAddress: address,
                preset
            });

            setQuote(quoteResult);
        } catch (error: any) {
            console.error('Error getting quote:', error);
            setError(error.message || 'Failed to get quote');
        } finally {
            setLoading(false);
        }
    };

    const handleBuildQuote = async () => {
        if (!quote || !address) return;

        try {
            setLoading(true);
            setError('');

            // Generate secrets for the order
            const generatedSecrets = Array.from({
                length: quote.presets[preset]?.secretsCount || 1,
            }).map(() => ethers.hexlify(ethers.randomBytes(32)));

            setSecrets(generatedSecrets);

            const secretHashes = generatedSecrets.map((s) => ethers.keccak256(s));

            const amountWei = ethers.parseUnits(
                amount,
                availableTokens.find(t => t.address === fromToken)?.decimals || 18
            ).toString();

            const builtQuoteResult = await SwapService.buildQuote({
                quote,
                secretsHashList: secretHashes,
                srcChain: srcChain.id,
                dstChain: dstChain.id,
                srcTokenAddress: fromToken,
                dstTokenAddress: toToken,
                amount: amountWei,
                walletAddress: address,
            });

            setBuiltQuote(builtQuoteResult);
        } catch (error: any) {
            console.error('Error building quote:', error);
            setError(error.message || 'Failed to build quote');
        } finally {
            setLoading(false);
        }
    };

    const handleSubmitOrder = async () => {
        if (!builtQuote || !quote || !window.ethereum) return;

        try {
            setLoading(true);
            setError('');

            const provider = new ethers.BrowserProvider(window.ethereum);
            const signer = await provider.getSigner();
            const { domain, types, message } = builtQuote.typedData;
            const signature = await signer.signTypedData(
                domain,
                { Order: types.Order },
                message
            );

            const result = await SwapService.submitOrder({
                order: message,
                signature,
                quoteId: quote.quoteId,
            });

            setOrderHash(result.orderHash);

            // Start polling for order status
            pollOrderStatus(result.orderHash);
        } catch (error: any) {
            console.error('Error submitting order:', error);
            setError(error.message || 'Failed to submit order');
        } finally {
            setLoading(false);
        }
    };

    const pollOrderStatus = async (hash: string) => {
        const interval = setInterval(async () => {
            try {
                const status = await SwapService.checkOrderStatus(hash);
                setOrderStatus(status);

                // Check if we need to reveal secrets
                const readyFills = status.fills.filter(fill => fill.status === 'ready_for_secret');
                if (readyFills.length > 0 && secrets.length > 0) {
                    // Reveal the first secret for simplicity
                    await SwapService.revealSecrets({
                        orderHash: hash,
                        secret: secrets[0],
                    });
                }

                // Stop polling if the order is completed or failed
                if (status.status === 'completed' || status.status === 'failed') {
                    clearInterval(interval);
                }
            } catch (error) {
                console.error('Error polling order status:', error);
                clearInterval(interval);
            }
        }, 5000); // Poll every 5 seconds

        return () => clearInterval(interval);
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
            <Sidebar />
            <main className={styles.main}>
                <h1 className={styles.title}>Cross-Chain Swap</h1>
                
                {/* Connection Status */}
                {isHydrated && (
                    <div className={styles.connectionStatus}>
                        {address ? (
                            <p>Connected: {address}</p>
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
                        <p>🔄 Processing...</p>
                    </div>
                )}

                <div className={styles.swapForm}>
                    {/* Source Chain Selection */}
                    <div className={styles.inputGroup}>
                        <label>From Chain:</label>
                        <select
                            value={srcChain.id}
                            onChange={(e) => {
                                const chain = SUPPORTED_CHAINS.find(c => c.id === +e.target.value);
                                if (chain) setSrcChain(chain);
                            }}
                            className={styles.select}
                        >
                            {SUPPORTED_CHAINS.map((chain) => (
                                <option key={chain.id} value={chain.id}>
                                    {chain.name}
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* Destination Chain Selection */}
                    <div className={styles.inputGroup}>
                        <label>To Chain:</label>
                        <select
                            value={dstChain.id}
                            onChange={(e) => {
                                const chain = SUPPORTED_CHAINS.find(c => c.id === +e.target.value);
                                if (chain) setDstChain(chain);
                            }}
                            className={styles.select}
                        >
                            {SUPPORTED_CHAINS.map((chain) => (
                                <option key={chain.id} value={chain.id}>
                                    {chain.name}
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* Source Token Selection */}
                    <div className={styles.inputGroup}>
                        <label>From Token:</label>
                        <select
                            value={fromToken}
                            onChange={(e) => setFromToken(e.target.value)}
                            className={styles.select}
                            disabled={loading || !availableTokens.length || !address || !isHydrated}
                        >
                            <option value="">Select token</option>
                            {availableTokens.map((token) => (
                                <option key={token.address} value={token.address}>
                                    {token.symbol} - {token.name}
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* Destination Token Selection */}
                    <div className={styles.inputGroup}>
                        <label>To Token:</label>
                        <select
                            value={toToken}
                            onChange={(e) => setToToken(e.target.value)}
                            className={styles.select}
                            disabled={loading || !availableTokens.length || !address || !isHydrated}
                        >
                            <option value="">Select token</option>
                            {availableTokens.map((token) => (
                                <option key={token.address} value={token.address}>
                                    {token.symbol} - {token.name}
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* Amount Input */}
                    <div className={styles.inputGroup}>
                        <label>Amount:</label>
                        <input
                            type="text"
                            value={amount}
                            onChange={(e) => setAmount(e.target.value)}
                            placeholder="Enter amount"
                            className={styles.input}
                        />
                    </div>

                    {/* Preset Selection */}
                    <div className={styles.inputGroup}>
                        <label>Speed:</label>
                        <select
                            value={preset}
                            onChange={(e) => setPreset(e.target.value as SwapPreset)}
                            className={styles.select}
                        >
                            {SWAP_PRESETS.map((p) => (
                                <option key={p} value={p}>
                                    {p.charAt(0).toUpperCase() + p.slice(1)}
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* Action Buttons */}
                    <div className={styles.buttonGroup}>
                        {chainId !== srcChain.id ? (
                            <button
                                onClick={handleNetworkSwitch}
                                className={styles.button}
                                disabled={loading}
                            >
                                Switch to {srcChain.name}
                            </button>
                        ) : !quote ? (
                            <button
                                onClick={handleGetQuote}
                                className={styles.button}
                                disabled={loading || !fromToken || !toToken || !amount}
                            >
                                Get Quote
                            </button>
                        ) : !builtQuote ? (
                            <button
                                onClick={handleBuildQuote}
                                className={styles.button}
                                disabled={loading}
                            >
                                Build Quote
                            </button>
                        ) : !orderHash ? (
                            <button
                                onClick={handleSubmitOrder}
                                className={styles.button}
                                disabled={loading}
                            >
                                Submit Order
                            </button>
                        ) : null}
                    </div>

                    {/* Order Status */}
                    {orderStatus && (
                        <div className={styles.orderStatus}>
                            <h3>Order Status</h3>
                            <p>Status: {orderStatus.status}</p>
                            {orderStatus.fills.map((fill, index) => (
                                <div key={index} className={styles.fill}>
                                    <p>Fill Status: {fill.status}</p>
                                    <p>Transaction: {fill.txHash}</p>
                                    <p>Amount: {fill.filledAuctionTakerAmount}</p>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
};

export default SwapPage; 