#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "engine.hpp"

namespace py = pybind11;
using namespace trading;

PYBIND11_MODULE(trade_engine, m) {
    m.doc() = "High-performance C++ trading engine for cryptocurrency simulation";

    // Expose OrderSide enum
    py::enum_<OrderSide>(m, "OrderSide")
        .value("BUY", OrderSide::BUY)
        .value("SELL", OrderSide::SELL)
        .export_values();

    // Expose Order struct
    py::class_<Order>(m, "Order")
        .def_readonly("id", &Order::id)
        .def_readonly("side", &Order::side)
        .def_readonly("price", &Order::price)
        .def_readonly("quantity", &Order::quantity)
        .def_readonly("timestamp", &Order::timestamp);

    // Expose Trade struct
    py::class_<Trade>(m, "Trade")
        .def_readonly("buy_order_id", &Trade::buy_order_id)
        .def_readonly("sell_order_id", &Trade::sell_order_id)
        .def_readonly("price", &Trade::price)
        .def_readonly("quantity", &Trade::quantity)
        .def_readonly("timestamp", &Trade::timestamp);

    // Expose SMACalculator class
    py::class_<SMACalculator>(m, "SMACalculator")
        .def(py::init<size_t>(), py::arg("window_size"),
             "Construct a Simple Moving Average calculator\n\n"
             "Args:\n"
             "    window_size: Number of prices to average over")
        .def("add_price", &SMACalculator::addPrice, py::arg("price"),
             "Add a new price to the calculation\n\n"
             "Args:\n"
             "    price: The price value to add")
        .def("get_sma", &SMACalculator::getSMA,
             "Get the current Simple Moving Average\n\n"
             "Returns:\n"
             "    float: The SMA value, or 0.0 if insufficient data")
        .def("size", &SMACalculator::size,
             "Get the number of prices currently stored\n\n"
             "Returns:\n"
             "    int: Number of prices")
        .def("reset", &SMACalculator::reset,
             "Reset the calculator, clearing all stored prices");

    // Expose OrderBook class
    py::class_<OrderBook>(m, "OrderBook")
        .def(py::init<>(),
             "Construct an empty order book")
        .def("add_order", &OrderBook::addOrder,
             py::arg("side"), py::arg("price"), py::arg("quantity"),
             "Add an order to the book\n\n"
             "Args:\n"
             "    side: Order side (OrderSide.BUY or OrderSide.SELL)\n"
             "    price: Order price (must be positive)\n"
             "    quantity: Order quantity (must be positive)\n\n"
             "Returns:\n"
             "    str: The generated order ID")
        .def("match_orders", &OrderBook::matchOrders,
             "Match orders and execute trades\n\n"
             "Returns:\n"
             "    List[Trade]: List of executed trades")
        .def("get_bids", &OrderBook::getBids,
             "Get all bid orders\n\n"
             "Returns:\n"
             "    List[Tuple[float, float]]: List of (price, quantity) pairs, sorted by price descending")
        .def("get_asks", &OrderBook::getAsks,
             "Get all ask orders\n\n"
             "Returns:\n"
             "    List[Tuple[float, float]]: List of (price, quantity) pairs, sorted by price ascending")
        .def("get_best_bid", &OrderBook::getBestBid,
             "Get the best bid price\n\n"
             "Returns:\n"
             "    float: Best bid price, or 0.0 if no bids")
        .def("get_best_ask", &OrderBook::getBestAsk,
             "Get the best ask price\n\n"
             "Returns:\n"
             "    float: Best ask price, or 0.0 if no asks")
        .def("reset", &OrderBook::reset,
             "Reset the order book, removing all orders");

    // Module version
    m.attr("__version__") = "1.0.0";
}
