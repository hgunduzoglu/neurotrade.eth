import { PrivyProvider } from '@/providers/PrivyProvider';
import type { AppProps } from 'next/app';
import { Navbar } from '@/components/Navbar';

export default function App({ Component, pageProps }: AppProps) {
  return (
    <PrivyProvider>
      <Navbar />
      <Component {...pageProps} />
    </PrivyProvider>
  );
} 