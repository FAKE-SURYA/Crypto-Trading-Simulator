"""
Pydantic schemas for API request/response validation
Ensures type safety between Python backend and TypeScript frontend
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal
from enum import Enum


class OrderSideEnum(str, Enum):
    """Order side enumeration"""
    BUY = "buy"
    SELL = "sell"


class OrderCreate(BaseModel):
    """Request schema for creating a new order"""
    side: OrderSideEnum = Field(..., description="Order side (buy or sell)")
    price: float = Field(..., gt=0, description="Order price (must be positive)")
    quantity: float = Field(..., gt=0, description="Order quantity (must be positive)")
    
    @field_validator('price', 'quantity')
    @classmethod
    def validate_positive(cls, v):
        if v <= 0:
            raise ValueError("Must be positive")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "side": "buy",
                "price": 45000.50,
                "quantity": 1.5
            }
        }


class OrderResponse(BaseModel):
    """Response schema for order creation"""
    order_id: str = Field(..., description="Unique order identifier")
    status: Literal["pending", "filled", "rejected"] = Field(..., description="Order status")
    message: str = Field(default="", description="Additional information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "order_id": "ORD123",
                "status": "pending",
                "message": "Order placed successfully"
            }
        }


class MarketDataMessage(BaseModel):
    """WebSocket message schema for market data"""
    timestamp: float = Field(..., description="Unix timestamp in milliseconds")
    price: float = Field(..., description="Current market price")
    sma: float = Field(..., description="Simple Moving Average")
    orderbook: dict = Field(..., description="Current order book state")
    
    class Config:
        json_schema_extra = {
            "example": {
                "timestamp": 1234567890.123,
                "price": 45123.45,
                "sma": 45050.20,
                "orderbook": {
                    "bids": [[44950, 2.5], [44900, 1.2]],
                    "asks": [[45100, 1.8], [45150, 3.0]]
                }
            }
        }


class TradeMessage(BaseModel):
    """WebSocket message for trade execution events"""
    type: Literal["trade"] = "trade"
    timestamp: float
    buy_order_id: str
    sell_order_id: str
    price: float
    quantity: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "type": "trade",
                "timestamp": 1234567890.123,
                "buy_order_id": "ORD123",
                "sell_order_id": "ORD124",
                "price": 45100.00,
                "quantity": 1.5
            }
        }
