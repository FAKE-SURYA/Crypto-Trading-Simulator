"""
Plot benchmark results
Creates professional visualization of performance comparison
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path

# Use non-interactive backend for headless environments
matplotlib.use('Agg')


def plot_benchmark_results():
    """Create visualization of benchmark results"""
    csv_file = Path(__file__).parent / "benchmark_results.csv"
    
    if not csv_file.exists():
        print(f"Error: {csv_file} not found. Run sma_benchmark.py first.")
        return
    
    # Read data
    df = pd.read_csv(csv_file)
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('C++ vs Python SMA Performance Comparison', fontsize=16, fontweight='bold')
    
    # Plot 1: Execution Time Comparison
    window_sizes = df['Window Size'].unique()
    x = range(len(df))
    width = 0.35
    
    ax1.bar([i - width/2 for i in x], df['Python (ms)'], width, label='Python', color='#ef4444', alpha=0.8)
    ax1.bar([i + width/2 for i in x], df['C++ (ms)'], width, label='C++', color='#3b82f6', alpha=0.8)
    
    ax1.set_xlabel('Test Configuration (Window Size, Iterations)', fontweight='bold')
    ax1.set_ylabel('Execution Time (ms, log scale)', fontweight='bold')
    ax1.set_title('Execution Time Comparison')
    ax1.set_yscale('log')
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Set x-axis labels
    labels = [f"W={row['Window Size']}, N={row['Iterations']}" for _, row in df.iterrows()]
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=45, ha='right', fontsize=8)
    
    # Plot 2: Speedup Factor
    ax2.bar(x, df['Speedup'], color='#10b981', alpha=0.8)
    ax2.axhline(y=1, color='r', linestyle='--', linewidth=2, label='No Speedup', alpha=0.5)
    
    ax2.set_xlabel('Test Configuration (Window Size, Iterations)', fontweight='bold')
    ax2.set_ylabel('Speedup Factor (x faster)', fontweight='bold')
    ax2.set_title('C++ Performance Advantage')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Set x-axis labels
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, rotation=45, ha='right', fontsize=8)
    
    # Add average speedup annotation
    avg_speedup = df['Speedup'].mean()
    ax2.text(0.5, 0.95, f'Average Speedup: {avg_speedup:.1f}x',
             transform=ax2.transAxes, fontsize=12, fontweight='bold',
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    # Save figure
    output_file = Path(__file__).parent / "performance_comparison.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ Performance chart saved to: {output_file}")
    
    # Also save a simple text summary
    summary_file = Path(__file__).parent / "benchmark_summary.txt"
    with open(summary_file, 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("PERFORMANCE BENCHMARK SUMMARY\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Average C++ Speedup: {avg_speedup:.2f}x faster than Python\n")
        f.write(f"Minimum Speedup: {df['Speedup'].min():.2f}x\n")
        f.write(f"Maximum Speedup: {df['Speedup'].max():.2f}x\n\n")
        f.write("Detailed Results:\n")
        f.write("-" * 60 + "\n")
        f.write(df.to_string(index=False))
    
    print(f"✓ Summary saved to: {summary_file}")


if __name__ == "__main__":
    # Install matplotlib and pandas if needed
    try:
        plot_benchmark_results()
    except ImportError as e:
        print(f"Error: {e}")
        print("\nInstall required packages:")
        print("  pip install matplotlib pandas")
