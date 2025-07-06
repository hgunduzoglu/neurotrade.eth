/**
 * AI Service for NeuroTrade Frontend
 * 
 * This service provides methods to communicate with the AI agent
 * through its HTTP endpoints for trading analysis and chat functionality.
 */

interface ChatRequest {
  message: string;
  symbols?: string[];
  user_id?: string;
}

interface ChatResponse {
  response: string;
  timestamp: string;
  symbols_analyzed: string[];
  analysis_type: string;
  success: boolean;
  error?: string;
}

interface TokenAnalysisResponse {
  symbol: string;
  analysis: any;
  timestamp: string;
  success: boolean;
  error?: string;
}

interface HealthResponse {
  status: string;
  timestamp: string;
  version: string;
}

class AIService {
  private baseUrl: string;
  private sessionId: string;
  private isConnected: boolean = false;

  constructor() {
    // Use the AI agent's HTTP server URL
    this.baseUrl = process.env.NEXT_PUBLIC_AI_API_URL || 'http://localhost:8000';
    this.sessionId = this.generateSessionId();
    console.log('🤖 AI Service initialized with URL:', this.baseUrl);
  }

  private generateSessionId(): string {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  private async makeRequest<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    try {
      const url = `${this.baseUrl}${endpoint}`;
      console.log(`🔄 Making request to: ${url}`);

      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        const errorText = await response.text().catch(() => 'Unknown error');
        console.error(`❌ HTTP ${response.status}: ${errorText}`);
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log(`✅ Response received:`, data);
      return data;
    } catch (error) {
      console.error(`❌ AI Service request failed:`, error);
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error('Cannot connect to AI service. Please make sure the AI agent is running on port 8000.');
      }
      throw error;
    }
  }

  /**
   * Initialize the AI service and check connection
   */
  async initialize(): Promise<boolean> {
    try {
      console.log('🔄 Initializing AI Service...');
      const health = await this.checkHealth();
      this.isConnected = health.status === 'healthy';
      
      if (this.isConnected) {
        console.log('✅ AI Service connected successfully');
      } else {
        console.warn('⚠️ AI Service health check failed');
      }
      
      return this.isConnected;
    } catch (error) {
      console.error('❌ AI Service initialization failed:', error);
      this.isConnected = false;
      return false;
    }
  }

  /**
   * Check if the AI service is healthy
   */
  async checkHealth(): Promise<HealthResponse> {
    return this.makeRequest<HealthResponse>('/health');
  }

  /**
   * Check if the service is connected
   */
  isServiceConnected(): boolean {
    return this.isConnected;
  }

  /**
   * Send a chat message to the AI agent
   */
  async sendChatMessage(request: ChatRequest): Promise<ChatResponse> {
    if (!this.isConnected) {
      console.warn('⚠️ AI Service not connected, attempting to reconnect...');
      await this.initialize();
    }

    return this.makeRequest<ChatResponse>('/chat', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * Get detailed analysis for a specific token
   */
  async analyzeToken(symbol: string): Promise<TokenAnalysisResponse> {
    if (!this.isConnected) {
      console.warn('⚠️ AI Service not connected, attempting to reconnect...');
      await this.initialize();
    }

    return this.makeRequest<TokenAnalysisResponse>(`/analyze/${symbol.toUpperCase()}`, {
      method: 'POST',
    });
  }

  /**
   * Get list of supported tokens
   */
  async getSupportedTokens(): Promise<{ tokens: string[]; count: number; timestamp: string }> {
    return this.makeRequest('/supported-tokens');
  }

  /**
   * Analyze multiple tokens at once
   */
  async batchAnalyzeTokens(symbols: string[]): Promise<any> {
    return this.makeRequest('/batch-analyze', {
      method: 'POST',
      body: JSON.stringify(symbols),
    });
  }

  /**
   * Start a new chat session
   */
  async startSession(userId?: string): Promise<any> {
    return this.makeRequest(`/session/${this.sessionId}/start`, {
      method: 'POST',
      body: JSON.stringify({ user_id: userId }),
    });
  }

  /**
   * End the current chat session
   */
  async endSession(): Promise<any> {
    return this.makeRequest(`/session/${this.sessionId}/end`, {
      method: 'POST',
    });
  }

  /**
   * Get current session info
   */
  async getSessionInfo(): Promise<any> {
    return this.makeRequest(`/session/${this.sessionId}`);
  }

  /**
   * Send a quick trading query (simplified interface)
   */
  async quickTradingQuery(query: string, symbols?: string[]): Promise<string> {
    try {
      const response = await this.sendChatMessage({
        message: query,
        symbols,
        user_id: 'frontend_user',
      });

      if (response.success) {
        return response.response;
      } else {
        throw new Error(response.error || 'Unknown error occurred');
      }
    } catch (error) {
      console.error('Quick trading query failed:', error);
      
      if (error instanceof Error && error.message.includes('Cannot connect')) {
        return '🔌 **Connection Error**: Cannot connect to AI service. Please make sure the AI agent is running.\n\n' +
               '💡 **To start the agent**: Run `python start_neurotrade.py` in the project root folder.';
      }
      
      return '❌ Sorry, I encountered an error processing your request. Please try again.';
    }
  }

  /**
   * Get price analysis for a token
   */
  async getPriceAnalysis(symbol: string): Promise<string> {
    return this.quickTradingQuery(`What's the price analysis for ${symbol}?`, [symbol]);
  }

  /**
   * Get buy recommendation for a token
   */
  async getBuyRecommendation(symbol: string): Promise<string> {
    return this.quickTradingQuery(`Should I buy ${symbol}?`, [symbol]);
  }

  /**
   * Get sell recommendation for a token
   */
  async getSellRecommendation(symbol: string): Promise<string> {
    return this.quickTradingQuery(`Should I sell ${symbol}?`, [symbol]);
  }

  /**
   * Get swap analysis for tokens
   */
  async getSwapAnalysis(fromToken: string, toToken: string): Promise<string> {
    return this.quickTradingQuery(
      `Should I swap ${fromToken} to ${toToken}?`,
      [fromToken, toToken]
    );
  }

  /**
   * Get market overview
   */
  async getMarketOverview(): Promise<string> {
    return this.quickTradingQuery('Give me a market overview');
  }

  /**
   * Get portfolio recommendation
   */
  async getPortfolioRecommendation(holdings: Array<{ symbol: string; amount: number }>): Promise<string> {
    const holdingsText = holdings.map(h => `${h.amount} ${h.symbol}`).join(', ');
    return this.quickTradingQuery(`Analyze my portfolio: ${holdingsText}`);
  }

  /**
   * Get trading signals
   */
  async getTradingSignals(symbol: string): Promise<string> {
    return this.quickTradingQuery(`What are the trading signals for ${symbol}?`, [symbol]);
  }

  /**
   * Get risk assessment
   */
  async getRiskAssessment(symbol: string): Promise<string> {
    return this.quickTradingQuery(`What's the risk assessment for ${symbol}?`, [symbol]);
  }
}

// Export a singleton instance
export const aiService = new AIService();
export default aiService;

// Export types for use in components
export type {
  ChatRequest,
  ChatResponse,
  TokenAnalysisResponse,
  HealthResponse,
}; 