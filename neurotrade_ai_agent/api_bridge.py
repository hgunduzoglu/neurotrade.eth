"""
NeuroTrade AI Agent API Bridge

This FastAPI service provides REST endpoints for the frontend to communicate
with the AI agent. It handles user queries and returns AI responses.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import logging
import asyncio
from datetime import datetime

# Import the enhanced AI agent
from enhanced_ai_agent import enhanced_analyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="NeuroTrade AI Agent API",
    description="API bridge for NeuroTrade AI agent communication",
    version="1.0.0"
)

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    symbols: Optional[List[str]] = None
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    timestamp: str
    symbols_analyzed: List[str]
    analysis_type: str
    success: bool
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str

class TokenAnalysisRequest(BaseModel):
    symbol: str

class TokenAnalysisResponse(BaseModel):
    symbol: str
    analysis: dict
    timestamp: str
    success: bool
    error: Optional[str] = None

# Global state for session management
active_sessions = {}

@app.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )

@app.get("/health", response_model=HealthResponse)
async def health():
    """Detailed health check"""
    try:
        # Test if the enhanced analyzer is working
        test_analysis = await enhanced_analyzer.analyze_token("ETH")
        
        return HealthResponse(
            status="healthy" if "error" not in test_analysis else "degraded",
            timestamp=datetime.now().isoformat(),
            version="1.0.0"
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="unhealthy",
            timestamp=datetime.now().isoformat(),
            version="1.0.0"
        )

@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """
    Main chat endpoint for communicating with the AI agent
    """
    try:
        logger.info(f"Received chat request: {request.message}")
        
        # Generate response using enhanced analyzer
        response_text = await enhanced_analyzer.generate_trading_response(
            query=request.message,
            symbols=request.symbols
        )
        
        # Extract symbols that were analyzed
        symbols_analyzed = request.symbols if request.symbols else ["ETH"]
        
        # Determine analysis type based on query
        query_lower = request.message.lower()
        if any(word in query_lower for word in ["price", "cost", "value"]):
            analysis_type = "price_analysis"
        elif any(word in query_lower for word in ["buy", "purchase"]):
            analysis_type = "buy_analysis"
        elif any(word in query_lower for word in ["sell", "exit"]):
            analysis_type = "sell_analysis"
        elif any(word in query_lower for word in ["swap", "trade"]):
            analysis_type = "swap_analysis"
        else:
            analysis_type = "general_analysis"
        
        return ChatResponse(
            response=response_text,
            timestamp=datetime.now().isoformat(),
            symbols_analyzed=symbols_analyzed,
            analysis_type=analysis_type,
            success=True
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return ChatResponse(
            response="❌ Sorry, I encountered an error processing your request. Please try again.",
            timestamp=datetime.now().isoformat(),
            symbols_analyzed=[],
            analysis_type="error",
            success=False,
            error=str(e)
        )

@app.post("/analyze/{symbol}", response_model=TokenAnalysisResponse)
async def analyze_token(symbol: str):
    """
    Get detailed analysis for a specific token
    """
    try:
        logger.info(f"Analyzing token: {symbol}")
        
        # Get comprehensive analysis
        analysis = await enhanced_analyzer.analyze_token(symbol.upper())
        
        if "error" in analysis:
            return TokenAnalysisResponse(
                symbol=symbol.upper(),
                analysis={},
                timestamp=datetime.now().isoformat(),
                success=False,
                error=analysis["error"]
            )
        
        return TokenAnalysisResponse(
            symbol=symbol.upper(),
            analysis=analysis,
            timestamp=datetime.now().isoformat(),
            success=True
        )
        
    except Exception as e:
        logger.error(f"Error analyzing token {symbol}: {e}")
        return TokenAnalysisResponse(
            symbol=symbol.upper(),
            analysis={},
            timestamp=datetime.now().isoformat(),
            success=False,
            error=str(e)
        )

@app.get("/supported-tokens")
async def get_supported_tokens():
    """Get list of supported tokens"""
    return {
        "tokens": enhanced_analyzer.supported_tokens,
        "count": len(enhanced_analyzer.supported_tokens),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/batch-analyze")
async def batch_analyze_tokens(symbols: List[str]):
    """
    Analyze multiple tokens at once
    """
    try:
        if len(symbols) > 5:  # Limit batch size
            raise HTTPException(status_code=400, detail="Maximum 5 tokens per batch")
        
        results = {}
        for symbol in symbols:
            try:
                analysis = await enhanced_analyzer.analyze_token(symbol.upper())
                results[symbol.upper()] = analysis
            except Exception as e:
                results[symbol.upper()] = {"error": str(e)}
        
        return {
            "results": results,
            "timestamp": datetime.now().isoformat(),
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Error in batch analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/session/{session_id}")
async def get_session(session_id: str):
    """Get session information"""
    if session_id in active_sessions:
        return active_sessions[session_id]
    else:
        raise HTTPException(status_code=404, detail="Session not found")

@app.post("/session/{session_id}/start")
async def start_session(session_id: str, user_id: Optional[str] = None):
    """Start a new chat session"""
    active_sessions[session_id] = {
        "session_id": session_id,
        "user_id": user_id,
        "start_time": datetime.now().isoformat(),
        "message_count": 0,
        "last_activity": datetime.now().isoformat()
    }
    
    return {
        "message": "Session started successfully",
        "session_info": active_sessions[session_id]
    }

@app.post("/session/{session_id}/end")
async def end_session(session_id: str):
    """End a chat session"""
    if session_id in active_sessions:
        session_info = active_sessions[session_id]
        del active_sessions[session_id]
        return {
            "message": "Session ended successfully",
            "session_summary": session_info
        }
    else:
        raise HTTPException(status_code=404, detail="Session not found")

# WebSocket support for real-time chat (optional)
try:
    from fastapi import WebSocket, WebSocketDisconnect
    from fastapi.responses import HTMLResponse
    
    @app.websocket("/ws/{session_id}")
    async def websocket_endpoint(websocket: WebSocket, session_id: str):
        await websocket.accept()
        logger.info(f"WebSocket connection established for session: {session_id}")
        
        try:
            while True:
                data = await websocket.receive_text()
                logger.info(f"WebSocket message received: {data}")
                
                # Process the message with AI agent
                try:
                    response = await enhanced_analyzer.generate_trading_response(data)
                    await websocket.send_text(response)
                except Exception as e:
                    error_response = f"❌ Error processing request: {str(e)}"
                    await websocket.send_text(error_response)
                    
        except WebSocketDisconnect:
            logger.info(f"WebSocket disconnected for session: {session_id}")
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            await websocket.close()

except ImportError:
    logger.warning("WebSocket support not available")

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting NeuroTrade AI Agent API Bridge...")
    logger.info("Enhanced AI Agent loaded successfully")
    logger.info("API will be available at: http://localhost:8000")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True
    ) 