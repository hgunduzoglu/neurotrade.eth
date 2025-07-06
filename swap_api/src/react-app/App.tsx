// src/App.tsx

import { useState, useEffect } from "react";
import { ethers, TypedDataDomain, TypedDataField } from "ethers";
import { chains, tokens, presets } from "./constants";
import { Chain, Token, Wallet, Quote, BuildQuoteResponse, OrderStatus } from "./types";
import "./App.css";

const ERC20_ABI = [
    "function allowance(address owner, address spender) view returns (uint256)",
    "function approve(address spender, uint256 amount) returns (bool)",
];

const ONEINCH_V6_AGGREGATOR = "0x111111125421ca6dc452d289314280a0f8842a65";

function App() {
  const [wallet, setWallet] = useState<Wallet>({
    address: "",
    provider: null,
    signer: null,
  });
  const [srcChain, setSrcChain] = useState<Chain>(chains[0]);
  const [dstChain, setDstChain] = useState<Chain>(chains[1]);
  const [srcToken, setSrcToken] = useState<Token>(tokens[srcChain.id][0]);
  const [dstToken, setDstToken] = useState<Token>(tokens[dstChain.id][0]);
  const [amount, setAmount] = useState("1");
  const [quote, setQuote] = useState<Quote | null>(null);
  const [builtQuote, setBuiltQuote] = useState<BuildQuoteResponse | null>(null);
  const [isApproving, setIsApproving] = useState(false);
  const [order, setOrder] = useState<any | null>(null);
  const [preset, setPreset] = useState(presets[0]);
  const [allowance, setAllowance] = useState<string | null>(null);
  const [secretHashes, setSecretHashes] = useState<string[] | null>(null);
  const [generatedSecrets, setGeneratedSecrets] = useState<string[] | null>(
    null
  );
  const [submittedOrderHash, setSubmittedOrderHash] = useState<string | null>(
    null
  );
  const [orderStatus, setOrderStatus] = useState<OrderStatus | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const connectWallet = async () => {
    if (window.ethereum) {
      try {
        const provider = new ethers.BrowserProvider(window.ethereum);
        await provider.send("eth_requestAccounts", []);
        const signer = await provider.getSigner();
        const address = await signer.getAddress();
        setWallet({ address, provider, signer });
      } catch (error) {
        console.error("Failed to connect wallet:", error);
      }
    } else {
      alert("MetaMask is not installed.");
    }
  };

  const checkAllowance = async () => {
    if (!wallet.provider || !wallet.address || !srcToken) return;
    try {
      const tokenContract = new ethers.Contract(srcToken.address, ERC20_ABI, wallet.provider);
      const currentAllowance = await tokenContract.allowance(wallet.address, ONEINCH_V6_AGGREGATOR);
      setAllowance(currentAllowance.toString());
    } catch (error) {
      console.error("Failed to check allowance:", error);
      setAllowance(null);
    }
  };

  const getQuote = async () => {
    setBuiltQuote(null);
    setOrder(null);
    const params = new URLSearchParams({
      srcChain: srcChain.id.toString(),
      srcTokenAddress: srcToken.address,
      dstChain: dstChain.id.toString(),
      dstTokenAddress: dstToken.address,
      amount: ethers.parseUnits(amount, srcToken.decimals).toString(),
      walletAddress: wallet.address,
      preset: preset,
      enableEstimate: "true",
    });

    const response = await fetch(`/api/quote?${params.toString()}`);
    const data = await response.json();
    setQuote(data);
  };

  const approveSpender = async () => {
    if (!quote || !wallet.provider || !wallet.signer) return;

    const spender = ONEINCH_V6_AGGREGATOR; // Using 1inch v6 Aggregator

    setIsApproving(true);
    try {
        const tokenContract = new ethers.Contract(srcToken.address, ERC20_ABI, wallet.signer);
        const tx = await tokenContract.approve(spender, ethers.MaxUint256);
        await tx.wait();
        alert("Approval successful!");
        // Re-fetch quote to get updated allowance info, or manually update state
        await checkAllowance();
    } catch (error) {
        console.error("Approval failed:", error);
        alert("Approval failed. Please try again.");
    } finally {
        setIsApproving(false);
    }
  };

  const buildQuote = async () => {
    if (!quote || !wallet.provider || !wallet.signer) return;

    // Check if the wallet is on the correct network
    const network = await wallet.provider.getNetwork();
    if (network.chainId !== BigInt(srcChain.id)) {
      try {
        await window.ethereum.request({
          method: 'wallet_switchEthereumChain',
          params: [{ chainId: ethers.toBeHex(srcChain.id) }],
        });
        // After switching, we'll just return. The user can click "Build Quote" again.
        // A more advanced implementation might re-trigger the quote build automatically.
        alert(`Switched to ${srcChain.name}. Please click "Build Quote" again.`);
        return;
      } catch (switchError: any) {
        // This error code indicates that the chain has not been added to MetaMask.
        if (switchError.code === 4902) {
          try {
            await window.ethereum.request({
              method: 'wallet_addEthereumChain',
              params: [
                {
                  chainId: ethers.toBeHex(srcChain.id),
                  chainName: srcChain.name,
                  rpcUrls: [srcChain.rpc],
                },
              ],
            });
          } catch (addError) {
            alert(`Failed to add the ${srcChain.name} network to your wallet.`);
            return;
          }
        } else {
            alert(`Failed to switch to the ${srcChain.name} network. Please do it manually in your wallet.`);
            return;
        }
      }
    }

    // 1. Build the quote
    const generatedSecrets = Array.from({
      length: quote.presets[preset]?.secretsCount || 1,
    }).map(() => ethers.hexlify(ethers.randomBytes(32)));
    setGeneratedSecrets(generatedSecrets);

    const secretHashes = generatedSecrets.map((s) => ethers.keccak256(s));
    setSecretHashes(secretHashes);

    const requestBody = {
      quote,
      secretsHashList: secretHashes,
    };

    const amountWei = ethers.parseUnits(amount, srcToken.decimals);

    const params = new URLSearchParams({
      srcChain: srcChain.id.toString(),
      dstChain: dstChain.id.toString(),
      srcTokenAddress: srcToken.address,
      dstTokenAddress: dstToken.address,
      amount: amountWei.toString(),
      walletAddress: wallet.address,
    });

    const response = await fetch(`/api/quote/build?${params.toString()}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestBody),
    });
    const data = await response.json();
    setBuiltQuote(data);
    setOrder(null);
  };

  const createOrder = async () => {
    if (!builtQuote || !wallet.signer || !quote) {
      console.error("Cannot sign order: No built quote, signer or quote");
      return null;
    }

    try {
      const { typedData } = builtQuote;
      if (!typedData || !typedData.domain || !typedData.types || !typedData.message) {
          console.error("Invalid typed data in builtQuote response", builtQuote);
          return null;
      }
      const { domain, types, message } = typedData;

      const domainForSigning: TypedDataDomain = {
        name: domain.name,
        version: domain.version,
        chainId: Number(domain.chainId),
        verifyingContract: domain.verifyingContract,
      };

      const typesForSigning: Record<string, TypedDataField[]> = { ...types };
      delete typesForSigning.EIP712Domain;

      const signature = await wallet.signer.signTypedData(
        domainForSigning,
        typesForSigning,
        message
      );

      const signedOrder = {
        order: message,
        signature: signature,
        quoteId: quote.quoteId, // Correctly use quote.quoteId
      };
      
      setOrder(signedOrder);
      return signedOrder;
    } catch (error) {
      console.error("Failed to sign order:", error);
      return null;
    }
  };

  const submitSecret = async () => {
    if (!generatedSecrets || !submittedOrderHash) {
      alert("No secrets generated or order not submitted.");
      return;
    }

    try {
      const response = await fetch("/api/order/reveal-secrets", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          orderHash: submittedOrderHash,
          secret: generatedSecrets[0], // Assuming we submit the first secret for simplicity
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.description || "Failed to submit secrets");
      }

      console.log("Secret submission result:");
      alert("Secrets submitted successfully!");
    } catch (error: any) {
      console.error("Secret submission error:", error);
      alert(`Error submitting secrets: ${error.message}`);
    }
  };

  const checkFillsAndSubmitSecrets = async () => {
    if (!submittedOrderHash || !generatedSecrets) {
      alert("No order submitted or secrets generated.");
      return;
    }

    // This is a conceptual implementation based on the provided example.
    // A real implementation would need to know which secret corresponds to which fill.
    // The example `secrets[fill.idx]` suggests an index mapping.
    // Here, we'll assume the first secret for the first fill if it's ready.

    if (orderStatus && orderStatus.fills && orderStatus.fills.length > 0) {
      // Assuming we'd check if a fill is in a state ready for secret submission.
      // For this example, we'll just check if there are any fills.
      const readyFills = orderStatus.fills.filter(fill => fill.status !== 'filled'); // Example condition

      if (readyFills.length > 0) {
        // In a real scenario with multiple secrets and fills, we'd need a mapping.
        // e.g. submitSecret(submittedOrderHash, generatedSecrets[fill.idx])
        // For now, we'll just call the existing submitSecret function which sends all secrets.
        await submitSecret();
      } else {
        alert("No fills are currently ready to accept secrets.");
      }
    } else {
      alert("No fills found for this order yet. Please check the order status.");
    }
  }

  const submitOrder = async () => {
    // Ensure we have the latest signed order, creating it if necessary.
    const signedOrder = order || (await createOrder());

    if (!signedOrder || !builtQuote || !quote) {
      alert("Failed to create or sign the order, or quote is missing.");
      return;
    }

    // Now that we are sure signedOrder is fresh, let's use it.
    const submissionPayload: any = {
      order: signedOrder.order,
      signature: signedOrder.signature,
      quoteId: signedOrder.quoteId, // Use quoteId from signedOrder
      srcChainId: srcChain.id,
      extension: builtQuote.extension || "0x",
    };

    if (quote.presets[preset]?.secretsCount > 1) {
      submissionPayload.secretHashes = secretHashes;
    }

    setIsSubmitting(true);
    try {
      const response = await fetch("/api/order/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(submissionPayload),
      });

      if (!response.ok) {
        const errorText = await response.text();
        try {
          const errorData = JSON.parse(errorText);
          throw new Error(errorData.description || "Failed to submit order");
        } catch (e) {
          throw new Error(`Server error: ${response.status} - ${errorText.substring(0, 200)}`);
        }
      }

      // Successful submission might not have a body, or we don't need it.
      // We already have the order hash from the build step.
      alert("Order submitted successfully!");
      const orderHash = builtQuote.orderHash;
      setSubmittedOrderHash(orderHash);
      await checkOrderStatus(orderHash);

    } catch (error: any) {
      console.error("Order submission error:", error);
      alert(`Error submitting order: ${error.message}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  const checkOrderStatus = async (orderHash?: string) => {
    const hash = orderHash || submittedOrderHash;
    if (!hash) {
      alert("No order submitted yet.");
      return;
    }
    try {
      const response = await fetch(`/api/order/status/${hash}`);
      if (response.ok) {
        const data = await response.json();
        setOrderStatus(data);
      } else {
        const errorData = await response.json();
        console.error("Failed to fetch order status:", errorData);
        alert(`Failed to fetch order status: ${errorData.description || response.statusText}`);
      }
    } catch (error) {
      console.error("Error fetching order status:", error);
      alert("Error fetching order status.");
    }
  };

  useEffect(() => {
    if (wallet.address && srcToken) {
      checkAllowance();
    }
  }, [wallet.address, srcToken]);

  useEffect(() => {
    setSrcToken(tokens[srcChain.id][0]);
  }, [srcChain]);

  useEffect(() => {
    setDstToken(tokens[dstChain.id][0]);
  }, [dstChain]);

  return (
    <div className="App">
      <h1>1inch Fusion+ Cross-Chain Swap PoC</h1>
      <div className="card">
        {wallet.address ? (
          <p>Connected: {wallet.address}</p>
        ) : (
          <button onClick={connectWallet}>Connect Wallet</button>
        )}
      </div>

      <div className="card">
        <h2>Swap</h2>
        <div className="row">
          <label>From:</label>
          <select
            value={srcChain.id}
            onChange={(e) => {
              const chain = chains.find((c) => c.id === +e.target.value);
              if (chain) setSrcChain(chain);
            }}
          >
            {chains.map((chain) => (
              <option key={chain.id} value={chain.id}>
                {chain.name}
              </option>
            ))}
          </select>
          <select
            value={srcToken.address}
            onChange={(e) => {
              const token = tokens[srcChain.id].find(
                (t: Token) => t.address === e.target.value
              );
              if (token) setSrcToken(token);
            }}
          >
            {tokens[srcChain.id].map((token: Token) => (
              <option key={token.address} value={token.address}>
                {token.name}
              </option>
            ))}
          </select>
        </div>
        <div className="row">
          <label>To:</label>
          <select
            value={dstChain.id}
            onChange={(e) => {
              const chain = chains.find((c) => c.id === +e.target.value);
              if (chain) setDstChain(chain);
            }}
          >
            {chains.map((chain) => (
              <option key={chain.id} value={chain.id}>
                {chain.name}
              </option>
            ))}
          </select>
          <select
            value={dstToken.address}
            onChange={(e) => {
              const token = tokens[dstChain.id].find(
                (t: Token) => t.address === e.target.value
              );
              if (token) setDstToken(token);
            }}
          >
            {tokens[dstChain.id].map((token: Token) => (
              <option key={token.address} value={token.address}>
                {token.name}
              </option>
            ))}
          </select>
        </div>
        <div className="row">
          <label>Amount:</label>
          <input
            type="text"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
          />
        </div>
        <div className="row">
          <label>Preset:</label>
          <select
            value={preset}
            onChange={(e) => setPreset(e.target.value)}
          >
            {presets.map((p) => (
              <option key={p} value={p}>
                {p}
              </option>
            ))}
          </select>
        </div>
        <button onClick={getQuote} disabled={!wallet.address}>
          Get Quote
        </button>
      </div>

      {quote && (
        <div className="card">
          <h2>Quote</h2>
          <p>
            Receive:{" "}
            {ethers.formatUnits(quote.dstTokenAmount, dstToken.decimals)} {dstToken.name}
          </p>
          <p>Price Impact: {quote.priceImpactPercent}%</p>
          <p>Recommended Preset: {quote.recommendedPreset}</p>
          <p>
            Src Token Price (USD): {quote.prices.usd.srcToken}
          </p>
          <p>
            Dst Token Price (USD): {quote.prices.usd.dstToken}
          </p>
          {allowance && BigInt(allowance) < ethers.parseUnits(amount, srcToken.decimals) ? (
              <button onClick={approveSpender} disabled={!wallet.address || isApproving}>
                  {isApproving ? "Approving..." : "Approve"}
              </button>
          ) : (
            <button onClick={buildQuote} disabled={!wallet.address}>
              Build Quote
            </button>
          )}
          <button onClick={submitOrder} disabled={!wallet.address || !builtQuote || isSubmitting}>
            {isSubmitting ? 'Submitting...' : 'Submit Order'}
          </button>
          <button onClick={() => checkOrderStatus()} disabled={!submittedOrderHash}>
            Check Order Status
          </button>
        </div>
      )}

      {orderStatus && (
        <div className="card">
          <h2>Order Status</h2>
          <p>Status: {orderStatus.status}</p>
          <p>Hash: {orderStatus.orderHash}</p>
          {orderStatus.fills?.length > 0 && (
            <div>
              <h4>Fills:</h4>
              {orderStatus.fills.map((fill, index) => (
                <div key={index} className="fill-details">
                  <p><b>Fill Status:</b> {fill.status}</p>
                  <p><b>Tx Hash:</b> {fill.txHash}</p>
                  <p><b>Filled Amount:</b> {ethers.formatUnits(fill.filledMakerAmount, srcToken.decimals)} {srcToken.name}</p>
                  <p><b>Auction Taker Amount:</b> {fill.filledAuctionTakerAmount}</p>
                  <h5>Escrow Events:</h5>
                  {fill.escrowEvents.map((event, eventIndex) => (
                    <div key={eventIndex} className="escrow-event">
                      <p><b>Action:</b> {event.action}</p>
                      <p><b>Side:</b> {event.side}</p>
                      <p><b>Escrow:</b> {event.escrow}</p>
                      <p><b>Tx Hash:</b> {event.transactionHash}</p>
                    </div>
                  ))}
                </div>
              ))}
            </div>
          )}
          <button
            onClick={() => checkOrderStatus()}
            disabled={!submittedOrderHash}
          >
            Check Status
          </button>
          <button
            onClick={checkFillsAndSubmitSecrets}
            disabled={!submittedOrderHash || !generatedSecrets || !orderStatus || orderStatus.fills.length === 0}
          >
            Submit Secret
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
