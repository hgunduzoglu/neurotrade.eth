'use client';
import { PrivyProvider as Provider } from '@privy-io/react-auth';
import { ReactNode } from 'react';
import { mainnet, goerli, polygon, arbitrum, optimism, base } from 'viem/chains';

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
          logo: 'https://img.freepik.com/free-psd/gradient-abstract-logo_23-2150689652.jpg?semt=ais_hybrid&w=740',
        },
        embeddedWallets: {
            ethereum: {
                createOnLogin: 'users-without-wallets',
            },
            solana: {
                createOnLogin: 'users-without-wallets',
            }
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
          metamask: true,
          walletConnect: true,
          coinbaseWallet: true,
        },
      }}
    >
      {children}
    </Provider>
  );
} 