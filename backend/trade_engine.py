"""
Python fallback for trade_engine module
Used when C++ module is not available
"""

class OrderSide:
    """Order side enum"""
    BUY = "BUY"
    SELL = "SELL"


class Order:
    """Order class"""
    def __init__(self, order_id, side, price, quantity):
        self.id = order_id
        self.side = side
        self.price = price
        self.quantity = quantity
        import time
        self.timestamp = int(time.time() * 1000)


class Trade:
    """Trade class"""
    def __init__(self):
        self.buy_order_id = ""
        self.sell_order_id = ""
        self.price = 0.0
        self.quantity = 0.0
        import time
        self.timestamp = int(time.time() * 1000)


class SMACalculator:
    """Python fallback SMA calculator"""
    def __init__(self, window_size):
        self.window_size = window_size
        self.prices = []
    
    def add_price(self, price):
        self.prices.append(price)
        if len(self.prices) > self.window_size:
            self.prices.pop(0)
    
    def get_sma(self):
        if not self.prices:
            return 0.0
        return sum(self.prices) / len(self.prices)
    
    def size(self):
        return len(self.prices)
    
    def reset(self):
        self.prices = []


class OrderBook:
    """Python fallback order book"""
    def __init__(self):
        self.bids = {}  # price -> [orders]
        self.asks = {}  # price -> [orders]
        self.next_id = 1
    
    def add_order(self, side, price, quantity):
        order_id = f"ORD{self.next_id}"
        self.next_id += 1
        
        order = Order(order_id, side, price, quantity)
        
        if side == OrderSide.BUY:
            if price not in self.bids:
                self.bids[price] = []
            self.bids[price].append(order)
        else:
            if price not in self.asks:
                self.asks[price] = []
            self.asks[price].append(order)
        
        return order_id
    
    def match_orders(self):
        trades = []
        # Simplified matching - just return empty for now
        return trades
    
    def get_bids(self):
        result = []
        for price in sorted(self.bids.keys(), reverse=True):
            total_qty = sum(o.quantity for o in self.bids[price])
            result.append((price, total_qty))
        return result
    
    def get_asks(self):
        result = []
        for price in sorted(self.asks.keys()):
            total_qty = sum(o.quantity for o in self.asks[price])
            result.append((price, total_qty))
        return result
    
    def get_best_bid(self):
        if not self.bids:
            return 0.0
        return max(self.bids.keys())
    
    def get_best_ask(self):
        if not self.asks:
            return 0.0
        return min(self.asks.keys())
    
    def reset(self):
        self.bids = {}
        self.asks = {}
        self.next_id = 1


__version__ = "1.0.0 (Python Fallback)"
