"""
Enhanced NeuroTrade AI Agent

This enhanced version includes:
- Comprehensive market data analysis
- Historical data and technical indicators
- Multi-token support
- Sophisticated trading recommendations
- Integration with frontend data sources
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import asdict

# Import the enhanced data service
from enhanced_data_service import data_service, PriceData, TechnicalIndicators, MarketSentiment

logger = logging.getLogger(__name__)

class EnhancedTradingAnalyzer:
    """Enhanced trading analyzer with sophisticated analysis capabilities"""
    
    def __init__(self):
        self.data_service = data_service
        self.supported_tokens = [
            "BTC", "ETH", "USDC", "USDT", "BNB", "SOL", "ADA", "DOT", 
            "MATIC", "UNI", "LINK", "AVAX", "LTC", "XRP", "DOGE"
        ]
    
    async def analyze_token(self, symbol: str) -> Dict:
        """Perform comprehensive token analysis"""
        try:
            # Get comprehensive analysis from data service
            analysis = await self.data_service.get_comprehensive_analysis(symbol.upper())
            
            if "error" in analysis:
                return analysis
            
            # Add our enhanced analysis
            enhanced_analysis = analysis.copy()
            enhanced_analysis["trading_signals"] = self._generate_trading_signals(analysis)
            enhanced_analysis["risk_assessment"] = self._assess_risk(analysis)
            # Pass enhanced analysis to generate_recommendations so it has access to all computed values
            enhanced_analysis["recommendations"] = self._generate_recommendations(enhanced_analysis)
            
            return enhanced_analysis
            
        except Exception as e:
            logger.error(f"Error in token analysis for {symbol}: {e}")
            return {"error": f"Analysis failed for {symbol}: {str(e)}"}
    
    def _generate_trading_signals(self, analysis: Dict) -> Dict:
        """Generate trading signals based on analysis"""
        signals = {
            "buy_signal": 0,    # -1 to 1
            "sell_signal": 0,   # -1 to 1
            "hold_signal": 0,   # -1 to 1
            "strength": "weak"  # weak, moderate, strong
        }
        
        price_data = analysis["price_data"]
        technical = analysis["technical_indicators"]
        sentiment = analysis["market_sentiment"]
        
        # Price momentum signal
        if price_data["change_24h"] > 5:
            signals["buy_signal"] += 0.3
        elif price_data["change_24h"] < -5:
            signals["sell_signal"] += 0.3
        
        # RSI signals
        if technical["rsi"] < 30:  # Oversold
            signals["buy_signal"] += 0.4
        elif technical["rsi"] > 70:  # Overbought
            signals["sell_signal"] += 0.4
        else:
            signals["hold_signal"] += 0.2
        
        # Moving average signals
        current_price = price_data["price"]
        if technical["sma_20"] > 0 and technical["sma_50"] > 0:
            if current_price > technical["sma_20"] > technical["sma_50"]:
                signals["buy_signal"] += 0.2
            elif current_price < technical["sma_20"] < technical["sma_50"]:
                signals["sell_signal"] += 0.2
        
        # Trend strength signals
        if technical["trend_strength"] > 0.5:
            signals["buy_signal"] += 0.2
        elif technical["trend_strength"] < -0.5:
            signals["sell_signal"] += 0.2
        
        # Volume confirmation
        if price_data["volume_24h"] > 1000000000:  # High volume
            # Amplify existing signals
            if signals["buy_signal"] > signals["sell_signal"]:
                signals["buy_signal"] += 0.1
            elif signals["sell_signal"] > signals["buy_signal"]:
                signals["sell_signal"] += 0.1
        
        # Normalize signals
        total_signal = abs(signals["buy_signal"]) + abs(signals["sell_signal"]) + abs(signals["hold_signal"])
        if total_signal > 0:
            signals["buy_signal"] /= total_signal
            signals["sell_signal"] /= total_signal
            signals["hold_signal"] /= total_signal
        
        # Determine strength
        max_signal = max(abs(signals["buy_signal"]), abs(signals["sell_signal"]), abs(signals["hold_signal"]))
        if max_signal > 0.6:
            signals["strength"] = "strong"
        elif max_signal > 0.3:
            signals["strength"] = "moderate"
        else:
            signals["strength"] = "weak"
        
        return signals
    
    def _assess_risk(self, analysis: Dict) -> Dict:
        """Assess risk levels"""
        risk_assessment = {
            "overall_risk": "medium",
            "volatility_risk": "medium",
            "liquidity_risk": "low",
            "market_risk": "medium",
            "score": 0.5  # 0 to 1
        }
        
        price_data = analysis["price_data"]
        technical = analysis["technical_indicators"]
        
        risk_factors = []
        
        # Volatility risk
        if technical["volatility"] > 0.1:
            risk_factors.append(0.3)
            risk_assessment["volatility_risk"] = "high"
        elif technical["volatility"] > 0.05:
            risk_factors.append(0.1)
            risk_assessment["volatility_risk"] = "medium"
        else:
            risk_factors.append(0.0)
            risk_assessment["volatility_risk"] = "low"
        
        # Liquidity risk
        if price_data["volume_24h"] < 100000000:  # Low volume
            risk_factors.append(0.2)
            risk_assessment["liquidity_risk"] = "high"
        elif price_data["volume_24h"] < 1000000000:
            risk_factors.append(0.1)
            risk_assessment["liquidity_risk"] = "medium"
        else:
            risk_factors.append(0.0)
            risk_assessment["liquidity_risk"] = "low"
        
        # Market cap risk
        if price_data["market_cap"] < 1000000000:  # Small cap
            risk_factors.append(0.3)
        elif price_data["market_cap"] < 10000000000:  # Mid cap
            risk_factors.append(0.1)
        else:  # Large cap
            risk_factors.append(0.0)
        
        # RSI extremes
        if technical["rsi"] > 80 or technical["rsi"] < 20:
            risk_factors.append(0.2)
        else:
            risk_factors.append(0.0)
        
        # Calculate overall risk score
        risk_score = sum(risk_factors) / len(risk_factors)
        risk_assessment["score"] = risk_score
        
        if risk_score > 0.6:
            risk_assessment["overall_risk"] = "high"
            risk_assessment["market_risk"] = "high"
        elif risk_score > 0.3:
            risk_assessment["overall_risk"] = "medium"
            risk_assessment["market_risk"] = "medium"
        else:
            risk_assessment["overall_risk"] = "low"
            risk_assessment["market_risk"] = "low"
        
        return risk_assessment
    
    def _generate_recommendations(self, analysis: Dict) -> List[Dict]:
        """Generate specific trading recommendations"""
        recommendations = []
        
        price_data = analysis["price_data"]
        technical = analysis["technical_indicators"]
        sentiment = analysis["market_sentiment"]
        signals = analysis.get("trading_signals", {})
        risk = analysis.get("risk_assessment", {})
        
        current_price = price_data["price"]
        
        # Buy recommendations
        if signals.get("buy_signal", 0) > 0.4:
            recommendations.append({
                "action": "BUY",
                "confidence": min(100, int(signals["buy_signal"] * 100)),
                "entry_price": current_price,
                "stop_loss": current_price * 0.92,
                "take_profit": current_price * 1.15,
                "reasoning": f"Strong buy signal detected. RSI: {technical['rsi']:.1f}, Trend: {technical['trend_strength']:.2f}"
            })
        
        # Sell recommendations
        if signals.get("sell_signal", 0) > 0.4:
            risk_level = risk.get("overall_risk", "medium")
            recommendations.append({
                "action": "SELL",
                "confidence": min(100, int(signals["sell_signal"] * 100)),
                "exit_price": current_price,
                "reasoning": f"Strong sell signal detected. RSI: {technical['rsi']:.1f}, Risk: {risk_level}"
            })
        
        # Hold recommendations
        if signals.get("hold_signal", 0) > 0.3:
            recommendations.append({
                "action": "HOLD",
                "confidence": min(100, int(signals["hold_signal"] * 100)),
                "reasoning": f"Market consolidation detected. Wait for clearer signals."
            })
        
        # Risk-based recommendations
        if risk.get("overall_risk", "medium") == "high":
            recommendations.append({
                "action": "REDUCE_POSITION",
                "confidence": 70,
                "reasoning": f"High risk detected. Consider reducing position size."
            })
        
        # DCA recommendations
        if technical["trend_strength"] > 0.3 and signals.get("buy_signal", 0) > 0.2:
            recommendations.append({
                "action": "DCA_BUY",
                "confidence": 60,
                "reasoning": f"Positive trend detected. Consider dollar-cost averaging."
            })
        
        return recommendations
    
    async def generate_trading_response(self, query: str, symbols: List[str] = None) -> str:
        """Generate a comprehensive trading response"""
        try:
            query_lower = query.lower()
            
            # Extract symbols if not provided
            if not symbols:
                symbols = self._extract_symbols_from_query(query)
            
            if not symbols:
                # Try to detect intent for default symbols
                if "market" in query_lower or "overview" in query_lower:
                    symbols = ["ETH", "BTC"]  # Default to major coins
                elif "price" in query_lower:
                    symbols = ["ETH"]  # Default to ETH
                else:
                    symbols = ["ETH"]  # Fallback
            
            # Get analysis for each symbol
            analyses = {}
            for symbol in symbols:
                if symbol in self.supported_tokens:
                    analysis = await self.analyze_token(symbol)
                    if "error" not in analysis:
                        analyses[symbol] = analysis
            
            if not analyses:
                return "I apologize, but I couldn't analyze any of the requested tokens. Please try again with supported tokens like ETH, BTC, etc."
            
            # Format response based on query type
            if len(analyses) == 1:
                # Single token analysis
                symbol = list(analyses.keys())[0]
                return self._format_single_token_response(symbol, analyses[symbol], query_lower)
            else:
                # Multi-token analysis
                return self._format_multi_token_response(analyses, query_lower)
                
        except Exception as e:
            logger.error(f"Error generating trading response: {e}")
            return "I encountered an error while analyzing the market. Please try again in a moment."
            
    def _extract_symbols_from_query(self, query: str) -> List[str]:
        """Extract token symbols from query"""
        query_upper = query.upper()
        found_symbols = []
        
        for symbol in self.supported_tokens:
            if symbol in query_upper:
                found_symbols.append(symbol)
        
        return found_symbols[:3]  # Limit to 3 symbols
    
    def _format_single_token_response(self, symbol: str, analysis: Dict, query_lower: str) -> str:
        """Format response for single token analysis"""
        try:
            price_data = analysis["price_data"]
            technical = analysis["technical_indicators"]
            sentiment = analysis["market_sentiment"]
            signals = analysis["trading_signals"]
            risk = analysis["risk_assessment"]
            
            # Price query
            if "price" in query_lower or "what" in query_lower and f"{symbol.lower()}" in query_lower:
                return f"""💰 **{symbol} Price Analysis**:
• Current Price: ${price_data['price']:,.2f} USD
• 24h Change: {price_data['change_24h']:+.2f}%
• Volume: ${price_data['volume_24h']:,.0f}
• Market Cap: ${price_data['market_cap']:,.0f}

📊 **Technical Indicators**:
• RSI: {technical['rsi']:.1f}
• Trend: {technical['trend_strength']:+.2f}
• Volatility: {technical['volatility']:.3f}"""
            
            # Market overview
            elif "market" in query_lower or "overview" in query_lower:
                return f"""🌍 **{symbol} Market Overview**:
• Price: ${price_data['price']:,.2f}
• Market Sentiment: {sentiment['label']}
• Confidence: {sentiment['confidence']*100:.1f}%
• 24h Performance: {price_data['change_24h']:+.2f}%
• Trading Volume: ${price_data['volume_24h']:,.0f}

📈 **Market Analysis**:
• Trend Strength: {technical['trend_strength']:+.2f}
• Risk Level: {risk['overall_risk'].title()}
• Volatility: {technical['volatility']:.3f}"""
            
            # Trading analysis (buy/sell/trade)
            elif any(word in query_lower for word in ["buy", "sell", "trade", "swap"]):
                action = "BUY" if signals['buy_signal'] > signals['sell_signal'] else "SELL" if signals['sell_signal'] > signals['buy_signal'] else "HOLD"
                confidence = signals['strength'].title()
                
                return f"""📊 **{symbol} Trading Analysis**:
• Current Price: ${price_data['price']:,.2f}
• Market Sentiment: {sentiment['label']}
• Signal Strength: {confidence}

🎯 **Recommendation**: {action}
• Buy Signal: {signals['buy_signal']*100:.1f}%
• Sell Signal: {signals['sell_signal']*100:.1f}%
• Risk Level: {risk['overall_risk'].title()}

⚠️ **Risk Assessment**:
• Volatility Risk: {risk['volatility_risk'].title()}
• Market Risk: {risk['market_risk'].title()}
• Overall Score: {risk['score']*100:.1f}%"""
            
            # Default comprehensive analysis
            else:
                return f"""📈 **{symbol} Comprehensive Analysis**:
• Price: ${price_data['price']:,.2f} ({price_data['change_24h']:+.2f}%)
• Market Sentiment: {sentiment['label']} ({sentiment['confidence']*100:.1f}% confidence)
• Risk Level: {risk['overall_risk'].title()}

🔍 **Key Indicators**:
• RSI: {technical['rsi']:.1f}
• Trend Strength: {technical['trend_strength']:+.2f}
• Volatility: {technical['volatility']:.3f}

💡 **Trading Signals**:
• Primary Signal: {"BUY" if signals['buy_signal'] > signals['sell_signal'] else "SELL"}
• Signal Strength: {signals['strength'].title()}
• Risk Score: {risk['score']*100:.1f}%"""
                
        except Exception as e:
            logger.error(f"Error formatting single token response: {e}")
            return f"Sorry, I encountered an error while analyzing {symbol}. Please try again."
            
    def _format_multi_token_response(self, analyses: Dict, query_lower: str) -> str:
        """Format response for multiple token analysis"""
        try:
            responses = []
            
            # Price comparison
            if "price" in query_lower or "compare" in query_lower:
                for symbol, analysis in analyses.items():
                    price_data = analysis["price_data"]
                    responses.append(f"""💰 **{symbol}**:
• Price: ${price_data['price']:,.2f}
• 24h Change: {price_data['change_24h']:+.2f}%
• Volume: ${price_data['volume_24h']:,.0f}""")
                    
            # Market overview
            elif "market" in query_lower or "overview" in query_lower:
                for symbol, analysis in analyses.items():
                    price_data = analysis["price_data"]
                    sentiment = analysis["market_sentiment"]
                    risk = analysis["risk_assessment"]
                    responses.append(f"""🌍 **{symbol} Overview**:
• Price: ${price_data['price']:,.2f} ({price_data['change_24h']:+.2f}%)
• Sentiment: {sentiment['label']}
• Risk: {risk['overall_risk'].title()}""")
                    
            # Trading analysis
            elif any(word in query_lower for word in ["buy", "sell", "trade"]):
                for symbol, analysis in analyses.items():
                    signals = analysis["trading_signals"]
                    risk = analysis["risk_assessment"]
                    action = "BUY" if signals['buy_signal'] > signals['sell_signal'] else "SELL" if signals['sell_signal'] > signals['buy_signal'] else "HOLD"
                    responses.append(f"""📊 **{symbol}**:
• Action: {action}
• Strength: {signals['strength'].title()}
• Risk: {risk['overall_risk'].title()}""")
                    
            # Default comparison
            else:
                for symbol, analysis in analyses.items():
                    price_data = analysis["price_data"]
                    sentiment = analysis["market_sentiment"]
                    signals = analysis["trading_signals"]
                    responses.append(f"""📈 **{symbol}**:
• Price: ${price_data['price']:,.2f} ({price_data['change_24h']:+.2f}%)
• Signal: {"BUY" if signals['buy_signal'] > signals['sell_signal'] else "SELL"}
• Sentiment: {sentiment['label']}""")
            
            return "\n\n".join(responses)
            
        except Exception as e:
            logger.error(f"Error formatting multi-token response: {e}")
            return "Sorry, I encountered an error while comparing the tokens. Please try again."

# Global instance
enhanced_analyzer = EnhancedTradingAnalyzer() 