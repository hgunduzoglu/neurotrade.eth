import { Chain } from '../services/swapService';

export const SUPPORTED_CHAINS: Chain[] = [
    {
        id: 1,
        name: 'Ethereum',
        rpc: 'https://eth-mainnet.g.alchemy.com/v2/your-api-key'
    },
    {
        id: 137,
        name: 'Polygon',
        rpc: 'https://polygon-mainnet.g.alchemy.com/v2/your-api-key'
    },
    {
        id: 56,
        name: 'BSC',
        rpc: 'https://bsc-dataseed.binance.org'
    },
    {
        id: 42161,
        name: 'Arbitrum',
        rpc: 'https://arb1.arbitrum.io/rpc'
    },
    {
        id: 10,
        name: 'Optimism',
        rpc: 'https://mainnet.optimism.io'
    }
];

export const SWAP_PRESETS = [
    'fast',
    'medium',
    'slow'
] as const;

export type SwapPreset = typeof SWAP_PRESETS[number]; 