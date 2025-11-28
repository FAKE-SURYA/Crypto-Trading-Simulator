#pragma once

#include <vector>
#include <map>
#include <string>
#include <memory>
#include <chrono>

namespace trading {

/**
 * @brief High-performance Simple Moving Average calculator using circular buffer
 * 
 * Optimized for O(1) price updates and SMA calculations using a running sum.
 * Demonstrates understanding of data structures and performance optimization.
 */
class SMACalculator {
public:
    /**
     * @brief Construct a new SMACalculator
     * @param window_size Number of prices to average over
     */
    explicit SMACalculator(size_t window_size);
    
    /**
     * @brief Add a new price to the calculation
     * @param price The price to add
     */
    void addPrice(double price);
    
    /**
     * @brief Get the current Simple Moving Average
     * @return double The SMA value, or 0.0 if insufficient data
     */
    double getSMA() const;
    
    /**
     * @brief Get the number of prices currently stored
     * @return size_t Number of prices
     */
    size_t size() const { return current_size_; }
    
    /**
     * @brief Reset the calculator
     */
    void reset();

private:
    std::vector<double> prices_;     // Circular buffer for prices
    size_t window_size_;             // Maximum number of prices to store
    size_t current_size_;            // Current number of prices stored
    size_t index_;                   // Current position in circular buffer
    double running_sum_;             // Running sum for O(1) average calculation
};

/**
 * @brief Order side enum
 */
enum class OrderSide {
    BUY,
    SELL
};

/**
 * @brief Represents a trading order
 */
struct Order {
    std::string id;
    OrderSide side;
    double price;
    double quantity;
    long long timestamp;  // Unix timestamp in milliseconds
    
    Order(const std::string& order_id, OrderSide s, double p, double q)
        : id(order_id), side(s), price(p), quantity(q) {
        auto now = std::chrono::system_clock::now();
        timestamp = std::chrono::duration_cast<std::chrono::milliseconds>(
            now.time_since_epoch()
        ).count();
    }
};

/**
 * @brief Represents an executed trade
 */
struct Trade {
    std::string buy_order_id;
    std::string sell_order_id;
    double price;
    double quantity;
    long long timestamp;
};

/**
 * @brief Simple order matching engine with price-time priority
 * 
 * Implements a basic order book with automatic matching when bid >= ask.
 * Uses price-time priority (FIFO at each price level).
 */
class OrderBook {
public:
    OrderBook() = default;
    
    /**
     * @brief Add an order to the book
     * @param side Order side (BUY or SELL)
     * @param price Order price
     * @param quantity Order quantity
     * @return std::string The generated order ID
     */
    std::string addOrder(OrderSide side, double price, double quantity);
    
    /**
     * @brief Match orders and execute trades
     * @return std::vector<Trade> Vector of executed trades
     */
    std::vector<Trade> matchOrders();
    
    /**
     * @brief Get all bid orders (sorted by price descending)
     * @return std::vector<std::pair<double, double>> Vector of (price, quantity) pairs
     */
    std::vector<std::pair<double, double>> getBids() const;
    
    /**
     * @brief Get all ask orders (sorted by price ascending)
     * @return std::vector<std::pair<double, double>> Vector of (price, quantity) pairs
     */
    std::vector<std::pair<double, double>> getAsks() const;
    
    /**
     * @brief Get the best bid price
     * @return double Best bid price, or 0.0 if no bids
     */
    double getBestBid() const;
    
    /**
     * @brief Get the best ask price
     * @return double Best ask price, or 0.0 if no asks
     */
    double getBestAsk() const;
    
    /**
     * @brief Reset the order book
     */
    void reset();

private:
    // Buy orders: price -> vector of orders (sorted by time)
    // Using reverse order (greater price first)
    std::map<double, std::vector<Order>, std::greater<double>> bids_;
    
    // Sell orders: price -> vector of orders (sorted by time)
    // Using natural order (lower price first)
    std::map<double, std::vector<Order>> asks_;
    
    size_t next_order_id_ = 1;
    
    std::string generateOrderId();
};

} // namespace trading
