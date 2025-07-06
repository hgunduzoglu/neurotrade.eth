export interface Token {
    name: string;
    address: string;
    decimals: number;
    symbol: string;
    logoURI?: string;
}

export interface Tokens {
    [chainId: number]: Token[];
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

export interface Fill {
    txHash: string;
    filledMakerAmount: string;
    filledAuctionTakerAmount: string;
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
    approximateTakingAmount: string;
    points: any[];
    auctionStartDate: number;
    auctionDuration: number;
    initialRateBump: number;
    timeLocks: string;
    positiveSurplus: string;
    cancelable: boolean;
} 