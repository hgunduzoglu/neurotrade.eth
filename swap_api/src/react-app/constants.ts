import { Chain, Tokens } from "./types";

export const chains: Chain[] = [
    {
        "id": 1,
        "name": "Ethereum",
        "rpc": "https://eth.llamarpc.com"
    },
    {
        "id": 137,
        "name": "Polygon",
        "rpc": "https://polygon-rpc.com"
    },
    {
        "id": 324,
        "name": "zkSync",
        "rpc": "https://mainnet.era.zksync.io"
    },
    {
        "id": 56,
        "name": "Binance",
        "rpc": "https://bsc-dataseed.binance.org/"
    },
    {
        "id": 42161,
        "name": "Arbitrum",
        "rpc": "https://arb1.arbitrum.io/rpc"
    },
    {
        "id": 43114,
        "name": "Avalanche",
        "rpc": "https://api.avax.network/ext/bc/C/rpc"
    },
    {
        "id": 10,
        "name": "Optimism",
        "rpc": "https://mainnet.optimism.io"
    },
    {
        "id": 250,
        "name": "Fantom",
        "rpc": "https://rpc.ftm.tools/"
    },
    {
        "id": 100,
        "name": "Gnosis",
        "rpc": "https://rpc.gnosischain.com/"
    },
    {
        "id": 8453,
        "name": "Coinbase",
        "rpc": "https://mainnet.base.org"
    },
    {
        "id": 59144,
        "name": "Linea",
        "rpc": "https://rpc.linea.build"
    }
]

export const tokens: Tokens = {
    1: [ // Ethereum
        {
            "name": "USDC",
            "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "decimals": 6
        },
        {
            "name": "USDT",
            "address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "decimals": 6
        },
        {
            "name": "WETH",
            "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "decimals": 18
        },
        {
            "name": "WBTC",
            "address": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
            "decimals": 8
        }
    ],
    137: [ // Polygon
        {
            "name": "USDC",
            "address": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
            "decimals": 6
        },
        {
            "name": "USDT",
            "address": "0xc2132D05D31c914a87C6611C10748AEb04B58e8F",
            "decimals": 6
        },
        {
            "name": "WETH",
            "address": "0x7ceb23fd6bc0add59e62ac25578270cff1b9f619",
            "decimals": 18
        },
        {
            "name": "WBTC",
            "address": "0x1bfd67037b42cf73acf2047067bd4f2c47d9bfd6",
            "decimals": 8
        }
    ],
    324: [ // zkSync
        {
            "name": "USDC",
            "address": "0x1d17CBcF0D6D143135aE902365D2E5e2A16538D4", // Corrected address
            "decimals": 6
        },
        {
            "name": "USDT",
            "address": "0x493257fD37EDB34451f6232d22D691441065a26b",
            "decimals": 6
        },
        {
            "name": "WETH",
            "address": "0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91",
            "decimals": 18
        },
        {
            "name": "WBTC",
            "address": "0xBBeB516fbF1A48F4312f08304D70195684E88AB7",
            "decimals": 8
        }
    ],
    56: [ // Binance
        {
            "name": "USDC",
            "address": "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d",
            "decimals": 6
        },
        {
            "name": "USDT",
            "address": "0x55d398326f99059fF775485246999027B3197955",
            "decimals": 18
        },
        {
            "name": "WETH",
            "address": "0x2170ed0880ac9a755fd29b2688956bd959f933f8",
            "decimals": 18
        },
        {
            "name": "WBTC",
            "address": "0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c",
            "decimals": 18
        }
    ],
    42161: [ // Arbitrum
        {
            "name": "USDC",
            "address": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
            "decimals": 6
        },
        {
            "name": "USDT",
            "address": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
            "decimals": 6
        },
        {
            "name": "WETH",
            "address": "0x82af49447d8a07e3bd95bd0d56f35241523fbab1",
            "decimals": 18
        },
        {
            "name": "WBTC",
            "address": "0x2f2a2543b76a4166549f7aab2e75bef0aefc5b0f",
            "decimals": 8
        }
    ],
    43114: [ // Avalanche
        {
            "name": "USDC",
            "address": "0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E",
            "decimals": 6
        },
        {
            "name": "USDT",
            "address": "0x9702230A8Ea53601f5E225511125f90A9354FC13",
            "decimals": 6
        },
        {
            "name": "WETH.e",
            "address": "0x49d5c2d72cd2e47d5abddcf958ce3620cd10925d",
            "decimals": 18
        },
        {
            "name": "WBTC.e",
            "address": "0x50b7545627a5162f82a992c33b87adc75187b218",
            "decimals": 8
        }
    ],
    10: [ // Optimism
        {
            "name": "USDC",
            "address": "0x7F5c764cBc14f9669B88837ca1490cCa17c31607",
            "decimals": 6
        },
        {
            "name": "USDT",
            "address": "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58",
            "decimals": 6
        },
        {
            "name": "WETH",
            "address": "0x4200000000000000000000000000000000000006",
            "decimals": 18
        },
        {
            "name": "WBTC",
            "address": "0x68f180fcce6836688e9084f035309e29bf0a2095",
            "decimals": 8
        }
    ],
    250: [ // Fantom
        {
            "name": "USDC",
            "address": "0x04068DA6C83AFCFA0e13ba15A6696662335D5B75",
            "decimals": 6
        },
        {
            "name": "USDT",
            "address": "0x049d68029688eAbF473097a2fC38ef61633A3C7A",
            "decimals": 6
        },
        {
            "name": "WETH",
            "address": "0x74b23882a30290451a17c44f4f05243b6b58c76d",
            "decimals": 18
        },
        {
            "name": "WBTC",
            "address": "0x321162cd933e2be498cd2267a90534a804051b11",
            "decimals": 8
        }
    ],
    100: [ // Gnosis
        {
            "name": "USDC",
            "address": "0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83",
            "decimals": 6
        },
        {
            "name": "USDT",
            "address": "0x4ECaBa5870353805a9F068101A40E0f324D46B0F",
            "decimals": 6
        },
        {
            "name": "WETH",
            "address": "0x6a023ccd1ff6f2045c3309768eaade8e6da8729b",
            "decimals": 18
        },
        {
            "name": "WBTC",
            "address": "0x8e5bBbb09Ed1ebdE8674Cda39A0c169401db4252",
            "decimals": 8
        }
    ],
    8453: [ // Coinbase
        {
            "name": "USDC",
            "address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
            "decimals": 6
        },
        {
            "name": "USDT",
            "address": "0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA",
            "decimals": 6
        },
        {
            "name": "WETH",
            "address": "0x4200000000000000000000000000000000000006",
            "decimals": 18
        }
    ],
    59144: [ // Linea
        {
            "name": "USDC",
            "address": "0x176211869cA2b568f2A7D4EE941E073a821EE1ff",
            "decimals": 6
        },
        {
            "name": "USDT",
            "address": "0xA219439258ca9da29E9Cc442AFCD6099D5E8861d",
            "decimals": 6
        },
        {
            "name": "WETH",
            "address": "0xe5D7C2a44FfDDf6b295A15c148167daaAf5Cf34f",
            "decimals": 18
        }
    ]
}

export const presets = ['fast', 'medium', 'slow'];