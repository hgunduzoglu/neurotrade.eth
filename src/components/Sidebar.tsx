import React, { useState } from 'react';
import Link from 'next/link';
import { usePrivy } from '@privy-io/react-auth';
import { FiCopy, FiCheck, FiMenu, FiX } from 'react-icons/fi';
import styles from '../styles/Sidebar.module.css';

const Sidebar = () => {
  const { login, logout, authenticated, user } = usePrivy();
  const [copied, setCopied] = useState(false);
  const [isOpen, setIsOpen] = useState(false);

  const displayAddress = () => {
    const walletAddress = user?.wallet?.address;
    if (walletAddress) {
      const addressStr = String(walletAddress);
      return `${addressStr.slice(0, 6)}...${addressStr.slice(-4)}`;
    }
    if (user?.email) return user.email.toString();
    return '';
  };

  const copyAddress = async () => {
    if (user?.wallet?.address) {
      await navigator.clipboard.writeText(user.wallet.address);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const closeMenu = () => {
    setIsOpen(false);
  };

  return (
    <>
      <button className={styles.menuButton} onClick={toggleMenu}>
        {isOpen ? <FiX size={24} color="white" /> : <FiMenu size={24} color="white" />}
      </button>
      <div className={`${styles.sidebar} ${isOpen ? styles.open : ''}`}>
        <div className={styles.logo}>
          <Link href="/" onClick={closeMenu}>
            NeuroTrade.eth
          </Link>
        </div>
        <nav className={styles.nav}>
          <Link href="/" className={styles.navItem} onClick={closeMenu}>
            <span>New Chat!</span>
          </Link>
          <Link href="http://localhost:8787/api" target="_blank" className={styles.navItem} onClick={closeMenu}>
            <span>Swap</span>
          </Link>
          <Link href="/belongings" className={styles.navItem} onClick={closeMenu}>
            <span>Your Belongings</span>
          </Link>
          <Link href="/analytics" className={styles.navItem} onClick={closeMenu}>
            <span>Analytics</span>
          </Link>
          <Link href="/transactions" className={styles.navItem} onClick={closeMenu}>
            <span>Last Transactions</span>
          </Link>
          <Link href="/settings" className={styles.navItem} onClick={closeMenu}>
            <span>Settings</span>
          </Link>
        </nav>
        <div className={styles.walletSection}>
          {authenticated ? (
            <div className={styles.userContainer}>
              <div 
                className={`${styles.userInfo} ${styles.copyable}`}
                onClick={copyAddress}
                title="Click to copy address"
              >
                <span>{displayAddress()}</span>
                {copied ? (
                  <FiCheck className={styles.copyIcon} style={{ color: '#4CAF50' }} />
                ) : (
                  <FiCopy className={styles.copyIcon} />
                )}
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
    </>
  );
};

export default Sidebar; 