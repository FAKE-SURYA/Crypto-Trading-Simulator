'use client';

import { useState } from 'react';
import styles from './TradingPanel.module.css';

interface TradingPanelProps {
    currentPrice: number;
    onSubmitOrder: (side: 'buy' | 'sell', price: number, quantity: number) => Promise<void>;
}

export default function TradingPanel({ currentPrice, onSubmitOrder }: TradingPanelProps) {
    const [side, setSide] = useState<'buy' | 'sell'>('buy');
    const [price, setPrice] = useState('');
    const [quantity, setQuantity] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        const priceNum = parseFloat(price);
        const quantityNum = parseFloat(quantity);

        if (isNaN(priceNum) || priceNum <= 0) {
            setMessage({ type: 'error', text: 'Please enter a valid price' });
            return;
        }

        if (isNaN(quantityNum) || quantityNum <= 0) {
            setMessage({ type: 'error', text: 'Please enter a valid quantity' });
            return;
        }

        setIsSubmitting(true);
        setMessage(null);

        try {
            await onSubmitOrder(side, priceNum, quantityNum);
            setMessage({ type: 'success', text: `${side.toUpperCase()} order placed successfully!` });

            // Clear form
            setPrice('');
            setQuantity('');

            // Clear success message after 3 seconds
            setTimeout(() => setMessage(null), 3000);
        } catch (error) {
            setMessage({ type: 'error', text: 'Failed to place order. Please try again.' });
        } finally {
            setIsSubmitting(false);
        }
    };

    const setMarketPrice = () => {
        if (currentPrice > 0) {
            setPrice(currentPrice.toFixed(2));
        }
    };

    return (
        <div className={styles.container}>
            <h4 className={styles.title}>Place Order</h4>

            <form onSubmit={handleSubmit} className={styles.form}>
                {/* Order Side Selector */}
                <div className={styles.sideSelector}>
                    <button
                        type="button"
                        className={`${styles.sideButton} ${side === 'buy' ? styles.sideButtonActive : ''} ${styles.buyButton}`}
                        onClick={() => setSide('buy')}
                    >
                        Buy
                    </button>
                    <button
                        type="button"
                        className={`${styles.sideButton} ${side === 'sell' ? styles.sideButtonActive : ''} ${styles.sellButton}`}
                        onClick={() => setSide('sell')}
                    >
                        Sell
                    </button>
                </div>

                {/* Price Input */}
                <div className={styles.field}>
                    <label className="label">
                        Price (USD)
                        {currentPrice > 0 && (
                            <button
                                type="button"
                                onClick={setMarketPrice}
                                className={styles.marketButton}
                            >
                                Use Market: ${currentPrice.toFixed(2)}
                            </button>
                        )}
                    </label>
                    <input
                        type="number"
                        step="0.01"
                        className="input"
                        value={price}
                        onChange={(e) => setPrice(e.target.value)}
                        placeholder="Enter price"
                        required
                    />
                </div>

                {/* Quantity Input */}
                <div className={styles.field}>
                    <label className="label">Quantity (BTC)</label>
                    <input
                        type="number"
                        step="0.0001"
                        className="input"
                        value={quantity}
                        onChange={(e) => setQuantity(e.target.value)}
                        placeholder="Enter quantity"
                        required
                    />
                </div>

                {/* Total Display */}
                {price && quantity && (
                    <div className={styles.total}>
                        <span>Total:</span>
                        <span className={styles.totalValue}>
                            ${(parseFloat(price) * parseFloat(quantity)).toFixed(2)}
                        </span>
                    </div>
                )}

                {/* Submit Button */}
                <button
                    type="submit"
                    className={`button ${side === 'buy' ? 'button-success' : 'button-danger'} ${styles.submitButton}`}
                    disabled={isSubmitting}
                >
                    {isSubmitting ? 'Placing Order...' : `Place ${side.toUpperCase()} Order`}
                </button>

                {/* Message Display */}
                {message && (
                    <div className={`${styles.message} ${styles[message.type]}`}>
                        {message.text}
                    </div>
                )}
            </form>
        </div>
    );
}
