# neurotrade.eth

AI-assisted cross-chain trading interface that combines conversational market analysis with explicit, user-signed execution through 1inch Fusion+.

**1inch Partner Prize · ETHGlobal Cannes 2025**

> The assistant analyzes and recommends. The user chooses the trade and signs the order.

## Overview

neurotrade.eth was built to make token research and cross-chain execution part of one coherent flow.

Users can ask the assistant about supported assets, review technical signals and risk indicators, inspect their portfolio, and continue into a cross-chain swap without leaving the application.

Analysis and execution are deliberately separated. The assistant cannot move funds or execute trades autonomously. Every swap is configured and signed explicitly by the user.

The project was built by a team of two for ETHGlobal Cannes 2025 and received a 1inch partner prize.

## Core Features

- Conversational token and market analysis
- Buy, sell, and hold signals with risk context
- Cross-chain swaps through 1inch Fusion+
- Privy email and wallet authentication
- Embedded wallets for users without an existing wallet
- External wallet support through wagmi
- Multi-chain portfolio and transaction views
- Server-side proxying for protected API credentials
- Explicit user approval and signing before execution

## How It Works

```text
User
  |
  v
Next.js Application
  |
  |-- Chat and token analysis ------> FastAPI AI service
  |                                    |
  |                                    `--> Market data and indicators
  |
  |-- Portfolio data ---------------> The Graph
  |
  |-- Wallet onboarding ------------> Privy + wagmi
  |
  `-- Cross-chain swap -------------> Server-side API proxy
                                       |
                                       `--> 1inch Fusion+
````

### Analysis Flow

```text
Natural-language request
        |
        v
Token and market data
        |
        v
Technical indicators
RSI · SMA · momentum · volatility · volume
        |
        v
Signal and risk assessment
BUY · SELL · HOLD
        |
        v
Explanation presented to the user
```

### Swap Flow

```text
Select source and destination assets
        |
        v
Request Fusion+ quote
        |
        v
Build intent-based order
        |
        v
Sign EIP-712 order
        |
        v
Submit to the 1inch relayer
        |
        v
Poll order status
        |
        v
Reveal the matching secret when required
        |
        v
Cross-chain settlement
```

## My Contribution

I owned the third-party integration layer that connected the product experience to its external infrastructure.

My work included:

* Integrating the 1inch Fusion+ quote, build, signing, submission, status, and secret-reveal lifecycle
* Building server-side proxy routes so 1inch credentials were never exposed to the browser
* Connecting Privy authentication and embedded wallet onboarding
* Supporting external wallets through wagmi
* Integrating portfolio and transaction data through The Graph
* Connecting market-data feeds used by the interface and analysis service
* Wiring the frontend to the Python AI service
* Normalizing external API responses and failure states for the application

## Key Technical Decisions

### Analysis and execution are separate

The assistant produces signals, explanations, and risk assessments, but it cannot execute a transaction.

A trade only proceeds after the user opens the swap interface, chooses the parameters, and signs the order. This boundary is enforced by the product flow rather than being left as a disclaimer.

### Fusion+ instead of a basic swap request

1inch Fusion+ uses signed, intent-based orders and resolver-driven execution. The integration supports cross-chain settlement while reducing the transaction's exposure to common forms of MEV.

The resulting flow is more involved than a conventional swap API: the application must construct and sign an order, track its status, and reveal the appropriate secret during execution.

### Provider credentials remain server-side

Authenticated 1inch requests pass through Next.js API routes. The browser communicates only with application-controlled endpoints and never receives the provider credential.

This also creates a single layer for:

* Error normalization
* Request validation
* Provider changes
* Rate-limit handling
* Logging and observability

### Embedded wallets reduce onboarding friction

Privy allows a user to create an embedded wallet through email authentication while still supporting users who prefer MetaMask, WalletConnect, or Coinbase Wallet.

This allows new users to move from login to a signed order without first installing a browser extension.

## Technology Stack

| Area                      | Technologies                           |
| ------------------------- | -------------------------------------- |
| Frontend                  | Next.js 14, React 18, TypeScript       |
| Server state              | TanStack Query                         |
| Authentication            | Privy                                  |
| Wallet integration        | wagmi, viem, ethers.js                 |
| Cross-chain execution     | 1inch Fusion+                          |
| AI service                | Python, FastAPI                        |
| Market analysis           | RSI, SMA, momentum, volatility, volume |
| Portfolio data            | The Graph                              |
| Data visualization        | Chart.js                               |
| API protection            | Next.js API routes                     |
| Optional deployment proxy | Cloudflare Workers                     |

## Running Locally

### Prerequisites

* Node.js
* npm
* Python 3
* A Privy application
* A 1inch developer API key
* Optional Graph API credentials

### 1. Clone the repository

```bash
git clone https://github.com/hgunduzoglu/neurotrade.eth.git
cd neurotrade.eth
```

### 2. Configure the environment

Copy the example environment file:

```bash
cp .env.example .env
```

Configure the required values:

```env
NEXT_PUBLIC_PRIVY_APP_ID=your_privy_app_id
NEXT_PUBLIC_AI_API_URL=http://localhost:8000

ONEINCH_API_KEY=your_1inch_api_key
GRAPH_API_KEY=your_graph_api_key

AGENT_SEED=neurotrade_ai_agent
AGENT_PORT=8000
LOG_LEVEL=INFO
USE_AGENTVERSE=true
```

Do not expose `ONEINCH_API_KEY` through a `NEXT_PUBLIC_` environment variable. It is read only by the server-side proxy.

### 3. Start the application

The repository includes a launcher that installs the frontend and Python dependencies and starts both services:

```bash
python start_neurotrade.py
```

The services will be available at:

```text
Frontend: http://localhost:3000
AI API:   http://localhost:8000
```

### Manual Startup

Install the frontend dependencies:

```bash
npm install
```

Install the AI service dependencies:

```bash
python -m pip install -r neurotrade_ai_agent/requirements.txt
```

Start the AI API:

```bash
python -m uvicorn neurotrade_ai_agent.api_bridge:app \
  --host 0.0.0.0 \
  --port 8000 \
  --reload
```

In another terminal, start the frontend:

```bash
npm run dev
```

## Project Context

* **Event:** ETHGlobal Cannes 2025
* **Team size:** Two
* **Result:** 1inch partner prize
* **My role:** Third-party API and wallet integrations
* **Status:** Hackathon prototype

## Disclaimer

neurotrade.eth is an experimental hackathon project. Its market signals are informational and should not be interpreted as financial advice. Do not use the prototype with funds you cannot afford to lose.

```

