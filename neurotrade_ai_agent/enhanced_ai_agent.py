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
        """Generate comprehensive trading response"""
        try:
            if symbols is None:
                symbols = self._extract_symbols_from_query(query)
            
            if not symbols:
                symbols = ["ETH"]  # Default to ETH
            
            # Analyze each symbol
            analyses = {}
            for symbol in symbols:
                analysis = await self.analyze_token(symbol)
                if "error" not in analysis:
                    analyses[symbol] = analysis
            
            if not analyses:
                return "❌ **Error**: Could not analyze any tokens. Please try again later."
            
            # Generate response based on query type
            return self._format_response(query, analyses)
            
        except Exception as e:
            logger.error(f"Error generating trading response: {e}")
            return f"❌ **Error**: Failed to generate analysis - {str(e)}"
    
    def _extract_symbols_from_query(self, query: str) -> List[str]:
        """Extract token symbols from query"""
        query_upper = query.upper()
        found_symbols = []
        
        for symbol in self.supported_tokens:
            if symbol in query_upper:
                found_symbols.append(symbol)
        
        return found_symbols[:3]  # Limit to 3 symbols
    
    def _format_response(self, query: str, analyses: Dict) -> str:
        """Format the response based on query and analyses"""
        query_lower = query.lower()
        
        if len(analyses) == 1:
            symbol = list(analyses.keys())[0]
            analysis = analyses[symbol]
            return self._format_single_token_response(symbol, analysis, query_lower)
        else:
            return self._format_multi_token_response(analyses, query_lower)
    
    def _format_single_token_response(self, symbol: str, analysis: Dict, query_lower: str) -> str:
        """Format response for a single token"""
        price_data = analysis["price_data"]
        technical = analysis["technical_indicators"]
        sentiment = analysis["market_sentiment"]
        signals = analysis["trading_signals"]
        risk = analysis["risk_assessment"]
        recommendations = analysis["recommendations"]
        
        # Header
        response = f"🚀 **NeuroTrade AI - {symbol} Analysis**\n\n"
        
        # Current market data
        response += f"💰 **Price**: ${price_data['price']:,.2f} USD\n"
        response += f"📈 **24h Change**: {price_data['change_24h']:+.2f}%\n"
        response += f"💹 **Volume**: ${price_data['volume_24h']:,.0f}\n"
        response += f"🏆 **Market Cap**: ${price_data['market_cap']:,.0f}\n\n"
        
        # Technical indicators
        response += f"🔧 **Technical Analysis**:\n"
        response += f"• RSI: {technical['rsi']:.1f} ({'Oversold' if technical['rsi'] < 30 else 'Overbought' if technical['rsi'] > 70 else 'Neutral'})\n"
        response += f"• SMA 20: ${technical['sma_20']:.2f}\n"
        response += f"• SMA 50: ${technical['sma_50']:.2f}\n"
        response += f"• Trend Strength: {technical['trend_strength']:.2f}\n"
        response += f"• Volatility: {technical['volatility']:.3f}\n\n"
        
        # Market sentiment
        response += f"🎯 **Sentiment**: {sentiment['label']} "
        response += f"({sentiment['confidence']*100:.0f}% confidence)\n\n"
        
        # Trading signals
        response += f"📊 **Trading Signals**:\n"
        if signals["buy_signal"] > 0.3:
            response += f"🟢 **Buy Signal**: {signals['buy_signal']*100:.0f}%\n"
        if signals["sell_signal"] > 0.3:
            response += f"🔴 **Sell Signal**: {signals['sell_signal']*100:.0f}%\n"
        if signals["hold_signal"] > 0.3:
            response += f"🟡 **Hold Signal**: {signals['hold_signal']*100:.0f}%\n"
        response += f"• Signal Strength: {signals['strength'].title()}\n\n"
        
        # Risk assessment
        response += f"⚠️ **Risk Assessment**: {risk.get('overall_risk', 'medium').title()}\n"
        response += f"• Volatility Risk: {risk.get('volatility_risk', 'medium').title()}\n"
        response += f"• Liquidity Risk: {risk.get('liquidity_risk', 'low').title()}\n\n"
        
        # Recommendations
        if recommendations:
            response += f"💡 **Recommendations**:\n"
            for rec in recommendations:
                response += f"• {rec['action']}: {rec['confidence']}% confidence\n"
                if 'entry_price' in rec:
                    response += f"  Entry: ${rec['entry_price']:.2f}\n"
                if 'stop_loss' in rec:
                    response += f"  Stop Loss: ${rec['stop_loss']:.2f}\n"
                if 'take_profit' in rec:
                    response += f"  Take Profit: ${rec['take_profit']:.2f}\n"
                response += f"  Reasoning: {rec['reasoning']}\n"
        
        # Footer
        response += f"\n---\n"
        response += f"🤖 **NeuroTrade AI** - Advanced Trading Intelligence\n"
        response += f"📊 **Live Data** • 🔍 **Technical Analysis** • 🎯 **Smart Signals**\n"
        response += f"⚡ Generated at {datetime.now().strftime('%H:%M:%S UTC')}"
        
        return response
    
    def _format_multi_token_response(self, analyses: Dict, query_lower: str) -> str:
        """Format response for multiple tokens"""
        response = f"🚀 **NeuroTrade AI - Multi-Token Analysis**\n\n"
        
        for symbol, analysis in analyses.items():
            price_data = analysis["price_data"]
            sentiment = analysis["market_sentiment"]
            signals = analysis["trading_signals"]
            
            response += f"**{symbol}**: ${price_data['price']:,.2f} "
            response += f"({price_data['change_24h']:+.2f}%) "
            response += f"- {sentiment['label']} "
            
            if signals["buy_signal"] > 0.3:
                response += f"🟢 Buy {signals['buy_signal']*100:.0f}%"
            elif signals["sell_signal"] > 0.3:
                response += f"🔴 Sell {signals['sell_signal']*100:.0f}%"
            else:
                response += f"🟡 Hold"
            
            response += f"\n"
        
        response += f"\n💡 **Need detailed analysis?** Ask about specific tokens!\n"
        response += f"🤖 **NeuroTrade AI** - Your Multi-Token Trading Assistant"
        
        return response

# Global instance
enhanced_analyzer = EnhancedTradingAnalyzer() 