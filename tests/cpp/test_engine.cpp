#include "engine.hpp"
#include <gtest/gtest.h>


using namespace trading;

// ==================== SMACalculator Tests ====================

TEST(SMACalculatorTest, InitializationTest) {
  SMACalculator sma(5);
  EXPECT_EQ(sma.size(), 0);
  EXPECT_DOUBLE_EQ(sma.getSMA(), 0.0);
}

TEST(SMACalculatorTest, InvalidWindowSize) {
  EXPECT_THROW(SMACalculator sma(0), std::invalid_argument);
}

TEST(SMACalculatorTest, SinglePriceTest) {
  SMACalculator sma(5);
  sma.addPrice(100.0);
  EXPECT_EQ(sma.size(), 1);
  EXPECT_DOUBLE_EQ(sma.getSMA(), 100.0);
}

TEST(SMACalculatorTest, PartialWindowTest) {
  SMACalculator sma(5);
  sma.addPrice(100.0);
  sma.addPrice(102.0);
  sma.addPrice(98.0);

  EXPECT_EQ(sma.size(), 3);
  EXPECT_DOUBLE_EQ(sma.getSMA(), 100.0); // (100 + 102 + 98) / 3
}

TEST(SMACalculatorTest, FullWindowTest) {
  SMACalculator sma(3);
  sma.addPrice(100.0);
  sma.addPrice(102.0);
  sma.addPrice(98.0);
  sma.addPrice(104.0);

  EXPECT_EQ(sma.size(), 3);
  // Should use last 3 prices: 102, 98, 104
  EXPECT_NEAR(sma.getSMA(), 101.333, 0.001);
}

TEST(SMACalculatorTest, CircularBufferTest) {
  SMACalculator sma(3);
  for (int i = 1; i <= 10; i++) {
    sma.addPrice(i * 10.0);
  }

  EXPECT_EQ(sma.size(), 3);
  // Last 3 prices: 80, 90, 100
  EXPECT_DOUBLE_EQ(sma.getSMA(), 90.0);
}

TEST(SMACalculatorTest, ResetTest) {
  SMACalculator sma(3);
  sma.addPrice(100.0);
  sma.addPrice(102.0);
  sma.reset();

  EXPECT_EQ(sma.size(), 0);
  EXPECT_DOUBLE_EQ(sma.getSMA(), 0.0);
}

TEST(SMACalculatorTest, NegativePriceTest) {
  SMACalculator sma(3);
  EXPECT_THROW(sma.addPrice(-10.0), std::invalid_argument);
}

// ==================== OrderBook Tests ====================

TEST(OrderBookTest, InitializationTest) {
  OrderBook book;
  EXPECT_EQ(book.getBids().size(), 0);
  EXPECT_EQ(book.getAsks().size(), 0);
  EXPECT_DOUBLE_EQ(book.getBestBid(), 0.0);
  EXPECT_DOUBLE_EQ(book.getBestAsk(), 0.0);
}

TEST(OrderBookTest, AddBuyOrderTest) {
  OrderBook book;
  std::string order_id = book.addOrder(OrderSide::BUY, 45000.0, 1.5);

  EXPECT_FALSE(order_id.empty());
  EXPECT_EQ(book.getBids().size(), 1);
  EXPECT_DOUBLE_EQ(book.getBestBid(), 45000.0);
}

TEST(OrderBookTest, AddSellOrderTest) {
  OrderBook book;
  std::string order_id = book.addOrder(OrderSide::SELL, 45100.0, 2.0);

  EXPECT_FALSE(order_id.empty());
  EXPECT_EQ(book.getAsks().size(), 1);
  EXPECT_DOUBLE_EQ(book.getBestAsk(), 45100.0);
}

TEST(OrderBookTest, InvalidOrderTest) {
  OrderBook book;
  EXPECT_THROW(book.addOrder(OrderSide::BUY, -100.0, 1.0),
               std::invalid_argument);
  EXPECT_THROW(book.addOrder(OrderSide::BUY, 100.0, -1.0),
               std::invalid_argument);
  EXPECT_THROW(book.addOrder(OrderSide::BUY, 0.0, 1.0), std::invalid_argument);
}

TEST(OrderBookTest, NoMatchTest) {
  OrderBook book;
  book.addOrder(OrderSide::BUY, 45000.0, 1.0);
  book.addOrder(OrderSide::SELL, 45100.0, 1.0);

  auto trades = book.matchOrders();
  EXPECT_EQ(trades.size(), 0); // No match (bid < ask)
}

TEST(OrderBookTest, SimpleMatchTest) {
  OrderBook book;
  book.addOrder(OrderSide::BUY, 45100.0, 1.0);
  book.addOrder(OrderSide::SELL, 45100.0, 1.0);

  auto trades = book.matchOrders();
  EXPECT_EQ(trades.size(), 1);
  EXPECT_DOUBLE_EQ(trades[0].price, 45100.0);
  EXPECT_DOUBLE_EQ(trades[0].quantity, 1.0);

  // Both orders should be filled and removed
  EXPECT_EQ(book.getBids().size(), 0);
  EXPECT_EQ(book.getAsks().size(), 0);
}

TEST(OrderBookTest, PartialFillTest) {
  OrderBook book;
  book.addOrder(OrderSide::BUY, 45000.0, 2.0);
  book.addOrder(OrderSide::SELL, 45000.0, 1.0);

  auto trades = book.matchOrders();
  EXPECT_EQ(trades.size(), 1);
  EXPECT_DOUBLE_EQ(trades[0].quantity, 1.0);

  // Bid should have remaining quantity
  auto bids = book.getBids();
  EXPECT_EQ(bids.size(), 1);
  EXPECT_DOUBLE_EQ(bids[0].second, 1.0); // Remaining quantity

  // Ask should be fully filled
  EXPECT_EQ(book.getAsks().size(), 0);
}

TEST(OrderBookTest, PriceTimePriorityTest) {
  OrderBook book;

  // Add multiple orders at same price
  book.addOrder(OrderSide::SELL, 45000.0, 1.0); // First
  book.addOrder(OrderSide::SELL, 45000.0, 2.0); // Second

  // Add matching buy order
  book.addOrder(OrderSide::BUY, 45000.0, 1.5);

  auto trades = book.matchOrders();

  // Should match with first sell order first (FIFO)
  EXPECT_EQ(trades.size(), 1);
  EXPECT_DOUBLE_EQ(trades[0].quantity, 1.0);
}

TEST(OrderBookTest, MultipleMatchesTest) {
  OrderBook book;
  book.addOrder(OrderSide::SELL, 45000.0, 1.0);
  book.addOrder(OrderSide::SELL, 45050.0, 1.0);
  book.addOrder(OrderSide::BUY, 45100.0, 2.0); // Crosses both asks

  auto trades = book.matchOrders();

  // Should execute 2 trades
  EXPECT_EQ(trades.size(), 2);
  EXPECT_DOUBLE_EQ(trades[0].price, 45000.0);
  EXPECT_DOUBLE_EQ(trades[1].price, 45050.0);
}

TEST(OrderBookTest, ResetTest) {
  OrderBook book;
  book.addOrder(OrderSide::BUY, 45000.0, 1.0);
  book.addOrder(OrderSide::SELL, 45100.0, 1.0);
  book.reset();

  EXPECT_EQ(book.getBids().size(), 0);
  EXPECT_EQ(book.getAsks().size(), 0);
}

// Main function
int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
