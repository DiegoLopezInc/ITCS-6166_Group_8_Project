# Simulation Overview and Research Paper Integration

## How the Simulation Works

1. **Network Topology (Mininet):**
   - Uses Mininet to create a **4-node star topology** (one switch, four hosts), simplifying the more complex topologies from the research papers.
   - Defined in `topology/star_topology.py`.

2. **SDN Controllers:**
   - Two multicast approaches are implemented as Ryu SDN controllers:
     - **Basic Multicast:** (`scripts/sdn_controller.py`) Implements a simple multicast forwarding strategy.
     - **Jasper-inspired Fair Multicast:** (`scripts/jasper_multicast_controller.py`) Implements fairness-aware multicast, inspired by Jasper’s algorithms.

3. **Traffic Generation:**
   - Financial data traffic is simulated using `scripts/traffic_generator.py`, mimicking the bursty, latency-sensitive flows in financial exchanges.

4. **Benchmarking & Comparison:**
   - The main script, `run_benchmark.py`, orchestrates the experiment:
     - Launches the topology and controllers.
     - Runs the traffic generator.
     - Measures performance (latency, fairness).
     - Uses `scripts/comparison_framework.py` to compare approaches and calculate metrics like **Jain’s Fairness Index**.

5. **Results:**
   - Outputs include latency statistics, fairness indices, and possibly plots/tables for comparison.

---

## Features Taken from the Three Research Papers

### 1. From “Multicast Optimization for SDNs in Financial Exchanges”
- **Financial Exchange Traffic Model:** The simulation uses a traffic generator that mimics the bursty, high-frequency, low-latency traffic found in financial exchanges.
- **Multicast in SDN:** The core problem is how to efficiently and fairly multicast data to multiple receivers in an SDN environment.
- **Performance Metrics:** Latency and fairness (Jain’s Index) are used as primary evaluation metrics.

### 2. From Jasper: Fair Multicast in SDN
- **Fair Multicast Algorithm:** The Jasper-inspired controller (`jasper_multicast_controller.py`) implements a fairness-aware multicast strategy, likely using tree-building or path selection logic that aims to balance delay among receivers.
- **Jain’s Fairness Index:** Used as a measure of fairness in delivery times across all receivers.

### 3. From the Third Paper (likely on SDN multicast/fairness)
- **Benchmarking Framework:** The simulation includes a comparison framework that can run multiple controller strategies and compare them systematically.
- **Topology Simplification:** While the original papers may use more complex topologies, this project adapts the ideas to a 4-node star for simplicity and reproducibility.

---

## Summary Table

| Paper Feature                                      | Incorporated in Project? | Where/How Used                           |
|----------------------------------------------------|:-----------------------:|------------------------------------------|
| Financial exchange multicast scenario              | Yes                     | Traffic generator, topology              |
| SDN-based multicast control                        | Yes                     | Both controllers (Ryu apps)              |
| Fairness-aware multicast (Jasper)                  | Yes                     | `jasper_multicast_controller.py`         |
| Jain’s Fairness Index for evaluation               | Yes                     | Comparison framework, benchmarking       |
| Topology adaptation for simulation                 | Yes                     | 4-node star topology                     |
| Performance benchmarking/plots                     | Yes                     | Output from `run_benchmark.py`           |

---

**For further details on the specific algorithms or a summary of the research papers, refer to the `paper_implementation` directory or request a summary.**
