import { usePrivy } from '@privy-io/react-auth';
import { WagmiConfig } from 'wagmi';
import { QueryClientProvider } from '@tanstack/react-query';
import styles from '@/styles/Home.module.css';
import { config, queryClient } from '@/config/wagmi';
import { EnsProfile } from '@/components/EnsProfile';
import { TextRecords } from '@/components/TextRecords';

export default function Home() {
  const { login, logout, authenticated, user } = usePrivy();

  // Get the first embedded wallet address if available
  const walletAddress = user?.linkedAccounts?.find(
    account => account.type === 'wallet'
  )?.address || 'No wallet created yet';

  // Convert email to string safely
  const emailString = user?.email?.toString() || 'User';

  return (
    <QueryClientProvider client={queryClient}>
      <WagmiConfig config={config}>
        <div className={styles.container}>
          <main className={styles.main}>
            <title>NeuroTrade.eth</title>
            <h1 className={styles.title}>
              Welcome to NeuroTrade.eth
            </h1>

            {!authenticated ? (
              <button onClick={login} className={styles.button}>
                Login with Email
              </button>
            ) : (
              <div className={styles.userInfo}>
                <h2>Welcome, {emailString}</h2>
                <p>User ID: {user?.id}</p>
                <p>Wallet Address: {walletAddress}</p>
                
                {/* ENS Profile */}
                <div className={styles.ensSection}>
                  <h3>Your ENS Profile</h3>
                  <EnsProfile />
                </div>

                {/* ENS Text Records */}
                <div className={styles.ensSection}>
                  <h3>ENS Text Records</h3>
                  <TextRecords 
                    name="neurotrade.eth"
                    keys={[
                      'ai_agent_version',
                      'supported_chains',
                      'description',
                      'url'
                    ]} 
                  />
                </div>

                <button onClick={logout} className={`${styles.button} ${styles.logoutButton}`}>
                  Logout
                </button>
              </div>
            )}
          </main>
        </div>
      </WagmiConfig>
    </QueryClientProvider>
  );
} 