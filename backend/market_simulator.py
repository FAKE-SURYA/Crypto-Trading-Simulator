"""
Market data simulator using Geometric Brownian Motion
Generates realistic cryptocurrency price movements
"""

import numpy as np
import time
from typing import Generator


class MarketSimulator:
    """
    Generates realistic mock cryptocurrency prices using Geometric Brownian Motion (GBM)
    
    Mathematical model: dS = μ * S * dt + σ * S * dW
    Where:
        S = current price
        μ = drift (trend parameter)
        σ = volatility
        dW = random normal shock
    """
    
    def __init__(
        self,
        initial_price: float = 45000.0,
        drift: float = 0.0001,
        volatility: float = 0.02,
        update_interval: float = 0.5
    ):
        """
        Initialize the market simulator
        
        Args:
            initial_price: Starting price (default: $45,000 - Bitcoin-like)
            drift: Trend parameter (default: 0.0001 - slight upward trend)
            volatility: Price volatility (default: 0.02 - 2% volatility)
            update_interval: Time between price updates in seconds
        """
        self.price = initial_price
        self.drift = drift
        self.volatility = volatility
        self.update_interval = update_interval
        
    def generate_price(self) -> float:
        """
        Generate next price using Geometric Brownian Motion
        
        Returns:
            float: The new price
        """
        # Random normal shock
        dW = np.random.normal(0, 1)
        
        # GBM formula: dS = μ * S * dt + σ * S * dW * sqrt(dt)
        dt = self.update_interval
        drift_component = self.drift * self.price * dt
        volatility_component = self.volatility * self.price * dW * np.sqrt(dt)
        
        # Update price
        self.price += drift_component + volatility_component
        
        # Add occasional jumps for realism (3% chance)
        if np.random.random() < 0.03:
            jump = np.random.choice([-1, 1]) * self.price * np.random.uniform(0.002, 0.008)
            self.price += jump
        
        # Ensure price doesn't go negative or unrealistic
        self.price = max(self.price, 1000.0)
        self.price = min(self.price, 100000.0)
        
        return round(self.price, 2)
    
    def stream_prices(self) -> Generator[float, None, None]:
        """
        Infinite generator that yields prices at regular intervals
        
        Yields:
            float: The next price
        """
        while True:
            yield self.generate_price()
            time.sleep(self.update_interval)
