'use client';

import { OrderBook as OrderBookType } from '@/types/api';
import styles from './OrderBook.module.css';

interface OrderBookProps {
    orderbook: OrderBookType;
}

export default function OrderBook({ orderbook }: OrderBookProps) {
    const { bids, asks } = orderbook;

    // Take top 5 of each
    const topAsks = asks.slice(0, 5).reverse(); // Reverse to show highest ask at bottom
    const topBids = bids.slice(0, 5);

    const formatPrice = (price: number) => price.toFixed(2);
    const formatQuantity = (qty: number) => qty.toFixed(4);
    const formatTotal = (price: number, qty: number) => (price * qty).toFixed(2);

    return (
        <div className={styles.container}>
            <h4 className={styles.title}>Order Book</h4>

            {/* Asks (Sell Orders) */}
            <div className={styles.section}>
                <div className={styles.header}>
                    <span>Price (USD)</span>
                    <span>Quantity (BTC)</span>
                    <span>Total</span>
                </div>

                <div className={styles.asks}>
                    {topAsks.length > 0 ? (
                        topAsks.map(([price, quantity], index) => (
                            <div key={`ask-${index}`} className={`${styles.row} ${styles.askRow}`}>
                                <span className={styles.price}>${formatPrice(price)}</span>
                                <span className={styles.quantity}>{formatQuantity(quantity)}</span>
                                <span className={styles.total}>${formatTotal(price, quantity)}</span>
                            </div>
                        ))
                    ) : (
                        <div className={styles.empty}>No asks</div>
                    )}
                </div>
            </div>

            {/* Spread */}
            {bids.length > 0 && asks.length > 0 && (
                <div className={styles.spread}>
                    <span className={styles.spreadLabel}>Spread:</span>
                    <span className={styles.spreadValue}>
                        ${(asks[0][0] - bids[0][0]).toFixed(2)}
                    </span>
                </div>
            )}

            {/* Bids (Buy Orders) */}
            <div className={styles.section}>
                <div className={styles.bids}>
                    {topBids.length > 0 ? (
                        topBids.map(([price, quantity], index) => (
                            <div key={`bid-${index}`} className={`${styles.row} ${styles.bidRow}`}>
                                <span className={styles.price}>${formatPrice(price)}</span>
                                <span className={styles.quantity}>{formatQuantity(quantity)}</span>
                                <span className={styles.total}>${formatTotal(price, quantity)}</span>
                            </div>
                        ))
                    ) : (
                        <div className={styles.empty}>No bids</div>
                    )}
                </div>
            </div>
        </div>
    );
}
