import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePrivy } from '@privy-io/react-auth';
import { FiCopy, FiCheck, FiMenu, FiX, FiMessageSquare, FiBox, FiBarChart, FiList, FiSettings, FiChevronLeft, FiChevronRight, FiLogOut } from 'react-icons/fi';
import styles from '../styles/Sidebar.module.css';
import Image from 'next/image';
import logo from '../assets/images/logo.png';

const Sidebar = () => {
  const { login, logout, authenticated, user } = usePrivy();
  const [copied, setCopied] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [mounted, setMounted] = useState(false);
  const [isCollapsed, setIsCollapsed] = useState(false);

  useEffect(() => {
    setMounted(true);
    const saved = localStorage.getItem('sidebarCollapsed');
    setIsCollapsed(saved ? JSON.parse(saved) : false);
  }, []);

  useEffect(() => {
    if (mounted) {
      localStorage.setItem('sidebarCollapsed', JSON.stringify(isCollapsed));
    }
  }, [isCollapsed, mounted]);

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

  const toggleCollapse = () => {
    setIsCollapsed(!isCollapsed);
  };

  const closeMenu = () => {
    setIsOpen(false);
  };

  return (
    <>
      <button className={styles.menuButton} onClick={toggleMenu}>
        {isOpen ? <FiX size={24} color="white" /> : <FiMenu size={24} color="white" />}
      </button>
      <div className={`${styles.sidebar} ${isOpen ? styles.open : ''} ${isCollapsed ? styles.collapsed : ''}`}>
        <div className={styles.logo}>
          <Link href="/" onClick={closeMenu}>
            {mounted && isCollapsed ? (
              <div style={{ position: 'relative', width: '32px', height: '32px' }}>
                <Image
                  src={logo}
                  alt="Logo"
                  fill
                  style={{ objectFit: 'contain' }}
                  priority
                />
              </div>
            ) : (
              "NeuroTrade.eth"
            )}
          </Link>
        </div>
        <button className={styles.collapseButton} onClick={toggleCollapse}>
          {isCollapsed ? <FiChevronRight size={20} /> : <FiChevronLeft size={20} />}
        </button>
        <nav className={styles.nav}>
          <Link href="/" className={styles.navItem} onClick={closeMenu} title="New Chat">
            <FiMessageSquare size={20} />
            {!isCollapsed && <span>New Chat!</span>}
          </Link>

          <Link href="http://localhost:8787/api" target="_blank" className={styles.navItem} onClick={closeMenu}>
            <span>Swap</span>
          </Link>
          <Link href="/belongings" className={styles.navItem} onClick={closeMenu}>
            <span>Your Belongings</span
          <Link href="/belongings" className={styles.navItem} onClick={closeMenu} title="Your Belongings">
            <FiBox size={20} />
            {!isCollapsed && <span>Your Belongings</span>}

          </Link>
          <Link href="/analytics" className={styles.navItem} onClick={closeMenu} title="Analytics">
            <FiBarChart size={20} />
            {!isCollapsed && <span>Analytics</span>}
          </Link>
          <Link href="/transactions" className={styles.navItem} onClick={closeMenu} title="Last Transactions">
            <FiList size={20} />
            {!isCollapsed && <span>Last Transactions</span>}
          </Link>
          <Link href="/settings" className={styles.navItem} onClick={closeMenu} title="Settings">
            <FiSettings size={20} />
            {!isCollapsed && <span>Settings</span>}
          </Link>
        </nav>
        <div className={styles.walletSection}>
          {authenticated ? (
            <div className={styles.userContainer}>
              <div 
                className={`${styles.userInfo} ${styles.copyable}`}
                onClick={copyAddress}
                title={isCollapsed ? `Copy address: ${displayAddress()}` : "Click to copy address"}
              >
                {!isCollapsed ? (
                  <>
                    <span>{displayAddress()}</span>
                    {copied ? (
                      <FiCheck className={styles.copyIcon} style={{ color: '#4CAF50' }} />
                    ) : (
                      <FiCopy className={styles.copyIcon} />
                    )}
                  </>
                ) : (
                  copied ? (
                    <FiCheck className={styles.copyIcon} style={{ color: '#4CAF50' }} />
                  ) : (
                    <FiCopy className={styles.copyIcon} />
                  )
                )}
              </div>
              <button 
                onClick={logout} 
                className={styles.logoutButton}
                title={isCollapsed ? "Logout" : undefined}
              >
                {!isCollapsed ? (
                  <>
                    <FiLogOut size={16} />
                    <span>Logout</span>
                  </>
                ) : (
                  <FiLogOut size={16} />
                )}
              </button>
            </div>
          ) : (
            <button 
              onClick={login} 
              className={styles.connectButton}
              title={isCollapsed ? "Connect Wallet" : undefined}
            >
              {!isCollapsed ? (
                <>
                  <FiMenu size={16} />
                  <span>Connect Wallet</span>
                </>
              ) : (
                <FiMenu size={16} />
              )}
            </button>
          )}
        </div>
      </div>
    </>
  );
};

export default Sidebar; 