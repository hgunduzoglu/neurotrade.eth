import type { AppProps } from 'next/app';
import { WagmiProvider } from 'wagmi';
import { QueryClientProvider } from '@tanstack/react-query';
import { config, queryClient } from '../config/wagmi';
import { PrivyProvider } from '../providers/PrivyProvider';
import '../styles/globals.css';

export default function App({ Component, pageProps }: AppProps) {
  return (
    <WagmiProvider config={config}>
      <QueryClientProvider client={queryClient}>
        <PrivyProvider>
          <Component {...pageProps} />
        </PrivyProvider>
      </QueryClientProvider>
    </WagmiProvider>
  );
} 