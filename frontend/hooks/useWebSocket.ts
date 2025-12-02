import { useEffect, useRef, useState, useCallback } from 'react';
import { MarketDataMessage, OrderEvent, TradeEvent } from '@/types/api';

interface UseWebSocketReturn { //
    data: MarketDataMessage | null;
    isConnected: boolean;
    sendOrder: (side: 'buy' | 'sell', price: number, quantity: number) => Promise<void>;
    trades: TradeEvent[];
    error: string | null;
}

// Get API URL from environment variable or default to localhost
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const WS_URL = API_URL.replace('http', 'ws') + '/ws/market-data';
const RECONNECT_INTERVAL = 3000;
const MAX_RECONNECT_ATTEMPTS = 10;

export function useWebSocket(): UseWebSocketReturn {
    const [data, setData] = useState<MarketDataMessage | null>(null);
    const [isConnected, setIsConnected] = useState(false);
    const [trades, setTrades] = useState<TradeEvent[]>([]);
    const [error, setError] = useState<string | null>(null);

    const wsRef = useRef<WebSocket | null>(null);
    const reconnectAttemptsRef = useRef(0);
    const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);

    const connect = useCallback(() => {
        try {
            const ws = new WebSocket(WS_URL);

            ws.onopen = () => {
                console.log('✓ WebSocket connected');
                setIsConnected(true);
                setError(null);
                reconnectAttemptsRef.current = 0;
            };

            ws.onmessage = (event) => {
                try {
                    const message = JSON.parse(event.data);

                    // Handle different message types
                    if (message.type === 'trade') {
                        setTrades(prev => [message as TradeEvent, ...prev].slice(0, 20));
                    } else if (message.type === 'order') {
                        // Order event - could trigger UI update
                        console.log('Order event:', message);
                    } else {
                        // Market data update
                        setData(message as MarketDataMessage);
                    }
                } catch (err) {
                    console.error('Failed to parse WebSocket message:', err);
                }
            };

            ws.onerror = (event) => {
                console.error('WebSocket error:', event);
                setError('Connection error');
            };

            ws.onclose = () => {
                console.log('WebSocket disconnected');
                setIsConnected(false);
                wsRef.current = null;

                // Attempt to reconnect
                if (reconnectAttemptsRef.current < MAX_RECONNECT_ATTEMPTS) {
                    reconnectAttemptsRef.current++;
                    console.log(`Reconnecting... (attempt ${reconnectAttemptsRef.current}/${MAX_RECONNECT_ATTEMPTS})`);

                    reconnectTimeoutRef.current = setTimeout(() => {
                        connect();
                    }, RECONNECT_INTERVAL);
                } else {
                    setError('Max reconnection attempts reached');
                }
            };

            wsRef.current = ws;
        } catch (err) {
            console.error('Failed to create WebSocket:', err);
            setError('Failed to connect');
        }
    }, []);

    // Connect on mount
    useEffect(() => {
        connect();

        // Cleanup on unmount
        return () => {
            if (reconnectTimeoutRef.current) {
                clearTimeout(reconnectTimeoutRef.current);
            }
            if (wsRef.current) {
                wsRef.current.close();
            }
        };
    }, [connect]);

    // Send order via REST API (not WebSocket)
    const sendOrder = useCallback(async (side: 'buy' | 'sell', price: number, quantity: number) => {
        try {
            const response = await fetch(`${API_URL}/api/orders`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ side, price, quantity }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            console.log('Order placed:', result);
        } catch (err) {
            console.error('Failed to send order:', err);
            throw err;
        }
    }, []);

    return { data, isConnected, sendOrder, trades, error };
}
