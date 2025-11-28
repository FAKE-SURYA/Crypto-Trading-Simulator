/**
 * TypeScript interfaces for API communication
 * Matches backend Pydantic schemas for type safety
 */

export interface OrderBook {
    bids: [number, number][];  // [price, quantity]
    asks: [number, number][];   // [price, quantity]
}

export interface MarketDataMessage {
    timestamp: number;
    price: number;
    sma: number;
    orderbook: OrderBook;
    trades?: Trade[];
}

export interface Trade {
    buy_order_id: string;
    sell_order_id: string;
    price: number;
    quantity: number;
    timestamp: number;
}

export interface Order {
    side: 'buy' | 'sell';
    price: number;
    quantity: number;
}

export interface OrderResponse {
    order_id: string;
    status: 'pending' | 'filled' | 'rejected';
    message: string;
}

export interface OrderEvent {
    type: 'order';
    order_id: string;
    side: 'buy' | 'sell';
    price: number;
    quantity: number;
    status: string;
}

export interface TradeEvent {
    type: 'trade';
    timestamp: number;
    buy_order_id: string;
    sell_order_id: string;
    price: number;
    quantity: number;
}

export interface PricePoint {
    timestamp: number;
    price: number;
    sma: number;
}

export type WebSocketMessage = MarketDataMessage | OrderEvent | TradeEvent;
