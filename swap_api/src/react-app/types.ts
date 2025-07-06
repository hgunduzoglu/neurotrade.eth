import { ethers } from "ethers";

export interface Chain {
    id: number;
    name: string;
    rpc: string;
}

export interface Token {
    name: string;
    address: string;
    decimals: number;
}

export interface Tokens {
    [key: number]: Token[];
}

export interface Wallet {
    address: string;
    provider: ethers.BrowserProvider | null;
    signer: ethers.JsonRpcSigner | null;
}

export interface Quote {
    quoteId: string;
    srcTokenAmount: string;
    dstTokenAmount: string;
    presets: {
        [key: string]: {
            auctionDuration: number;
            startAuctionIn: number;
            initialRateBump: number;
            auctionStartAmount: string;
            startAmount: string;
            auctionEndAmount: string;
            exclusiveResolver: string | null;
            costInDstToken: string;
            points: {
                delay: number;
                coefficient: number;
            }[];
            allowPartialFills: boolean;
            allowMultipleFills: boolean;
            gasCost: {
                gasBumpEstimate: number;
                gasPriceEstimate: string;
            };
            secretsCount: number;
        }
    };
    timeLocks: {
        srcWithdrawal: number;
        srcPublicWithdrawal: number;
        srcCancellation: number;
        srcPublicCancellation: number;
        dstWithdrawal: number;
        dstPublicWithdrawal: number;
        dstCancellation: number;
    };
    srcEscrowFactory: string;
    dstEscrowFactory: string;
    srcSafetyDeposit: string;
    dstSafetyDeposit: string;
    whitelist: string[];
    recommendedPreset: string;
    prices: {
        usd: {
            srcToken: string;
            dstToken: string;
        }
    };
    volume: {
        usd: {
            srcToken: string;
            dstToken: string;
        }
    };
    priceImpactPercent: number;
    autoK: number;
    k: number;
    mxK: number;
}

export interface BuildQuoteResponse {
    typedData: {
        primaryType: string;
        types: {
            EIP712Domain: {
                name: string;
                type: string;
            }[];
            Order: {
                name: string;
                type: string;
            }[];
        };
        domain: {
            name: string;
            version: string;
            chainId: number;
            verifyingContract: string;
        };
        message: {
            maker: string;
            makerAsset: string;
            takerAsset: string;
            makerTraits: string;
            salt: string;
            makingAmount: string;
            takingAmount: string;
            receiver: string;
        };
    };
    orderHash: string;
    extension: string;
}

export interface Order {
    hash: string;
    // Add other properties from the 1inch API response as needed
}

export interface EscrowEvent {
    transactionHash: string;
    escrow: string;
    side: string;
    action: string;
    blockTimestamp: number;
}

export interface Fill {
    txHash: string;
    filledMakerAmount: string;
    filledAuctionTakerAmount: string;
    escrowEvents: EscrowEvent[];
    status: string;
}

export interface OrderStatus {
    orderHash: string;
    srcChainId: number;
    dstChainId: number;
    validation: string;
    remainingMakerAmount: string;
    deadline: number;
    order: {
        salt: string;
        maker: string;
        receiver: string;
        makerAsset: string;
        takerAsset: string;
        makerTraits: string;
        makingAmount: string;
        takingAmount: string;
    };
    extension: string;
    status: string;
    createdAt: number;
    takerAsset: string;
    srcTokenPriceUsd: string;
    dstMarketAmount: string;
    dstTokenPriceUsd: string;
    fills: Fill[];
    cancelTx: any; // or a more specific type if you know the structure
    approximateTakingAmount: string;
    points: any[]; // or a more specific type
    auctionStartDate: number;
    auctionDuration: number;
    initialRateBump: number;
    timeLocks: string;
    positiveSurplus: string;
    cancelable: boolean;
}

// Extend the Window interface to include the ethereum property
declare global {
    interface Window {
        ethereum?: any;
    }
}
