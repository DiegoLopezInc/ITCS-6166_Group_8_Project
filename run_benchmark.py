#!/usr/bin/env python
"""
Mini-Project: Multicast Optimization for SDN in Financial Exchanges
Main Benchmark Runner Script

This script ties together all components and runs a complete benchmark
comparing basic multicast vs. Jasper-inspired multicast approaches.
"""

import os
import sys
import time
import argparse
from scripts.comparison_framework import FairnessComparator

def run_full_benchmark(test_scenarios=None):
    """
    Run a complete benchmark comparing both multicast implementations
    
    Args:
        test_scenarios: List of test scenarios to run. If None, default scenarios will be used.
    """
    if test_scenarios is None:
        # Define default test scenarios
        test_scenarios = [
            {
                'name': 'Low Rate',
                'duration': 10,
                'message_rate': 10,  # 10 messages per second
                'message_size': 100  # 100 bytes per message
            },
            {
                'name': 'High Rate',
                'duration': 10,
                'message_rate': 100,  # 100 messages per second
                'message_size': 100   # 100 bytes per message
            },
            {
                'name': 'Large Message',
                'duration': 10,
                'message_rate': 10,   # 10 messages per second
                'message_size': 1000  # 1000 bytes per message
            },
            {
                'name': 'High Frequency',
                'duration': 10,
                'message_rate': 200,  # 200 messages per second
                'message_size': 100   # 100 bytes per message
            }
        ]
    
    print("====================================================")
    print("Mini-Project: Multicast Optimization Benchmark Suite")
    print("====================================================")
    print(f"Running {len(test_scenarios)} test scenarios")
    
    # Create the comparator
    comparator = FairnessComparator()
    
    # Run benchmarks for each scenario and each implementation
    for scenario in test_scenarios:
        print("\n" + "=" * 40)
        print(f"Test Scenario: {scenario['name']}")
        print("=" * 40)
        
        # Test all implementations with this scenario
        for implementation in ['basic_multicast', 'jasper_multicast', 'dbo_multicast']:
            comparator.run_benchmark(implementation, scenario)
            
            # Small delay between tests
            time.sleep(1)
    
    # Generate comparison plots
    print("\nGenerating comparison visualizations...")
    plot_path = comparator.plot_comparison()
    
    print("\n====================================================")
    print("Benchmark Summary:")
    print("====================================================")
    
    # Calculate average metrics across all test scenarios
    implementations = list(comparator.metrics.keys())
    for impl in implementations:
        avg_latency = sum(comparator.metrics[impl]['latency']) / len(comparator.metrics[impl]['latency'])
        avg_fairness = sum(comparator.metrics[impl]['fairness_index']) / len(comparator.metrics[impl]['fairness_index'])
        avg_efficiency = sum(comparator.metrics[impl]['bandwidth_efficiency']) / len(comparator.metrics[impl]['bandwidth_efficiency'])
        
        print(f"\n{impl.upper()}:")
        print(f"  Average Latency: {avg_latency:.3f} ms")
        print(f"  Average Fairness Index: {avg_fairness:.4f}")
        print(f"  Average Bandwidth Efficiency: {avg_efficiency:.2f}%")
    
    print(f"\nResults saved to results directory. Comparison plot: {plot_path}")
    
    return plot_path

def main():
    """Main function for standalone usage"""
    parser = argparse.ArgumentParser(description='Multicast Optimization Benchmark Suite')
    parser.add_argument('--scenarios', type=int, default=4, help='Number of test scenarios to run (1-4)')
    
    args = parser.parse_args()
    
    # Limit the number of scenarios based on user input
    num_scenarios = min(max(1, args.scenarios), 4)
    
    # Define default test scenarios
    all_scenarios = [
        {
            'name': 'Low Rate',
            'duration': 10,
            'message_rate': 10,
            'message_size': 100
        },
        {
            'name': 'High Rate',
            'duration': 10,
            'message_rate': 100,
            'message_size': 100
        },
        {
            'name': 'Large Message',
            'duration': 10,
            'message_rate': 10,
            'message_size': 1000
        },
        {
            'name': 'High Frequency',
            'duration': 10,
            'message_rate': 200,
            'message_size': 100
        }
    ]
    
    # Use only the requested number of scenarios
    selected_scenarios = all_scenarios[:num_scenarios]
    
    # Run the benchmark
    run_full_benchmark(selected_scenarios)

if __name__ == '__main__':
    main()
