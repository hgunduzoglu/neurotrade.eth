'use client';
import { PrivyProvider as Provider } from '@privy-io/react-auth';
import { ReactNode } from 'react';
import { mainnet, goerli, polygon, arbitrum, optimism, base } from 'viem/chains';
import logo from '../assets/images/logo.png';

interface PrivyProviderProps {
  children: ReactNode;
}

export function PrivyProvider({ children }: PrivyProviderProps) {
  return (
    <Provider
      appId={process.env.NEXT_PUBLIC_PRIVY_APP_ID || ''}
      config={{
        loginMethods: ['email', 'wallet'],
        appearance: {
          theme: 'light',
          accentColor: '#676FFF',
          landingHeader: "NeuroTrade.eth",
          loginMessage: "Welcome to new age for trading.",
          showWalletLoginFirst: false,
          logo: logo.src,
        },
        embeddedWallets: {
            createOnLogin: 'users-without-wallets',
        },
        defaultChain: mainnet,
        supportedChains: [
          mainnet,
          goerli,
          polygon,
          arbitrum,
          optimism,
          base
        ],
        externalWallets: {
          metamask: { enabled: true },
          walletConnect: { enabled: true },
          coinbaseWallet: { connectionOptions: 'all' },
        },
      }}
    >
      {children}
    </Provider>
  );
} 