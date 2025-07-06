import { ethers } from 'ethers';

const ONEINCH_V6_AGGREGATOR = "0x111111125421ca6dc314280a0f8842a65";

export interface Chain {
    id: number;
    name: string;
    rpc: string;
}

export interface Token {
    address: string;
    symbol: string;
    decimals: number;
    name: string;
    logoURI?: string;
}

export interface Quote {
    quoteId: string;
    presets: Record<string, { secretsCount: number }>;
    // Add other quote fields as needed
}

export interface BuildQuoteResponse {
    typedData: {
        domain: {
            name: string;
            version: string;
            chainId: number;
            verifyingContract: string;
        };
        types: Record<string, Array<{ name: string; type: string }>>;
        message: any;
    };
}

export interface OrderStatus {
    status: string;
    fills: Array<{
        status: string;
        txHash: string;
        filledAuctionTakerAmount: string;
        escrowEvents: Array<{
            action: string;
            side: string;
        }>;
    }>;
}

interface ErrorResponse {
    message: string;
}

const makeRequest = async <T>(path: string, method: string = 'GET', body?: any): Promise<T> => {
    const options: RequestInit = {
        method,
        headers: {
            'Content-Type': 'application/json',
        },
    };

    if (method === 'POST' && body) {
        options.body = JSON.stringify(body);
    }

    const response = await fetch(`/api/swap?path=${path}`, options);
    
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: 'Unknown error' })) as ErrorResponse;
        throw new Error(errorData.message || `Request failed with status ${response.status}`);
    }

    return response.json() as Promise<T>;
};

export const SwapService = {
    getQuote: async (params: {
        srcChain: number;
        srcTokenAddress: string;
        dstChain: number;
        dstTokenAddress: string;
        amount: string;
        walletAddress: string;
        preset: string;
    }): Promise<Quote> => {
        const queryParams = new URLSearchParams({
            path: 'quote',
            srcChain: params.srcChain.toString(),
            srcTokenAddress: params.srcTokenAddress,
            dstChain: params.dstChain.toString(),
            dstTokenAddress: params.dstTokenAddress,
            amount: params.amount,
            walletAddress: params.walletAddress,
            preset: params.preset,
            enableEstimate: 'true',
        });

        return makeRequest<Quote>(`quote?${queryParams.toString()}`);
    },

    buildQuote: async (params: {
        quote: Quote;
        secretsHashList: string[];
        srcChain: number;
        dstChain: number;
        srcTokenAddress: string;
        dstTokenAddress: string;
        amount: string;
        walletAddress: string;
    }): Promise<BuildQuoteResponse> => {
        const queryParams = new URLSearchParams({
            path: 'quote/build',
            srcChain: params.srcChain.toString(),
            dstChain: params.dstChain.toString(),
            srcTokenAddress: params.srcTokenAddress,
            dstTokenAddress: params.dstTokenAddress,
            amount: params.amount,
            walletAddress: params.walletAddress,
        });

        return makeRequest<BuildQuoteResponse>(`quote/build?${queryParams.toString()}`, 'POST', {
            quote: params.quote,
            secretsHashList: params.secretsHashList,
        });
    },

    submitOrder: async (params: {
        order: any;
        signature: string;
        quoteId: string;
    }): Promise<{ orderHash: string }> => {
        return makeRequest<{ orderHash: string }>('order/submit', 'POST', params);
    },

    checkOrderStatus: async (orderHash: string): Promise<OrderStatus> => {
        return makeRequest<OrderStatus>(`order/status?hash=${orderHash}`);
    },

    revealSecrets: async (params: {
        orderHash: string;
        secret: string;
    }): Promise<void> => {
        return makeRequest<void>('order/reveal-secrets', 'POST', params);
    },

    checkAllowance: async (params: {
        tokenAddress: string;
        walletAddress: string;
        provider: ethers.Provider;
    }): Promise<string> => {
        const tokenContract = new ethers.Contract(
            params.tokenAddress,
            [
                'function allowance(address owner, address spender) view returns (uint256)',
            ],
            params.provider
        );

        return tokenContract.allowance(params.walletAddress, ONEINCH_V6_AGGREGATOR);
    },

    approveToken: async (params: {
        tokenAddress: string;
        signer: ethers.Signer;
    }): Promise<ethers.TransactionResponse> => {
        const tokenContract = new ethers.Contract(
            params.tokenAddress,
            [
                'function approve(address spender, uint256 amount) returns (bool)',
            ],
            params.signer
        );

        return tokenContract.approve(ONEINCH_V6_AGGREGATOR, ethers.MaxUint256);
    },
}; 