#include "engine.hpp"
#include <algorithm>
#include <numeric>
#include <stdexcept>
#include <sstream>

namespace trading {

// ==================== SMACalculator Implementation ====================

SMACalculator::SMACalculator(size_t window_size)
    : window_size_(window_size),
      current_size_(0),
      index_(0),
      running_sum_(0.0) {
    if (window_size == 0) {
        throw std::invalid_argument("Window size must be greater than 0");
    }
    prices_.resize(window_size, 0.0);
}

void SMACalculator::addPrice(double price) {
    if (price < 0) {
        throw std::invalid_argument("Price cannot be negative");
    }
    
    // Subtract the old value from running sum
    if (current_size_ == window_size_) {
        running_sum_ -= prices_[index_];
    }
    
    // Add the new price
    prices_[index_] = price;
    running_sum_ += price;
    
    // Update circular buffer index
    index_ = (index_ + 1) % window_size_;
    
    // Update size (capped at window_size)
    if (current_size_ < window_size_) {
        current_size_++;
    }
}

double SMACalculator::getSMA() const {
    if (current_size_ == 0) {
        return 0.0;
    }
    return running_sum_ / static_cast<double>(current_size_);
}

void SMACalculator::reset() {
    std::fill(prices_.begin(), prices_.end(), 0.0);
    current_size_ = 0;
    index_ = 0;
    running_sum_ = 0.0;
}

// ==================== OrderBook Implementation ====================

std::string OrderBook::generateOrderId() {
    std::ostringstream oss;
    oss << "ORD" << next_order_id_++;
    return oss.str();
}

std::string OrderBook::addOrder(OrderSide side, double price, double quantity) {
    if (price <= 0 || quantity <= 0) {
        throw std::invalid_argument("Price and quantity must be positive");
    }
    
    std::string order_id = generateOrderId();
    Order order(order_id, side, price, quantity);
    
    if (side == OrderSide::BUY) {
        bids_[price].push_back(std::move(order));
    } else {
        asks_[price].push_back(std::move(order));
    }
    
    return order_id;
}

std::vector<Trade> OrderBook::matchOrders() {
    std::vector<Trade> trades;
    
    // Continue matching while we have both bids and asks
    while (!bids_.empty() && !asks_.empty()) {
        // Get best bid and ask
        auto& best_bid_level = bids_.begin();
        auto& best_ask_level = asks_.begin();
        
        double best_bid_price = best_bid_level->first;
        double best_ask_price = best_ask_level->first;
        
        // Check if prices cross (bid >= ask)
        if (best_bid_price < best_ask_price) {
            break;  // No match possible
        }
        
        // Get the first order at each price level (FIFO)
        auto& bid_orders = best_bid_level->second;
        auto& ask_orders = best_ask_level->second;
        
        if (bid_orders.empty() || ask_orders.empty()) {
            // Clean up empty levels
            if (bid_orders.empty()) bids_.erase(best_bid_level);
            if (ask_orders.empty()) asks_.erase(best_ask_level);
            continue;
        }
        
        Order& bid_order = bid_orders.front();
        Order& ask_order = ask_orders.front();
        
        // Execute trade at the ask price (price-time priority)
        double trade_price = best_ask_price;
        double trade_quantity = std::min(bid_order.quantity, ask_order.quantity);
        
        // Create trade record
        Trade trade;
        trade.buy_order_id = bid_order.id;
        trade.sell_order_id = ask_order.id;
        trade.price = trade_price;
        trade.quantity = trade_quantity;
        
        auto now = std::chrono::system_clock::now();
        trade.timestamp = std::chrono::duration_cast<std::chrono::milliseconds>(
            now.time_since_epoch()
        ).count();
        
        trades.push_back(trade);
        
        // Update order quantities
        bid_order.quantity -= trade_quantity;
        ask_order.quantity -= trade_quantity;
        
        // Remove fully filled orders
        if (bid_order.quantity == 0) {
            bid_orders.erase(bid_orders.begin());
            if (bid_orders.empty()) {
                bids_.erase(best_bid_level);
            }
        }
        
        if (ask_order.quantity == 0) {
            ask_orders.erase(ask_orders.begin());
            if (ask_orders.empty()) {
                asks_.erase(best_ask_level);
            }
        }
    }
    
    return trades;
}

std::vector<std::pair<double, double>> OrderBook::getBids() const {
    std::vector<std::pair<double, double>> result;
    
    for (const auto& [price, orders] : bids_) {
        double total_quantity = 0.0;
        for (const auto& order : orders) {
            total_quantity += order.quantity;
        }
        result.emplace_back(price, total_quantity);
    }
    
    return result;
}

std::vector<std::pair<double, double>> OrderBook::getAsks() const {
    std::vector<std::pair<double, double>> result;
    
    for (const auto& [price, orders] : asks_) {
        double total_quantity = 0.0;
        for (const auto& order : orders) {
            total_quantity += order.quantity;
        }
        result.emplace_back(price, total_quantity);
    }
    
    return result;
}

double OrderBook::getBestBid() const {
    if (bids_.empty()) return 0.0;
    return bids_.begin()->first;
}

double OrderBook::getBestAsk() const {
    if (asks_.empty()) return 0.0;
    return asks_.begin()->first;
}

void OrderBook::reset() {
    bids_.clear();
    asks_.clear();
    next_order_id_ = 1;
}

} // namespace trading
