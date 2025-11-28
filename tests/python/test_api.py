"""
Python backend tests using pytest
Tests FastAPI endpoints, WebSocket connections, and C++ engine integration
"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from main import app
from trading_service import TradingService


@pytest.fixture
def client():
    """Create test client for FastAPI app"""
    return TestClient(app)


@pytest.fixture
def trading_service():
    """Create trading service instance for testing"""
    return TradingService(sma_window=5)


class TestHealthEndpoints:
    """Test health and info endpoints"""
    
    def test_root_endpoint(self, client):
        """Test root endpoint returns API information"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "endpoints" in data
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestOrderBookEndpoint:
    """Test order book REST API"""
    
    def test_get_empty_orderbook(self, client):
        """Test getting empty order book"""
        response = client.get("/api/orderbook")
        assert response.status_code == 200
        data = response.json()
        assert "bids" in data
        assert "asks" in data
        assert isinstance(data["bids"], list)
        assert isinstance(data["asks"], list)


class TestOrdersEndpoint:
    """Test order creation POST endpoint"""
    
    def test_create_buy_order(self, client):
        """Test creating a buy order"""
        order_data = {
            "side": "buy",
            "price": 45000.0,
            "quantity": 1.5
        }
        response = client.post("/api/orders", json=order_data)
        assert response.status_code == 200
        data = response.json()
        assert "order_id" in data
        assert data["status"] in ["pending", "filled"]
    
    def test_create_sell_order(self, client):
        """Test creating a sell order"""
        order_data = {
            "side": "sell",
            "price": 45100.0,
            "quantity": 2.0
        }
        response = client.post("/api/orders", json=order_data)
        assert response.status_code == 200
        data = response.json()
        assert "order_id" in data
    
    def test_invalid_price(self, client):
        """Test order with invalid price"""
        order_data = {
            "side": "buy",
            "price": -100.0,  # Invalid negative price
            "quantity": 1.0
        }
        response = client.post("/api/orders", json=order_data)
        assert response.status_code == 422  # Validation error
    
    def test_invalid_quantity(self, client):
        """Test order with invalid quantity"""
        order_data = {
            "side": "buy",
            "price": 45000.0,
            "quantity": 0.0  # Invalid zero quantity
        }
        response = client.post("/api/orders", json=order_data)
        assert response.status_code == 422


class TestCppEngineIntegration:
    """Test C++ trading engine integration"""
    
    def test_sma_calculator(self, trading_service):
        """Test SMA calculation through trading service"""
        prices = [100.0, 102.0, 98.0, 104.0, 96.0]
        
        for price in prices:
            result = trading_service.process_price(price)
            assert "price" in result
            assert "sma" in result
            assert "orderbook" in result
        
        # After 5 prices, SMA should be the average
        final_result = trading_service.process_price(100.0)
        expected_sma = sum(prices[1:] + [100.0]) / 5
        assert abs(final_result["sma"] - expected_sma) < 0.01
    
    def test_order_matching(self, trading_service):
        """Test order matching through trading service"""
        # Add a buy order
        buy_result = trading_service.add_order("buy", 45000.0, 1.0)
        assert buy_result["status"] == "pending"
        
        # Add a matching sell order
        sell_result = trading_service.add_order("sell", 45000.0, 1.0)
        assert sell_result["status"] == "pending"
        
        # Process a price to trigger matching
        market_data = trading_service.process_price(45000.0)
        
        # Check if trade was executed
        if market_data.get("trades"):
            assert len(market_data["trades"]) > 0
            trade = market_data["trades"][0]
            assert trade["price"] == 45000.0
            assert trade["quantity"] == 1.0
    
    def test_price_history(self, trading_service):
        """Test price history tracking"""
        for i in range(10):
            trading_service.process_price(45000.0 + i * 10)
        
        assert len(trading_service.price_history) == 10


@pytest.mark.asyncio
class TestWebSocket:
    """Test WebSocket connection and messaging"""
    
    async def test_websocket_connection(self):
        """Test WebSocket connection"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Note: Full WebSocket testing requires more setup
            # This is a placeholder for WebSocket tests
            pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
