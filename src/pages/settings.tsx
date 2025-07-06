import React, { useState } from 'react';
import { usePrivy } from '@privy-io/react-auth';
import Sidebar from '../components/Sidebar';
import styles from '../styles/Settings.module.css';

type AIMode = 'ai_decide' | 'predefined_rules' | 'user_decide';

const Settings = () => {
  const { authenticated, user, exportWallet } = usePrivy();
  const [selectedAIMode, setSelectedAIMode] = useState<AIMode>('user_decide');
  const [theme, setTheme] = useState('dark');
  const [notifications, setNotifications] = useState(true);
  const [isExporting, setIsExporting] = useState(false);

  const handleAIModeChange = (mode: AIMode) => {
    setSelectedAIMode(mode);
    // Here you would typically save this to your backend or local storage
  };

  const handleThemeChange = (newTheme: string) => {
    setTheme(newTheme);
    // Implement theme change logic
  };

  const handleNotificationsChange = (enable: boolean) => {
    setNotifications(enable);
    // Implement notifications change logic
  };

  const handleExportWallet = async () => {
    try {
      setIsExporting(true);
      // If user has multiple wallets, you can specify which one to export
      // by passing the address: await exportWallet({ address: user?.wallet?.address })
      await exportWallet();
    } catch (error) {
      console.error('Failed to export wallet:', error);
    } finally {
      setIsExporting(false);
    }
  };

  if (!authenticated) {
    return (
      <div className={styles.container}>
        <Sidebar />
        <main className={styles.main}>
          <h1 className={styles.title}>Please connect your wallet to access settings</h1>
        </main>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <Sidebar />
      <main className={styles.main}>
        <h1 className={styles.title}>Settings</h1>

        <section className={styles.section}>
          <h2>AI Trading Mode</h2>
          <div className={styles.optionsGrid}>
            <div
              className={`${styles.option} ${selectedAIMode === 'ai_decide' ? styles.selected : ''}`}
              onClick={() => handleAIModeChange('ai_decide')}
            >
              <h3>AI Decide Mode</h3>
              <p>AI makes trading decisions automatically based on market analysis</p>
            </div>
            <div
              className={`${styles.option} ${selectedAIMode === 'predefined_rules' ? styles.selected : ''}`}
              onClick={() => handleAIModeChange('predefined_rules')}
            >
              <h3>Pre-defined Rules</h3>
              <p>Trading follows strict pre-set rules and conditions</p>
            </div>
            <div
              className={`${styles.option} ${selectedAIMode === 'user_decide' ? styles.selected : ''}`}
              onClick={() => handleAIModeChange('user_decide')}
            >
              <h3>User Decide Mode</h3>
              <p>AI provides suggestions but you make the final decisions</p>
            </div>
          </div>
        </section>

        <section className={styles.section}>
          <h2>Theme</h2>
          <div className={styles.optionsGrid}>
            <div
              className={`${styles.option} ${theme === 'dark' ? styles.selected : ''}`}
              onClick={() => handleThemeChange('dark')}
            >
              <h3>Dark Theme</h3>
              <p>Dark mode for comfortable night trading</p>
            </div>
            <div
              className={`${styles.option} ${theme === 'light' ? styles.selected : ''}`}
              onClick={() => handleThemeChange('light')}
            >
              <h3>Light Theme</h3>
              <p>Light mode for clear visibility</p>
            </div>
          </div>
        </section>

        <section className={styles.section}>
          <h2>Notifications</h2>
          <div className={styles.optionsGrid}>
            <div
              className={`${styles.option} ${notifications ? styles.selected : ''}`}
              onClick={() => handleNotificationsChange(true)}
            >
              <h3>Enable Notifications</h3>
              <p>Receive alerts for important trading events</p>
            </div>
            <div
              className={`${styles.option} ${!notifications ? styles.selected : ''}`}
              onClick={() => handleNotificationsChange(false)}
            >
              <h3>Disable Notifications</h3>
              <p>Turn off trading notifications</p>
            </div>
          </div>
        </section>

        <section className={styles.section}>
          <h2>Wallet Security</h2>
          <div className={styles.walletSection}>
            <div className={styles.warningBox}>
              <h4>⚠️ Important Security Information</h4>
              <p>Exporting your private key means you take full responsibility for its security.</p>
              <p>Never share your private key with anyone. Store it securely offline.</p>
              <p>Anyone with access to your private key has complete control over your wallet.</p>
            </div>
            <button
              className={styles.exportButton}
              onClick={handleExportWallet}
              disabled={isExporting || !user?.wallet}
            >
              {isExporting ? 'Exporting...' : 'Export Private Key'}
            </button>
          </div>
        </section>
      </main>
    </div>
  );
};

export default Settings; 