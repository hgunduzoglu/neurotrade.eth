import { useRouter } from 'next/router';
import Link from 'next/link';
import styles from '@/styles/Navbar.module.css';
import { usePrivy } from '@privy-io/react-auth';

export const Navbar = () => {
  const router = useRouter();
  const { authenticated } = usePrivy();

  return (
    <nav className={styles.navbar}>
      <div className={styles.logo}>
        NeuroTrade.eth
      </div>
      <div className={styles.links}>
        <Link 
          href="/" 
          className={`${styles.link} ${router.pathname === '/' ? styles.active : ''}`}
        >
          Home
        </Link>
        {authenticated && (
          <Link 
            href="/swap" 
            className={`${styles.link} ${router.pathname === '/swap' ? styles.active : ''}`}
          >
            Swap
          </Link>
        )}
      </div>
    </nav>
  );
}; 