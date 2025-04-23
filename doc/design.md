# Executive Summary

This project presents a mini-implementation of multicast optimization strategies for Software-Defined Networks (SDN) in financial exchange environments. The main objective is to simulate and compare the performance and fairness of different multicast approaches using a simplified star topology network.

**Key Features:**

- **4-Node Star Topology Simulation:**
  - Implements a star-shaped network topology with four nodes using Mininet, providing a simplified yet representative environment for multicast testing.

- **Multicast Approaches:**
  - **Basic Multicast:** A straightforward multicast method managed by a custom SDN controller.
  - **Jasper-Inspired Fair Multicast:** An advanced multicast technique inspired by the Jasper algorithm, designed to enhance fairness among receivers.
  - **DBO (Delivery-Clock-Based Ordering):** A multicast approach that uses logical delivery clocks for post-hoc fairness calculation, eliminating the need for global clock synchronization.

- **Performance Comparison Framework:**
  - Measures and compares multicast methods based on network latency and Jain's Fairness Index, providing quantitative insights into efficiency and fairness.

- **Financial Data Packet Generator:**
  - Simulates realistic financial exchange traffic to test multicast delivery under conditions similar to actual trading environments.

- **Benchmarking and Visualization:**
  - Includes scripts to automate benchmarking of both multicast strategies and visualize results for clear, actionable analysis.

This project provides a practical, time-bounded demonstration of SDN-based multicast optimization in financial networks, emphasizing both performance and fairness in data distribution.

# Research Paper Integration

This simulation incorporates key features from all three foundational research papers on multicast optimization in financial exchange networks:

- **CloudEx:**
  - Implements simulated clock synchronization and artificial message delays in the controllers, enabling experiments with fairness and latency trade-offs.
  - Supports dynamic delay adjustment and clock offset simulation for each receiver.

- **Jasper:**
  - Provides a Jasper-inspired multicast controller that builds dynamic multicast trees, uses hold-and-release buffers, and enforces fairness windows to synchronize delivery times across receivers.
  - Incorporates the core fairness algorithms and benchmarking metrics from the Jasper paper.

- **DBO (Delivery-Clock-Based Ordering):**
  - Includes a DBO-inspired controller that uses logical delivery clocks for post-hoc fairness calculation, eliminating the need for global clock synchronization.
  - Enables benchmarking of clockless fairness and deterministic delivery order.

The benchmarking framework and comparison scripts allow side-by-side evaluation of these approaches, measuring latency, fairness (Jain's Index), and delivery consistency. This comprehensive integration enables practical, reproducible experiments that highlight the strengths and trade-offs of each multicast strategy in a financial SDN context.