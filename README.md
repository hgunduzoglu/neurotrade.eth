NeuroTrade.eth

NeuroTrade.eth is an omnichain decentralized AI trading agent that helps users trade seamlessly and intelligently across multiple blockchains. It combines AI-generated trading signals, automated trading execution, and private, confidential compute to provide the next generation of decentralized finance tools.

NeuroTrade supports three modes of operation:

✅ AI Signals (Manual Execution) – AI generates trading signals, but the user decides whether to execute them.

✅ Fully Automated AI Trading – The AI automatically executes trades based on market conditions without user intervention.

✅ Automated User-Defined Rules – Users define specific trading rules (e.g. "Buy ETH if price drops to $2,400"), and NeuroTrade automatically executes trades when those conditions are met.

NeuroTrade.eth is designed to maximize eligibility for numerous hackathon bounties by integrating many state-of-the-art web3 technologies.

Technologies & Tools Used

1. Fetch.AI (uAgents, Agentverse, ASI:One)

Hosts the core NeuroTrade agent.

Handles:

receiving user prompts

generating AI trading signals

managing user-defined rules

Deployed either locally or via Agentverse.ai.

Registered as an agent discoverable on ASI:One.



2. The Graph (Subgraphs & Substreams)

Provides onchain data feeds for:

token prices

liquidity pools

volume changes

Enables NeuroTrade to:

detect market opportunities

trigger user rules

generate informed AI signals.



3. LayerZero

Provides cross-chain messaging and bridging.

Enables:

moving tokens between chains

executing trades across EVM networks

Integrated for executing user trades on chains like Ethereum, Arbitrum, Base, and Mantle.



4. Oasis ROFL (Runtime Off-chain Logic)

Powers private compute for:

confidential AI logic

secure storage of user-defined trading rules

Ensures:

trading strategies remain private

regulatory and user privacy compliance.



5. Privy

Handles:

user authentication (email, social, wallet-based login)

embedded wallet management

Simplifies onboarding for non-crypto users.



6. ENS (Ethereum Name Service)

NeuroTrade is assigned the identity neurotrade.eth.

Benefits:

easy recognition of the AI agent

can store agent metadata in text records (e.g. supported chains, trading model versions).



7. Ledger / ERC-7730 Clear Signing

Provides clear, human-readable transaction signing for:

manual trades

automatic trades if user chooses confirmation step

Prevents malicious transactions by requiring explicit user approval.



8. INTMAX (Optional)

Provides privacy-focused payments and transfers.

Users can:

pay for NeuroTrade’s subscription or services anonymously

execute private token transfers.



How It Works

User Flow

Login

User authenticates via Privy.

NeuroTrade displays ENS identity if available (e.g. neurotrade.eth).

Mode Selection

User chooses:

AI signals only (manual execution)

fully automated AI trading

automated trading via user-defined rules

AI Signals

NeuroTrade scans The Graph data feeds.

Generates signals like:

“BUY ETH on Arbitrum at $3,300. Confidence: 92%.”

User can manually execute the trade.

Fully Automated AI Trading

NeuroTrade’s AI decides and executes trades without user intervention.

Executes cross-chain transactions via LayerZero.

User-Defined Rules

User sets rules such as:

“Buy ETH on Ethereum if price ≤ $2,400, sell if ≥ $2,600.”

NeuroTrade stores rules securely in Oasis ROFL.

Monitors onchain data via The Graph.

Executes trades automatically when conditions are met.

Cross-Chain Execution

Trades are performed across chains using LayerZero.

Ensures best prices and liquidity utilization.

Clear Signing

For any manual or auto-triggered trade, NeuroTrade optionally prompts Ledger for clear signing using ERC-7730.

Private Payments (Optional)

Users can pay NeuroTrade fees or subscribe privately via INTMAX.

Features

Hybrid trading system:

manual AI signals

fully automated AI trades

user-defined trading rules

Cross-chain asset management

Private AI compute for sensitive trading logic

User-friendly UI with embedded wallet auth

ENS identity for seamless user trust

Clear signing for transaction safety





Setup & Running

Frontend: React.js or Next.js

Styling: TailwindCSS

Auth & Wallet: Privy SDK

Agent Logic: Fetch.AI SDK

Data Feeds: The Graph (GraphQL)

Cross-Chain Execution: LayerZero SDK

Private Compute: Oasis ROFL SDK

ENS Integration: ethers.js or ENS.js

Hardware Signing: Ledger SDK

Steps to Run (Example Flow)

Clone repo

Install dependencies

Configure .env for:

LayerZero endpoints

Oasis API keys

Privy credentials

Run local server:

npm run dev

Deploy smart contracts on:

LayerZero testnets

Target chains (e.g. Arbitrum, Base)

Deploy ROFL service on Oasis

Future Improvements

Support additional AI models for trading logic

Integration with additional chains

Voice or natural language input for rule creation

Deeper analytics and charting tools

NeuroTrade.eth represents the next leap in decentralized trading:

A truly omnichain, intelligent, private trading agent — designed for both security and innovation.

Let’s build the future of trading together!