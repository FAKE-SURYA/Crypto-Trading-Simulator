"""
Performance benchmarking script
Compares C++ SMA implementation vs pure Python implementation
"""

import time
import numpy as np
import sys
import os

# Add cpp_core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'cpp_core'))

try:
    import trade_engine
    CPP_AVAILABLE = True
except ImportError:
    CPP_AVAILABLE = False
    print("WARNING: C++ module not available. Install with: cd cpp_core && pip install .")


class PythonSMACalculator:
    """Pure Python SMA implementation for comparison"""
    
    def __init__(self, window_size):
        self.window_size = window_size
        self.prices = []
    
    def add_price(self, price):
        self.prices.append(price)
        if len(self.prices) > self.window_size:
            self.prices.pop(0)
    
    def get_sma(self):
        if not self.prices:
            return 0.0
        return sum(self.prices) / len(self.prices)


def benchmark_sma(calculator, num_iterations, name):
    """Benchmark SMA calculator"""
    prices = np.random.uniform(44000, 46000, num_iterations)
    
    start_time = time.perf_counter()
    
    for price in prices:
        calculator.add_price(price)
        _ = calculator.get_sma()
    
    end_time = time.perf_counter()
    elapsed = (end_time - start_time) * 1000  # Convert to ms
    
    print(f"{name:20} | {num_iterations:8} iterations | {elapsed:10.2f} ms | {elapsed/num_iterations:10.4f} ms/iter")
    
    return elapsed


def run_benchmarks():
    """Run performance benchmarks"""
    print("\n" + "=" * 80)
    print("High-Performance Crypto Trading Simulator - Performance Benchmarks")
    print("=" * 80)
    print()
    
    window_sizes = [20, 50, 100]
    iteration_counts = [1000, 10000, 100000]
    
    results = {
        'cpp': {},
        'python': {}
    }
    
    for window_size in window_sizes:
        print(f"\nWindow Size: {window_size}")
        print("-" * 80)
        print(f"{'Implementation':<20} | {'Iterations':^8} | {'Time (ms)':^10} | {'Time/Iter':^10}")
        print("-" * 80)
        
        for num_iter in iteration_counts:
            # Python implementation
            py_calc = PythonSMACalculator(window_size)
            py_time = benchmark_sma(py_calc, num_iter, f"Python (w={window_size})")
            results['python'][(window_size, num_iter)] = py_time
            
            # C++ implementation
            if CPP_AVAILABLE:
                cpp_calc = trade_engine.SMACalculator(window_size)
                cpp_time = benchmark_sma(cpp_calc, num_iter, f"C++ (w={window_size})")
                results['cpp'][(window_size, num_iter)] = cpp_time
                
                # Calculate speedup
                speedup = py_time / cpp_time
                print(f"{'Speedup':>20}   | {'':8} | {speedup:10.2f}x")
                print("-" * 80)
    
    # Summary
    if CPP_AVAILABLE:
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        
        all_speedups = []
        for key in results['python']:
            if key in results['cpp']:
                speedup = results['python'][key] / results['cpp'][key]
                all_speedups.append(speedup)
        
        if all_speedups:
            avg_speedup = np.mean(all_speedups)
            min_speedup = np.min(all_speedups)
            max_speedup = np.max(all_speedups)
            
            print(f"\nC++ Performance vs Python:")
            print(f"  Average Speedup: {avg_speedup:.2f}x faster")
            print(f"  Minimum Speedup: {min_speedup:.2f}x faster")
            print(f"  Maximum Speedup: {max_speedup:.2f}x faster")
            print()
            print("✓ C++ engine provides significant performance advantage!")
    
    print("\n" + "=" * 80)
    
    # Save results
    save_results(results)
    
    return results


def save_results(results):
    """Save benchmark results to CSV"""
    import csv
    from pathlib import Path
    
    output_file = Path(__file__).parent / "benchmark_results.csv"
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Window Size', 'Iterations', 'Python (ms)', 'C++ (ms)', 'Speedup'])
        
        for (window_size, iterations), py_time in results['python'].items():
            cpp_time = results['cpp'].get((window_size, iterations), 0)
            speedup = py_time / cpp_time if cpp_time > 0 else 0
            writer.writerow([window_size, iterations, f"{py_time:.2f}", f"{cpp_time:.2f}", f"{speedup:.2f}"])
    
    print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    if not CPP_AVAILABLE:
        print("\nPlease install the C++ module first:")
        print("  cd cpp_core")
        print("  pip install .")
        sys.exit(1)
    
    run_benchmarks()
