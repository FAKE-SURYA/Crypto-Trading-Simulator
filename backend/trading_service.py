"""
Trading service integrating C++ engine with Python backend
Manages SMA calculations and order book state
"""

import time
import sys
from typing import Dict, List, Tuple, Optional

# Import the C++ trading engine (or Python fallback)
try:
    import trade_engine
    print("✓ Using C++ trade_engine module (high performance)")
except ImportError:
    print("⚠ C++ module not available, using Python fallback")
    print("  To build C++ module: cd cpp_core && pip install .")
    import trade_engine  # Will use the Python fallback we created


class TradingService:
    """
    Service layer for trading operations
    Integrates C++ SMACalculator and OrderBook with Python backend
    """
    
    def __init__(self, sma_window: int = 20):
        """
        Initialize trading service
        
        Args:
            sma_window: Window size for Simple Moving Average calculation
        """
        # Initialize C++ components
        self.sma_calculator = trade_engine.SMACalculator(sma_window)
        self.order_book = trade_engine.OrderBook()
        
        # Track recent prices for UI
        self.price_history: List[Tuple[float, float]] = []  # (timestamp, price)
        self.max_history = 100
        
    def process_price(self, price: float) -> Dict:
        """
        Process a new price through the C++ engine
        
        Args:
            price: The new market price
            
        Returns:
            dict: Market data including price, SMA, and order book
        """
        # Add price to C++ SMA calculator
        self.sma_calculator.add_price(price)
        current_sma = self.sma_calculator.get_sma()
        
        # Store in history
        timestamp = time.time()
        self.price_history.append((timestamp, price))
        
        # Trim history if too long
        if len(self.price_history) > self.max_history:
            self.price_history = self.price_history[-self.max_history:]
        
        # Match any pending orders
        trades = self.order_book.match_orders()
        
        # Get current order book state
        bids = self.order_book.get_bids()
        asks = self.order_book.get_asks()
        
        return {
            "timestamp": timestamp,
            "price": price,
            "sma": current_sma,
            "orderbook": {
                "bids": [[float(p), float(q)] for p, q in bids],
                "asks": [[float(p), float(q)] for p, q in asks]
            },
            "trades": [
                {
                    "buy_order_id": t.buy_order_id,
                    "sell_order_id": t.sell_order_id,
                    "price": t.price,
                    "quantity": t.quantity,
                    "timestamp": t.timestamp
                }
                for t in trades
            ]
        }
    
    def add_order(self, side: str, price: float, quantity: float) -> Dict:
        """
        Add an order to the C++ order book
        
        Args:
            side: "buy" or "sell"
            price: Order price
            quantity: Order quantity
            
        Returns:
            dict: Order confirmation with order_id and status
        """
        try:
            # Convert side to C++ enum
            if side.lower() == "buy":
                cpp_side = trade_engine.OrderSide.BUY
            elif side.lower() == "sell":
                cpp_side = trade_engine.OrderSide.SELL
            else:
                return {
                    "order_id": "",
                    "status": "rejected",
                    "message": f"Invalid order side: {side}"
                }
            
            # Add order to C++ order book
            order_id = self.order_book.add_order(cpp_side, price, quantity)
            
            return {
                "order_id": order_id,
                "status": "pending",
                "message": "Order placed successfully"
            }
            
        except Exception as e:
            return {
                "order_id": "",
                "status": "rejected",
                "message": str(e)
            }
    
    def get_order_book_snapshot(self) -> Dict:
        """
        Get current order book state
        
        Returns:
            dict: Current bids and asks
        """
        bids = self.order_book.get_bids()
        asks = self.order_book.get_asks()
        
        return {
            "bids": [[float(p), float(q)] for p, q in bids],
            "asks": [[float(p), float(q)] for p, q in asks],
            "best_bid": float(self.order_book.get_best_bid()),
            "best_ask": float(self.order_book.get_best_ask())
        }
    
    def reset(self):
        """Reset all trading state"""
        self.sma_calculator.reset()
        self.order_book.reset()
        self.price_history.clear()
