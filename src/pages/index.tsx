import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { usePrivy } from '@privy-io/react-auth';
import { WagmiConfig } from 'wagmi';
import { QueryClientProvider } from '@tanstack/react-query';
import styles from '@/styles/Home.module.css';
import { config, queryClient } from '@/config/wagmi';
import { EnsProfile } from '@/components/EnsProfile';
import { TextRecords } from '@/components/TextRecords';
import Link from 'next/link';

export default function Home() {
  const router = useRouter();
  const { login, logout, authenticated, user } = usePrivy();

  useEffect(() => {
    router.replace('/homepage');
  }, [router]);

  // Get the first embedded wallet address if available
  const walletAddress = user?.linkedAccounts?.find(
    account => account.type === 'wallet'
  )?.address || 'No wallet created yet';

  // Convert email to string safely
  const emailString = user?.email?.toString() || 'User';

  // Return null or a loading state while redirecting
  return null;
} 