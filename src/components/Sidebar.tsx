import React from 'react';
import Link from 'next/link';
import { usePrivy } from '@privy-io/react-auth';
import styles from '../styles/Sidebar.module.css';

const Sidebar = () => {
  const { login, logout, authenticated, user } = usePrivy();

  const displayAddress = () => {
    if (user?.email) return user.email.toString();
    if (user?.wallet?.address) {
      return `${user.wallet.address.slice(0, 6)}...${user.wallet.address.slice(-4)}`;
    }
    return '';
  };

  return (
    <div className={styles.sidebar}>
      <div className={styles.logo}>
        <Link href="/">
            NeuroTrade.eth
        </Link>
      </div>
      <nav className={styles.nav}>
        <Link href="/" className={styles.navItem}>
          <span>New Chat!</span>
        </Link>
        <Link href="/belongings" className={styles.navItem}>
          <span>Your Belongings</span>
        </Link>
        <Link href="/transactions" className={styles.navItem}>
          <span>Last Transactions</span>
        </Link>
      </nav>
      <div className={styles.walletSection}>
        {authenticated ? (
          <div className={styles.userContainer}>
            <div className={styles.userInfo}>
              {displayAddress()}
            </div>
            <button onClick={logout} className={styles.logoutButton}>
              Logout
            </button>
          </div>
        ) : (
          <button onClick={login} className={styles.connectButton}>
            Connect Wallet
          </button>
        )}
      </div>
    </div>
  );
};

export default Sidebar; 