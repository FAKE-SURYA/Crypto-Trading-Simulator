'use client';

import { useEffect, useState } from 'react';
import { useWebSocket } from '@/hooks/useWebSocket';
import PriceChart from '@/components/PriceChart';
import OrderBook from '@/components/OrderBook';
import TradingPanel from '@/components/TradingPanel';
import { PricePoint, OrderBook as OrderBookType } from '@/types/api';
import styles from './page.module.css';

const API_URL = process.env.NEXT_PUBLIC_API_URL;


export default function Home() {
    const { data, isConnected, sendOrder, trades, error } = useWebSocket();
    const [priceHistory, setPriceHistory] = useState<PricePoint[]>([]);
    const [orderbook, setOrderbook] = useState<OrderBookType>({ bids: [], asks: [] });
    const [currentPrice, setCurrentPrice] = useState(0);

    useEffect(() => {
        if (data) {
            // Update price history for chart
            setPriceHistory(prev => {
                const newPoint: PricePoint = {
                    timestamp: data.timestamp,
                    price: data.price,
                    sma: data.sma,
                };
                const updated = [...prev, newPoint];
                // Keep last 100 points
                return updated.slice(-100);
            });

            // Update order book
            setOrderbook(data.orderbook);

            // Update current price
            setCurrentPrice(data.price);
        }
    }, [data]);

    const handleSubmitOrder = async (side: 'buy' | 'sell', price: number, quantity: number) => {
        await sendOrder(side, price, quantity);
    };

    return (
        <main className={styles.main}>
            {/* Header */}
            <header className={styles.header}>
                <div className={styles.headerLeft}>
                    <h1 className={styles.title}>
                        ⚡ Crypto Trading Simulator
                    </h1>
                    <p className={styles.subtitle}>High-Performance C++ Engine</p>
                </div>

                <div className={styles.headerRight}>
                    {/* Connection Status */}
                    <div className={`status-indicator ${isConnected ? 'status-connected' : 'status-disconnected'}`}>
                        <div className="status-dot"></div>
                        {isConnected ? 'Connected' : 'Disconnected'}
                    </div>

                    {/* Current Price Display */}
                    {currentPrice > 0 && (
                        <div className={styles.priceDisplay}>
                            <span className={styles.priceLabel}>BTC/USD</span>
                            <span className={styles.priceValue}>${currentPrice.toFixed(2)}</span>
                        </div>
                    )}
                </div>
            </header>

            {/* Error Display */}
            {error && (
                <div className={styles.errorBanner}>
                    ⚠️ {error} - Check that the backend is running on port 8000
                </div>
            )}

            {/* Main Grid Layout */}
            <div className={styles.grid}>
                {/* Price Chart - Spans 2 columns */}
                <div className={`card ${styles.chartCard}`}>
                    <div className={styles.cardHeader}>
                        <h3>Market Price & SMA</h3>
                        <div className={styles.chartInfo}>
                            <span className={styles.chartLegend}>
                                <span style={{ color: '#3b82f6' }}>●</span> Real-time Price
                            </span>
                            <span className={styles.chartLegend}>
                                <span style={{ color: '#f59e0b' }}>●</span> C++ SMA (20-period)
                            </span>
                        </div>
                    </div>
                    <PriceChart data={priceHistory} />
                </div>

                {/* Order Book */}
                <div className={`card ${styles.orderbookCard}`}>
                    <OrderBook orderbook={orderbook} />
                </div>

                {/* Trading Panel */}
                <div className={`card ${styles.tradingCard}`}>
                    <TradingPanel
                        currentPrice={currentPrice}
                        onSubmitOrder={handleSubmitOrder}
                    />
                </div>

                {/* Recent Trades */}
                {trades.length > 0 && (
                    <div className={`card ${styles.tradesCard}`}>
                        <h4 className={styles.tradesTitle}>Recent Trades</h4>
                        <div className={styles.tradesList}>
                            {trades.slice(0, 10).map((trade, index) => (
                                <div key={index} className={styles.tradeItem}>
                                    <span className={styles.tradePrice}>${trade.price.toFixed(2)}</span>
                                    <span className={styles.tradeQty}>{trade.quantity.toFixed(4)} BTC</span>
                                    <span className={styles.tradeTime}>
                                        {new Date(trade.timestamp).toLocaleTimeString()}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>

            {/* Footer */}
            <footer className={styles.footer}>
                <p>
                    Built with <span style={{ color: '#ef4444' }}>♥</span> using C++17, Python FastAPI, and Next.js |
                    <a href="https://github.com" target="_blank" rel="noopener noreferrer"> View on GitHub</a>
                </p>
            </footer>
        </main>
    );
}
