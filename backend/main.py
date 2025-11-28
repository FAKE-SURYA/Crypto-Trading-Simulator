"""
High-Performance Crypto Trading Simulator - FastAPI Backend
Provides WebSocket streaming and REST API for order management
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import json
from typing import List, Set
import logging

from market_simulator import MarketSimulator
from trading_service import TradingService
from schemas import OrderCreate, OrderResponse, MarketDataMessage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global instances
trading_service: TradingService = None
market_simulator: MarketSimulator = None
active_connections: Set[WebSocket] = set()
background_task: asyncio.Task = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    Initializes services on startup and cleans up on shutdown
    """
    global trading_service, market_simulator, background_task
    
    # Startup
    logger.info("Starting High-Performance Crypto Trading Simulator...")
    
    # Initialize services
    trading_service = TradingService(sma_window=20)
    market_simulator = MarketSimulator(
        initial_price=45000.0,
        drift=0.0001,
        volatility=0.02,
        update_interval=0.5
    )
    
    # Start background price generation task
    background_task = asyncio.create_task(broadcast_market_data())
    
    logger.info("✓ Services initialized successfully")
    logger.info("✓ WebSocket endpoint available at: ws://localhost:8000/ws/market-data")
    logger.info("✓ REST API available at: http://localhost:8000/api/orders")
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")
    if background_task:
        background_task.cancel()
        try:
            await background_task
        except asyncio.CancelledError:
            pass
    
    # Close all WebSocket connections
    for connection in list(active_connections):
        await connection.close()
    
    logger.info("✓ Shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="Crypto Trading Simulator API",
    description="High-performance cryptocurrency trading simulator with C++ core engine",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def broadcast_market_data():
    """
    Background task that generates prices and broadcasts to all connected clients
    """
    logger.info("Starting market data broadcast...")
    
    try:
        while True:
            # Generate new price
            new_price = market_simulator.generate_price()
            
            # Process through C++ engine
            market_data = trading_service.process_price(new_price)
            
            # Broadcast to all connected WebSocket clients
            if active_connections:
                message = json.dumps(market_data)
                disconnected = set()
                
                for connection in active_connections:
                    try:
                        await connection.send_text(message)
                    except Exception as e:
                        logger.warning(f"Failed to send to client: {e}")
                        disconnected.add(connection)
                
                # Remove disconnected clients
                active_connections.difference_update(disconnected)
            
            # Broadcast trade events if any
            if market_data.get("trades"):
                for trade in market_data["trades"]:
                    trade_message = json.dumps({
                        "type": "trade",
                        **trade
                    })
                    for connection in active_connections:
                        try:
                            await connection.send_text(trade_message)
                        except:
                            pass
            
            # Wait for next update
            await asyncio.sleep(market_simulator.update_interval)
            
    except asyncio.CancelledError:
        logger.info("Market data broadcast stopped")
    except Exception as e:
        logger.error(f"Error in market data broadcast: {e}")


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "High-Performance Crypto Trading Simulator",
        "version": "1.0.0",
        "endpoints": {
            "websocket": "ws://localhost:8000/ws/market-data",
            "orders": "POST http://localhost:8000/api/orders",
            "orderbook": "GET http://localhost:8000/api/orderbook"
        }
    }


@app.get("/api/orderbook")
async def get_orderbook():
    """
    Get current order book snapshot
    
    Returns:
        dict: Current bids, asks, and best prices
    """
    if not trading_service:
        raise HTTPException(status_code=503, detail="Trading service not initialized")
    
    return trading_service.get_order_book_snapshot()


@app.post("/api/orders", response_model=OrderResponse)
async def create_order(order: OrderCreate):
    """
    Create a new buy or sell order
    
    Args:
        order: Order details (side, price, quantity)
        
    Returns:
        OrderResponse: Order confirmation with ID and status
    """
    if not trading_service:
        raise HTTPException(status_code=503, detail="Trading service not initialized")
    
    logger.info(f"Received order: {order.side} {order.quantity} @ {order.price}")
    
    # Add order to C++ order book
    result = trading_service.add_order(
        side=order.side.value,
        price=order.price,
        quantity=order.quantity
    )
    
    # Broadcast order event to WebSocket clients
    order_event = json.dumps({
        "type": "order",
        "order_id": result["order_id"],
        "side": order.side.value,
        "price": order.price,
        "quantity": order.quantity,
        "status": result["status"]
    })
    
    for connection in active_connections:
        try:
            await connection.send_text(order_event)
        except:
            pass
    
    return OrderResponse(**result)


@app.websocket("/ws/market-data")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time market data streaming
    
    Clients receive:
    - Market data updates (price, SMA, order book)
    - Trade execution events
    - Order placement events
    """
    await websocket.accept()
    active_connections.add(websocket)
    
    client_id = id(websocket)
    logger.info(f"Client {client_id} connected. Total connections: {len(active_connections)}")
    
    try:
        # Send initial order book snapshot
        if trading_service:
            snapshot = trading_service.get_order_book_snapshot()
            await websocket.send_text(json.dumps({
                "type": "snapshot",
                "orderbook": snapshot
            }))
        
        # Keep connection alive and handle incoming messages
        while True:
            try:
                data = await websocket.receive_text()
                # Echo back for heartbeat/debugging
                await websocket.send_text(json.dumps({
                    "type": "pong",
                    "received": data
                }))
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.warning(f"WebSocket error: {e}")
                break
                
    except WebSocketDisconnect:
        logger.info(f"Client {client_id} disconnected")
    finally:
        active_connections.discard(websocket)
        logger.info(f"Client {client_id} removed. Total connections: {len(active_connections)}")


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "active_connections": len(active_connections),
        "trading_service": "initialized" if trading_service else "not initialized"
    }


if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("High-Performance Crypto Trading Simulator")
    print("=" * 60)
    print("\nStarting server...")
    print("WebSocket: ws://localhost:8000/ws/market-data")
    print("REST API:  http://localhost:8000/api/orders")
    print("Docs:      http://localhost:8000/docs")
    print("=" * 60)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
