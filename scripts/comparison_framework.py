#!/usr/bin/env python
"""
Mini-Project: Multicast Optimization for SDN in Financial Exchanges
Comparison Framework for evaluating multicast approaches
"""

import numpy as np
import matplotlib.pyplot as plt
import time
import subprocess
import csv
import os

class FairnessComparator:
    def __init__(self):
        self.metrics = {
            'basic_multicast': {
                'latency': [],
                'fairness_index': [],
                'bandwidth_efficiency': []
            },
            'jasper_multicast': {
                'latency': [],
                'fairness_index': [],
                'bandwidth_efficiency': []
            },
            'dbo_multicast': {
                'latency': [],
                'fairness_index': [],
                'bandwidth_efficiency': [],
                'delivery_clock_fairness': [],
                'delivery_clock_window': []
            }
        }
        self.results_dir = 'results'
        # Ensure results directory exists
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)
        
    def run_benchmark(self, implementation, test_scenario):
        """
        Run a benchmark test for the given implementation and scenario
        
        Args:
            implementation: 'basic_multicast' or 'jasper_multicast' or 'dbo_multicast'
            test_scenario: Dict containing test parameters:
                - duration: Test duration in seconds
                - message_rate: Messages per second
                - message_size: Size of each message in bytes
        """
        print(f"Running benchmark for {implementation}...")
        
        # Start the controller according to implementation
        if implementation == 'basic_multicast':
            controller_cmd = "ryu-manager scripts/sdn_controller.py"
        elif implementation == 'jasper_multicast':
            controller_cmd = "ryu-manager scripts/jasper_multicast_controller.py"
        elif implementation == 'dbo_multicast':
            controller_cmd = "ryu-manager scripts/dbo_multicast_controller.py"
        else:
            raise ValueError(f"Unknown implementation: {implementation}")
        
        # Simulate latency measurements - in real implementation, this would come from actual network
        if implementation == 'dbo_multicast':
            latencies, delivery_clocks = self._simulate_dbo_latencies(test_scenario)
        else:
            latencies = self._simulate_latencies(implementation, test_scenario)
            delivery_clocks = None
        
        # Calculate metrics
        avg_latency = np.mean(latencies)
        fairness = self.calculate_jains_fairness(latencies)
        bandwidth_efficiency = self._simulate_bandwidth_efficiency(implementation)
        delivery_clock_fairness = None
        delivery_clock_window = None
        if implementation == 'dbo_multicast' and delivery_clocks is not None:
            delivery_clock_fairness = self.calculate_jains_fairness(delivery_clocks)
            delivery_clock_window = max(delivery_clocks) - min(delivery_clocks) if len(delivery_clocks) > 1 else 0.0
        
        # Record metrics
        self.metrics[implementation]['latency'].append(avg_latency)
        self.metrics[implementation]['fairness_index'].append(fairness)
        self.metrics[implementation]['bandwidth_efficiency'].append(bandwidth_efficiency)
        if implementation == 'dbo_multicast':
            self.metrics[implementation]['delivery_clock_fairness'].append(delivery_clock_fairness)
            self.metrics[implementation]['delivery_clock_window'].append(delivery_clock_window)
        
        print(f"Benchmark results for {implementation}:")
        print(f"  Average Latency: {avg_latency:.3f} ms")
        print(f"  Fairness Index: {fairness:.4f}")
        print(f"  Bandwidth Efficiency: {bandwidth_efficiency:.2f}%")
        if implementation == 'dbo_multicast':
            print(f"  Delivery Clock Fairness: {delivery_clock_fairness:.4f}")
            print(f"  Delivery Clock Window: {delivery_clock_window*1000:.2f} ms")
        
        # Save results to CSV
        self._save_results(implementation, test_scenario, {
            'avg_latency': avg_latency,
            'fairness': fairness,
            'bandwidth_efficiency': bandwidth_efficiency,
            'raw_latencies': latencies,
            'delivery_clocks': delivery_clocks,
            'delivery_clock_fairness': delivery_clock_fairness,
            'delivery_clock_window': delivery_clock_window
        })
        
        return {
            'avg_latency': avg_latency,
            'fairness': fairness,
            'bandwidth_efficiency': bandwidth_efficiency,
            'delivery_clock_fairness': delivery_clock_fairness,
            'delivery_clock_window': delivery_clock_window
        }
    
    def _simulate_latencies(self, implementation, test_scenario):
        """Simulate latencies for the given implementation"""
        # Number of hosts in our star topology
        num_hosts = 4
        
        # Base latency in milliseconds
        base_latency = 1.0
        
        # Generate latencies with different patterns based on implementation
        if implementation == 'basic_multicast':
            # Basic multicast tends to have more variance in latencies
            latencies = [base_latency + np.random.exponential(0.5) for _ in range(num_hosts)]
        else:  # jasper_multicast
            # Jasper should have more consistent latencies due to fairness optimization
            # Still some variance but less than basic
            latencies = [base_latency + np.random.normal(0.2, 0.1) for _ in range(num_hosts)]
            
        return latencies
    
    def _simulate_dbo_latencies(self, test_scenario):
        """
        Simulate DBO-inspired delivery: no clock sync, use logical delivery clocks
        Returns both observed latencies and logical delivery clocks.
        """
        num_hosts = 4
        base_latency = 1.0
        # Simulate random network latency for each host
        raw_latencies = [base_latency + np.random.uniform(0.0, 1.0) for _ in range(num_hosts)]
        # Logical delivery clock for each host (arrival time minus min arrival)
        min_arrival = min(raw_latencies)
        delivery_clocks = [lat - min_arrival for lat in raw_latencies]
        return raw_latencies, delivery_clocks
    
    def _simulate_bandwidth_efficiency(self, implementation):
        """Simulate bandwidth efficiency for the given implementation"""
        # Basic efficiency percentages
        if implementation == 'basic_multicast':
            # Basic multicast tends to be less efficient
            return 70.0 + np.random.normal(0, 5.0)
        elif implementation == 'jasper_multicast':
            # Jasper should be more efficient
            return 85.0 + np.random.normal(0, 3.0)
        else:  # dbo_multicast
            # DBO should be more efficient
            return 90.0 + np.random.normal(0, 2.0)
    
    def _save_results(self, implementation, test_scenario, results):
        """Save benchmark results to CSV file"""
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"{self.results_dir}/{implementation}_{timestamp}.csv"
        
        # Write test parameters and results
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Parameter', 'Value'])
            writer.writerow(['Implementation', implementation])
            for key, value in test_scenario.items():
                writer.writerow([key, value])
            writer.writerow(['Average Latency (ms)', results['avg_latency']])
            writer.writerow(['Fairness Index', results['fairness']])
            writer.writerow(['Bandwidth Efficiency (%)', results['bandwidth_efficiency']])
            if implementation == 'dbo_multicast':
                writer.writerow(['Delivery Clock Fairness', results['delivery_clock_fairness']])
                writer.writerow(['Delivery Clock Window (ms)', results['delivery_clock_window'] * 1000 if results['delivery_clock_window'] is not None else None])
            
            # Write raw latencies
            writer.writerow([])
            writer.writerow(['Host', 'Latency (ms)'])
            for i, latency in enumerate(results['raw_latencies']):
                writer.writerow([f'h{i+1}', latency])
            
            if implementation == 'dbo_multicast' and results['delivery_clocks'] is not None:
                writer.writerow([])
                writer.writerow(['Host', 'Delivery Clock (ms)'])
                for i, clock in enumerate(results['delivery_clocks']):
                    writer.writerow([f'h{i+1}', clock * 1000])
        
        print(f"Results saved to {filename}")
        
    def calculate_jains_fairness(self, latencies):
        """
        Calculate Jain's fairness index for the given latencies
        
        Jain's Fairness Index = (sum(x_i))^2 / (n * sum(x_i^2))
        - Result ranges from 1/n (worst case) to 1 (best case)
        - Value of 1 means all latencies are equal
        """
        if not latencies:
            return 0.0
            
        n = len(latencies)
        sum_latencies = sum(latencies)
        sum_squared = sum(x**2 for x in latencies)
        
        if sum_squared == 0:
            return 1.0  # All values are 0, perfect fairness
            
        return (sum_latencies**2) / (n * sum_squared)
        
    def plot_comparison(self):
        """Generate comparative visualizations of the benchmark results"""
        implementations = list(self.metrics.keys())
        
        # Create figure with subplots
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
        
        # Plot average latency
        latencies = [np.mean(self.metrics[impl]['latency']) for impl in implementations]
        ax1.bar(implementations, latencies)
        ax1.set_title('Average Latency')
        ax1.set_ylabel('Latency (ms)')
        ax1.set_ylim(bottom=0)
        
        # Plot fairness index
        fairness = [np.mean(self.metrics[impl]['fairness_index']) for impl in implementations]
        ax2.bar(implementations, fairness)
        ax2.set_title('Jain\'s Fairness Index')
        ax2.set_ylim(0, 1)
        
        # Plot bandwidth efficiency
        bw_efficiency = [np.mean(self.metrics[impl]['bandwidth_efficiency']) for impl in implementations]
        ax3.bar(implementations, bw_efficiency)
        ax3.set_title('Bandwidth Efficiency')
        ax3.set_ylabel('Efficiency (%)')
        ax3.set_ylim(0, 100)
        
        plt.tight_layout()
        
        # Save the plot
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        plot_path = f"{self.results_dir}/comparison_{timestamp}.png"
        plt.savefig(plot_path)
        
        print(f"Comparison plot saved to {plot_path}")
        return plot_path