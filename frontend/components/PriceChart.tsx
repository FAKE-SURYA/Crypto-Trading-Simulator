'use client';

import { useMemo } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { PricePoint } from '@/types/api';

interface PriceChartProps {
    data: PricePoint[];
}

export default function PriceChart({ data }: PriceChartProps) {
    // Format data for Recharts
    const chartData = useMemo(() => {
        return data.map((point, index) => ({
            index,
            time: new Date(point.timestamp * 1000).toLocaleTimeString(),
            price: point.price,
            sma: point.sma > 0 ? point.sma : null, // Only show SMA when available
        }));
    }, [data]);

    // Custom tooltip
    const CustomTooltip = ({ active, payload }: any) => {
        if (active && payload && payload.length) {
            return (
                <div style={{
                    background: 'rgba(26, 29, 46, 0.95)',
                    padding: '12px',
                    border: '1px solid rgba(148, 163, 184, 0.2)',
                    borderRadius: '8px',
                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.3)',
                }}>
                    <p style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '4px' }}>
                        {payload[0].payload.time}
                    </p>
                    <p style={{ color: '#3b82f6', fontWeight: '600', margin: '4px 0' }}>
                        Price: ${payload[0].value?.toFixed(2) || 'N/A'}
                    </p>
                    {payload[1] && payload[1].value && (
                        <p style={{ color: '#f59e0b', fontWeight: '600', margin: '4px 0' }}>
                            SMA: ${payload[1].value.toFixed(2)}
                        </p>
                    )}
                </div>
            );
        }
        return null;
    };

    if (data.length === 0) {
        return (
            <div style={{
                height: '400px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#64748b'
            }}>
                <p>Waiting for market data...</p>
            </div>
        );
    }

    return (
        <ResponsiveContainer width="100%" height={400}>
            <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <defs>
                    <linearGradient id="priceGradient" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                        <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="smaGradient" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.2} />
                        <stop offset="95%" stopColor="#f59e0b" stopOpacity={0} />
                    </linearGradient>
                </defs>

                <CartesianGrid
                    strokeDasharray="3 3"
                    stroke="rgba(148, 163, 184, 0.1)"
                    vertical={false}
                />

                <XAxis
                    dataKey="time"
                    stroke="#64748b"
                    style={{ fontSize: '0.75rem' }}
                    tickLine={false}
                />

                <YAxis
                    stroke="#64748b"
                    style={{ fontSize: '0.75rem' }}
                    tickFormatter={(value) => `$${value.toFixed(0)}`}
                    tickLine={false}
                    domain={['dataMin - 50', 'dataMax + 50']}
                />

                <Tooltip content={<CustomTooltip />} />

                <Legend
                    wrapperStyle={{ fontSize: '0.875rem', paddingTop: '20px' }}
                    iconType="line"
                />

                <Line
                    type="monotone"
                    dataKey="price"
                    stroke="#3b82f6"
                    strokeWidth={2}
                    dot={false}
                    fill="url(#priceGradient)"
                    name="Market Price"
                    animationDuration={300}
                />

                <Line
                    type="monotone"
                    dataKey="sma"
                    stroke="#f59e0b"
                    strokeWidth={2}
                    dot={false}
                    fill="url(#smaGradient)"
                    name="SMA (C++ Calculated)"
                    animationDuration={300}
                    strokeDasharray="5 5"
                />
            </LineChart>
        </ResponsiveContainer>
    );
}
