"""
Enhanced Data Service for NeuroTrade AI Agent

This service provides comprehensive market data including:
- Real-time price feeds (using CryptoCompare API like frontend)
- Historical data for trend analysis
- Multi-token support
- Technical indicators
- Market sentiment analysis
"""

import aiohttp
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
from dataclasses import dataclass
import json

logger = logging.getLogger(__name__)

@dataclass
class PriceData:
    """Mirror of frontend PriceData interface"""
    PRICE: float
    CHANGEPCT24HOUR: float
    VOLUME24HOUR: float
    MKTCAP: float

@dataclass
class HistoricalDataPoint:
    """Historical price data point"""
    timestamp: int
    close: float
    high: float
    low: float
    open: float
    volume: float

@dataclass
class TechnicalIndicators:
    """Technical analysis indicators"""
    rsi: float
    sma_20: float
    sma_50: float
    volatility: float
    momentum: float
    trend_strength: float

@dataclass
class MarketSentiment:
    """Market sentiment analysis"""
    score: float  # -1 to 1
    label: str   # "Bullish", "Bearish", "Neutral"
    confidence: float  # 0 to 1

class EnhancedDataService:
    """Enhanced data service for AI agent"""
    
    def __init__(self):
        self.cache = {}
        self.cache_timeout = 300  # 5 minutes
        self.historical_cache = {}
        self.historical_cache_timeout = 3600  # 1 hour
        
    async def fetch_token_price(self, symbol: str) -> Optional[PriceData]:
        """Fetch token price using CryptoCompare API (same as frontend)"""
        try:
            # Check cache first
            cache_key = f"price_{symbol}"
            if cache_key in self.cache:
                cached_data, timestamp = self.cache[cache_key]
                if datetime.now().timestamp() - timestamp < self.cache_timeout:
                    return cached_data
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={symbol}&tsyms=USD",
                    headers={'accept': 'application/json'}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if data.get('RAW') and data['RAW'].get(symbol) and data['RAW'][symbol].get('USD'):
                            usd_data = data['RAW'][symbol]['USD']
                            
                            price_data = PriceData(
                                PRICE=usd_data.get('PRICE', 0),
                                CHANGEPCT24HOUR=usd_data.get('CHANGEPCT24HOUR', 0),
                                VOLUME24HOUR=usd_data.get('VOLUME24HOUR', 0),
                                MKTCAP=usd_data.get('MKTCAP', 0)
                            )
                            
                            # Cache the result
                            self.cache[cache_key] = (price_data, datetime.now().timestamp())
                            return price_data
                    
                    return None
                    
        except Exception as e:
            logger.error(f"Error fetching price for {symbol}: {e}")
            return None
    
    async def fetch_multiple_token_prices(self, symbols: List[str]) -> Dict[str, Optional[PriceData]]:
        """Fetch multiple token prices (same as frontend)"""
        try:
            symbols_string = ','.join(symbols)
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={symbols_string}&tsyms=USD",
                    headers={'accept': 'application/json'}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        prices = {}
                        
                        for symbol in symbols:
                            if (data.get('RAW') and 
                                data['RAW'].get(symbol) and 
                                data['RAW'][symbol].get('USD')):
                                
                                usd_data = data['RAW'][symbol]['USD']
                                prices[symbol] = PriceData(
                                    PRICE=usd_data.get('PRICE', 0),
                                    CHANGEPCT24HOUR=usd_data.get('CHANGEPCT24HOUR', 0),
                                    VOLUME24HOUR=usd_data.get('VOLUME24HOUR', 0),
                                    MKTCAP=usd_data.get('MKTCAP', 0)
                                )
                            else:
                                prices[symbol] = None
                        
                        return prices
                    
                    return {symbol: None for symbol in symbols}
                    
        except Exception as e:
            logger.error(f"Error fetching multiple prices: {e}")
            return {symbol: None for symbol in symbols}
    
    async def fetch_historical_data(self, symbol: str, days: int = 30) -> List[HistoricalDataPoint]:
        """Fetch historical price data for technical analysis"""
        try:
            # Check cache first
            cache_key = f"historical_{symbol}_{days}"
            if cache_key in self.historical_cache:
                cached_data, timestamp = self.historical_cache[cache_key]
                if datetime.now().timestamp() - timestamp < self.historical_cache_timeout:
                    return cached_data
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://min-api.cryptocompare.com/data/v2/histoday?fsym={symbol}&tsym=USD&limit={days}",
                    headers={'accept': 'application/json'}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if data.get('Data') and data['Data'].get('Data'):
                            historical_data = []
                            for point in data['Data']['Data']:
                                historical_data.append(HistoricalDataPoint(
                                    timestamp=point['time'],
                                    close=point['close'],
                                    high=point['high'],
                                    low=point['low'],
                                    open=point['open'],
                                    volume=point['volumeto']
                                ))
                            
                            # Cache the result
                            self.historical_cache[cache_key] = (historical_data, datetime.now().timestamp())
                            return historical_data
                    
                    return []
                    
        except Exception as e:
            logger.error(f"Error fetching historical data for {symbol}: {e}")
            return []
    
    def calculate_technical_indicators(self, historical_data: List[HistoricalDataPoint]) -> TechnicalIndicators:
        """Calculate technical indicators from historical data"""
        if len(historical_data) < 20:
            return TechnicalIndicators(0, 0, 0, 0, 0, 0)
        
        prices = [point.close for point in historical_data]
        
        # RSI calculation
        rsi = self._calculate_rsi(prices)
        
        # Simple Moving Averages
        sma_20 = sum(prices[-20:]) / 20 if len(prices) >= 20 else 0
        sma_50 = sum(prices[-50:]) / 50 if len(prices) >= 50 else 0
        
        # Volatility (standard deviation of last 20 days)
        if len(prices) >= 20:
            recent_prices = prices[-20:]
            avg_price = sum(recent_prices) / len(recent_prices)
            volatility = (sum((p - avg_price) ** 2 for p in recent_prices) / len(recent_prices)) ** 0.5
        else:
            volatility = 0
        
        # Momentum (price change over last 14 days)
        momentum = ((prices[-1] - prices[-14]) / prices[-14]) * 100 if len(prices) >= 14 else 0
        
        # Trend strength (correlation with time)
        trend_strength = self._calculate_trend_strength(prices[-20:] if len(prices) >= 20 else prices)
        
        return TechnicalIndicators(
            rsi=rsi,
            sma_20=sma_20,
            sma_50=sma_50,
            volatility=volatility,
            momentum=momentum,
            trend_strength=trend_strength
        )
    
    def _calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """Calculate RSI (Relative Strength Index)"""
        if len(prices) < period + 1:
            return 50.0  # Neutral RSI
        
        gains = []
        losses = []
        
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        if len(gains) < period:
            return 50.0
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def _calculate_trend_strength(self, prices: List[float]) -> float:
        """Calculate trend strength (-1 to 1)"""
        if len(prices) < 2:
            return 0.0
        
        n = len(prices)
        x = list(range(n))
        y = prices
        
        # Calculate correlation coefficient
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_x2 = sum(xi * xi for xi in x)
        sum_y2 = sum(yi * yi for yi in y)
        
        numerator = n * sum_xy - sum_x * sum_y
        denominator = ((n * sum_x2 - sum_x * sum_x) * (n * sum_y2 - sum_y * sum_y)) ** 0.5
        
        if denominator == 0:
            return 0.0
        
        correlation = numerator / denominator
        return correlation
    
    def calculate_market_sentiment(self, price_data: PriceData, technical_indicators: TechnicalIndicators) -> MarketSentiment:
        """Calculate market sentiment based on price and technical data"""
        score = 0.0
        factors = []
        
        # Price change factor
        if price_data.CHANGEPCT24HOUR > 5:
            factors.append(0.3)
        elif price_data.CHANGEPCT24HOUR > 0:
            factors.append(0.1)
        elif price_data.CHANGEPCT24HOUR < -5:
            factors.append(-0.3)
        else:
            factors.append(-0.1)
        
        # RSI factor
        if technical_indicators.rsi > 70:
            factors.append(-0.2)  # Overbought
        elif technical_indicators.rsi < 30:
            factors.append(0.2)   # Oversold
        else:
            factors.append(0.0)   # Neutral
        
        # Momentum factor
        if technical_indicators.momentum > 10:
            factors.append(0.2)
        elif technical_indicators.momentum < -10:
            factors.append(-0.2)
        else:
            factors.append(0.0)
        
        # Trend strength factor
        factors.append(technical_indicators.trend_strength * 0.3)
        
        # Volume factor
        if price_data.VOLUME24HOUR > 1000000000:  # High volume
            factors.append(0.1)
        else:
            factors.append(0.0)
        
        score = sum(factors) / len(factors)
        score = max(-1.0, min(1.0, score))  # Clamp to [-1, 1]
        
        # Determine label
        if score > 0.3:
            label = "Bullish"
        elif score < -0.3:
            label = "Bearish"
        else:
            label = "Neutral"
        
        # Calculate confidence
        confidence = min(1.0, abs(score) * 2)
        
        return MarketSentiment(
            score=score,
            label=label,
            confidence=confidence
        )
    
    async def get_comprehensive_analysis(self, symbol: str) -> Dict:
        """Get comprehensive analysis for a token"""
        try:
            # Fetch current price data
            price_data = await self.fetch_token_price(symbol)
            if not price_data:
                return {"error": f"Could not fetch price data for {symbol}"}
            
            # Fetch historical data
            historical_data = await self.fetch_historical_data(symbol, 30)
            
            # Calculate technical indicators
            technical_indicators = self.calculate_technical_indicators(historical_data)
            
            # Calculate market sentiment
            market_sentiment = self.calculate_market_sentiment(price_data, technical_indicators)
            
            return {
                "symbol": symbol,
                "price_data": {
                    "price": price_data.PRICE,
                    "change_24h": price_data.CHANGEPCT24HOUR,
                    "volume_24h": price_data.VOLUME24HOUR,
                    "market_cap": price_data.MKTCAP
                },
                "technical_indicators": {
                    "rsi": technical_indicators.rsi,
                    "sma_20": technical_indicators.sma_20,
                    "sma_50": technical_indicators.sma_50,
                    "volatility": technical_indicators.volatility,
                    "momentum": technical_indicators.momentum,
                    "trend_strength": technical_indicators.trend_strength
                },
                "market_sentiment": {
                    "score": market_sentiment.score,
                    "label": market_sentiment.label,
                    "confidence": market_sentiment.confidence
                },
                "historical_data_points": len(historical_data),
                "analysis_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in comprehensive analysis for {symbol}: {e}")
            return {"error": f"Analysis failed for {symbol}: {str(e)}"}

# Global instance
data_service = EnhancedDataService() 