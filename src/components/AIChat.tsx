import React, { useState, useEffect, useRef } from 'react';
import { aiService } from '../services/aiService';
import styles from '../styles/AIChat.module.css';

interface Message {
  id: string;
  type: 'user' | 'ai';
  content: string;
  timestamp: Date;
  isLoading?: boolean;
}

interface AIChatProps {
  className?: string;
}

const AIChat: React.FC<AIChatProps> = ({ className }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Welcome message
  const welcomeMessage: Message = {
    id: 'welcome',
    type: 'ai',
    content: `🎉 **Welcome to NeuroTrade AI!**

🚀 I'm your intelligent trading assistant. I can help you with:

💰 **Real-time Price Analysis** - "What's ETH price?"
📊 **Buy/Sell Signals** - "Should I buy BTC?"
🔄 **Swap Analysis** - "Should I swap ETH to USDC?"
📈 **Market Overview** - "Give me a market overview"
🎯 **Portfolio Advice** - "I have 1 ETH and 1000 USDC, what should I do?"

**Try asking me anything about crypto trading!**`,
    timestamp: new Date(),
  };

  // Initialize chat
  useEffect(() => {
    const initializeChat = async () => {
      try {
        console.log('🔄 Initializing AI Chat...');
        
        // Initialize AI service
        const connected = await aiService.initialize();
        setIsConnected(connected);
        
        if (connected) {
          console.log('✅ AI Chat initialized successfully');
          // Add welcome message
          setMessages([welcomeMessage]);
        } else {
          console.warn('⚠️ AI Chat initialization failed');
          setMessages([{
            id: 'error',
            type: 'ai',
            content: `🔌 **Connection Error**: Cannot connect to AI service.

💡 **To start the AI agent**:
1. Open terminal in project root folder
2. Run: \`python start_neurotrade.py\`
3. The HTTP server will start on port 8000
4. The AI agent will run on port 8001

🔄 **Then refresh this page** to connect to the AI agent.`,
            timestamp: new Date(),
          }]);
        }
      } catch (error) {
        console.error('❌ Failed to initialize AI chat:', error);
        setIsConnected(false);
        setMessages([{
          id: 'error',
          type: 'ai',
          content: `❌ **AI Service Error**: ${error instanceof Error ? error.message : 'Unknown error'}

🔧 **Troubleshooting**:
1. Make sure the AI agent is running (check both ports 8000 and 8001)
2. Verify the HTTP server is accessible at http://localhost:8000/health
3. Check the agent's console for any error messages`,
          timestamp: new Date(),
        }]);
      }
    };

    initializeChat();
  }, []);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: `user_${Date.now()}`,
      type: 'user',
      content: inputValue.trim(),
      timestamp: new Date(),
    };

    const loadingMessage: Message = {
      id: `loading_${Date.now()}`,
      type: 'ai',
      content: '🤔 Analyzing market data...',
      timestamp: new Date(),
      isLoading: true,
    };

    // Add user message and loading indicator
    setMessages(prev => [...prev, userMessage, loadingMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Send message to AI agent
      const response = await aiService.quickTradingQuery(userMessage.content);
      
      // Remove loading message and add AI response
      setMessages(prev => [
        ...prev.filter(msg => !msg.isLoading),
        {
          id: `ai_${Date.now()}`,
          type: 'ai',
          content: response,
          timestamp: new Date(),
        }
      ]);
    } catch (error) {
      console.error('Failed to get AI response:', error);
      
      // Remove loading message and add error message
      setMessages(prev => [
        ...prev.filter(msg => !msg.isLoading),
        {
          id: `error_${Date.now()}`,
          type: 'ai',
          content: '❌ Sorry, I encountered an error. Please try again.',
          timestamp: new Date(),
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const formatMessage = (content: string) => {
    // Convert markdown-style formatting to HTML
    return content
      .split('\n')
      .map((line, index) => {
        if (line.startsWith('**') && line.endsWith('**')) {
          return <strong key={index}>{line.slice(2, -2)}</strong>;
        }
        if (line.startsWith('• ')) {
          return <li key={index}>{line.slice(2)}</li>;
        }
        if (line.startsWith('---')) {
          return <hr key={index} />;
        }
        return <div key={index}>{line || <br />}</div>;
      });
  };

  const quickQuestions = [
    "What's ETH price?",
    "Should I buy BTC?",
    "Market overview",
    "ETH vs BTC analysis",
  ];

  const handleQuickQuestion = (question: string) => {
    setInputValue(question);
  };

  return (
    <div className={`${styles.chatContainer} ${className || ''}`}>
      {/* Connection Status */}
      <div className={styles.statusBar}>
        <div className={`${styles.status} ${isConnected ? styles.connected : styles.disconnected}`}>
          <span className={styles.statusDot}></span>
          {isConnected ? 'AI Agent Connected' : 'AI Agent Disconnected'}
        </div>
      </div>

      {/* Messages */}
      <div className={styles.messagesContainer}>
        {messages.map((message) => (
          <div
            key={message.id}
            className={`${styles.message} ${
              message.type === 'user' ? styles.userMessage : styles.aiMessage
            } ${message.isLoading ? styles.loading : ''}`}
          >
            <div className={styles.messageContent}>
              {message.type === 'ai' && (
                <div className={styles.aiAvatar}>🤖</div>
              )}
              <div className={styles.messageText}>
                {message.isLoading ? (
                  <div className={styles.loadingDots}>
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                ) : (
                  formatMessage(message.content)
                )}
              </div>
              {message.type === 'user' && (
                <div className={styles.userAvatar}>👤</div>
              )}
            </div>
            <div className={styles.timestamp}>
              {message.timestamp.toLocaleTimeString()}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Questions */}
      {messages.length <= 1 && (
        <div className={styles.quickQuestions}>
          <div className={styles.quickQuestionsTitle}>Try asking:</div>
          <div className={styles.questionButtons}>
            {quickQuestions.map((question, index) => (
              <button
                key={index}
                className={styles.questionButton}
                onClick={() => handleQuickQuestion(question)}
                disabled={isLoading}
              >
                {question}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input */}
      <div className={styles.inputContainer}>
        <input
          ref={inputRef}
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={
            isConnected 
              ? "Ask me about crypto trading..." 
              : "Connecting to AI agent..."
          }
          className={styles.input}
          disabled={!isConnected || isLoading}
        />
        <button
          onClick={sendMessage}
          disabled={!inputValue.trim() || !isConnected || isLoading}
          className={styles.sendButton}
        >
          {isLoading ? '⌛' : '🚀'}
        </button>
      </div>
    </div>
  );
};

export default AIChat; 