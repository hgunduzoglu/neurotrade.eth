import { Tokens } from '../types/swap';

export const tokens: Tokens = {
    1: [ // Ethereum
        {
            name: "USDC",
            address: "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            decimals: 6,
            symbol: "USDC",
            logoURI: "https://assets.coingecko.com/coins/images/6319/thumb/USD_Coin_icon.png"
        },
        {
            name: "USDT",
            address: "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            decimals: 6,
            symbol: "USDT",
            logoURI: "https://assets.coingecko.com/coins/images/325/thumb/Tether.png"
        },
        {
            name: "Wrapped Ether",
            address: "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            decimals: 18,
            symbol: "WETH",
            logoURI: "https://assets.coingecko.com/coins/images/2518/thumb/weth.png"
        },
        {
            name: "Wrapped Bitcoin",
            address: "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
            decimals: 8,
            symbol: "WBTC",
            logoURI: "https://assets.coingecko.com/coins/images/7598/thumb/wrapped_bitcoin_wbtc.png"
        }
    ],
    137: [ // Polygon
        {
            name: "USDC",
            address: "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
            decimals: 6,
            symbol: "USDC",
            logoURI: "https://assets.coingecko.com/coins/images/6319/thumb/USD_Coin_icon.png"
        },
        {
            name: "USDT",
            address: "0xc2132D05D31c914a87C6611C10748AEb04B58e8F",
            decimals: 6,
            symbol: "USDT",
            logoURI: "https://assets.coingecko.com/coins/images/325/thumb/Tether.png"
        },
        {
            name: "Wrapped Ether",
            address: "0x7ceb23fd6bc0add59e62ac25578270cff1b9f619",
            decimals: 18,
            symbol: "WETH",
            logoURI: "https://assets.coingecko.com/coins/images/2518/thumb/weth.png"
        },
        {
            name: "Wrapped Bitcoin",
            address: "0x1bfd67037b42cf73acf2047067bd4f2c47d9bfd6",
            decimals: 8,
            symbol: "WBTC",
            logoURI: "https://assets.coingecko.com/coins/images/7598/thumb/wrapped_bitcoin_wbtc.png"
        }
    ]
}; 