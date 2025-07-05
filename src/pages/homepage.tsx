import React from 'react';
import Head from 'next/head';
import Sidebar from '../components/Sidebar';
import TypewriterInput from '../components/TypewriterInput';
import styles from '../styles/Homepage.module.css';

const Homepage = () => {
  return (
    <>
      <Head>
        <title>NeuroTrade.eth - AI Trading Assistant</title>
        <meta name="description" content="Your AI-powered crypto trading assistant" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className={styles.container}>
        <Sidebar />
        
        <main className={styles.main}>
          <div className={styles.chatSection}>
            <div className={styles.chatContainer}>
              <h1>How can I help you?</h1>
              <div className={styles.inputContainer}>
                <TypewriterInput 
                  text="What is the best move for this week?"
                  className={styles.chatInput}
                />
              </div>
              <div className={styles.todoNote}>
                TODO: AI Agent Integration Coming Soon
              </div>
            </div>
          </div>
        </main>
      </div>
    </>
  );
};

export default Homepage; 