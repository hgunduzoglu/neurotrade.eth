import { createConfig, http } from 'wagmi'
import { mainnet, sepolia, arbitrum, optimism, polygon } from 'wagmi/chains'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

// Create a client
export const queryClient = new QueryClient()

// Configure supported chains
export const config = createConfig({
  chains: [mainnet, sepolia, arbitrum, optimism, polygon],
  transports: {
    [mainnet.id]: http(),
    [sepolia.id]: http(),
    [arbitrum.id]: http(),
    [optimism.id]: http(),
    [polygon.id]: http(),
  },
}) 