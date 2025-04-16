# ITCS-6166_Group_8_Project  
**Multicast Optimization for Software-Defined Networks in Financial Exchanges**    
Group #8: 
- Diego Lopez (dlopez18@charlotte.edu)
- Khushi Arvindbhai Kalathiya (kkalathi@charlotte.edu)
- Sach Denuwara (sdenuwar@charlotte.edu)
- Thomas Macdougall (tmacdoug@charlotte.edu)

Submission Date: March 31, 2025  
---

### 2. Project Abstract  
This project aims to develop a simplified simulation to model and optimize a software-defined network (SDN) for financial exchanges, integrating basic multicast techniques inspired by Jasper. The core functionalities include creating a small virtual SDN topology, implementing a simplified multicast optimization algorithm for fair and low-latency data delivery, and comparing this with a basic multicast approach. The intended outcome is a mini-simulation demonstrating how multicast enhancements can improve bandwidth efficiency, reduce latency, and ensure fairness in financial systems.

---

### 3. Progress Summary  
This project has been scaled down to a 4-hour mini-implementation that focuses on the essential components of multicast optimization for financial exchanges. The simplified approach includes a 4-node topology in Mininet with a basic OpenFlow controller, two multicast implementations (basic and Jasper-inspired), and performance comparison measuring latency and Jain's Fairness Index.

---

### 4. Mini-Project Scope

#### 1. Simplified Network Simulation
- Create a **4-node topology** in Mininet (instead of 8-node)
- Implement a basic OpenFlow controller with Ryu
- Focus on a star topology (simpler than ring)

#### 2. Streamlined Multicast Implementation
- Implement **only 2 multicast approaches** (instead of 3):
  - Basic multicast (baseline)
  - Jasper-inspired fair multicast optimization

#### 3. Basic Performance Comparison
- Measure only key metrics:
  - Latency
  - Jain's Fairness Index
- Generate simple financial data packets for testing

#### 4. Minimalist Visualization
- Command-line output of results
- Simple Matplotlib bar charts comparing approaches

---

### 5. Implementation Plan (4 Hours)

| Time | Task |
|------|------|
| 0:00-0:30 | Setup Mininet environment and install dependencies |
| 0:30-1:15 | Create 4-node topology script with basic SDN controller |
| 1:15-2:15 | Implement basic multicast and Jasper-inspired approaches |
| 2:15-3:00 | Create simple traffic generator and benchmark script |
| 3:00-3:45 | Implement comparison with latency and fairness metrics |
| 3:45-4:00 | Final testing and documentation |

---

### 6. Additional Notes  
To simulate the network, we are using Mininet to create a virtual SDN with a 4-node star topology, where each node represents an optical switch managed by an SDN controller (Ryu). The digital twin is implemented as a Python script that mirrors the network’s real-time state (e.g., link utilization, latency), updated via OpenFlow messages from Mininet. Multicast optimization, inspired by Jasper, is coded as a tree-building algorithm within the controller, distributing synthetic financial data to all nodes. We plan to measure performance metrics such as end-to-end delay, jitter, and fairness, comparing Jasper’s approach with a basic multicast approach, and visualize results using Matplotlib. The team, meets twice weekly to ensure steady progress. We’d appreciate instructor feedback on the simulation’s realism, traffic design, and fairness comparison scope in the future.

### 6.1 Simulation Approach Explained  
1. **Tool Selection**: Mininet is chosen for its ability to emulate SDN environments, extended with Ryu for controller logic. Mininet’s flexibility allows us to approximate SDN behavior.
2. **Topology**: A 4-node star topology mimics a small-scale exchange network, with high-bandwidth links (e.g., 10 Gbps) and low latency (e.g., 1 ms) to simulate realistic network conditions.
3. **Digital Twin**: A Python script queries Mininet via OpenFlow to track network state (e.g., bandwidth usage, queue lengths), serving as the digital twin for real-time monitoring and optimization.
4. **Multicast Implementation**: Adapt Jasper’s multicast tree algorithm, coded in Python, to distribute financial data fairly across nodes, tested with iperf-generated traffic.
5. **Testing**: Synthetic financial traffic (e.g., stock updates) is injected, and a basic multicast approach is simulated for comparison, measuring latency, jitter, and fairness.
6. **Visualization**: Matplotlib will plot results, aiding in performance analysis.

---

### 7. Running the Project for Testing

#### Prerequisites
- This project requires Mininet, which typically runs on Linux (Ubuntu is recommended)
- Python 3.6 or higher

#### Step-by-Step Guide

##### 1. Install Dependencies
First, install all the required dependencies:
```bash
pip install -r requirements.txt
```

##### 2. Start the SDN Controller
In one terminal window, start the Ryu SDN controller. You can choose either the basic or Jasper-inspired controller:

For basic multicast:
```bash
ryu-manager scripts/sdn_controller.py
```

Or for Jasper-inspired multicast:
```bash
ryu-manager scripts/jasper_multicast_controller.py
```

##### 3. Launch the Mininet Topology
In a second terminal window, start the Mininet topology:
```bash
sudo python topology/star_topology.py
```
This will create a 4-node star topology and connect to the controller you started in step 2.

##### 4. Generate Traffic
In the Mininet CLI (which opens after starting the topology), you can generate traffic from one of the hosts:
```
mininet> h1 python scripts/traffic_generator.py --count 100 --rate 10
```
This will send 100 multicast messages at a rate of 10 per second.

##### 5. Run Full Benchmark (Alternative)
Alternatively, instead of steps 2-4, you can run the full automated benchmark which will test both controllers with different scenarios:
```bash
python run_benchmark.py
```

##### 6. View Results
The benchmark results will be saved in the `results` directory:
- CSV files with detailed metrics
- PNG image with comparison charts

#### Troubleshooting
- If you encounter permission issues with Mininet, make sure to run it with sudo
- Ensure that the controller is running before starting the Mininet topology
- If port conflicts occur, you may need to kill any existing Mininet processes: `sudo mn -c`

---

## Project Overview
This mini-project simulates and compares multicast optimization strategies for software-defined networks (SDN) in financial exchanges. It is based on key ideas from CloudEx, Jasper, and DBO research papers, using a 4-node star topology in Mininet and a suite of SDN controllers and benchmarking tools.

## Key Features
- **Topologies:** 4-node star topology in Mininet
- **Multicast Approaches:**
  - Basic Multicast (CloudEx-inspired, with clock sync and artificial delays)
  - Jasper-inspired Fair Multicast (dynamic multicast tree, hold-and-release)
  - DBO-inspired Clockless Fair Multicast (logical delivery clocks, post-hoc fairness)
- **Performance Metrics:**
  - End-to-end latency
  - Jain's Fairness Index
  - Bandwidth efficiency
  - Fairness window (max delivery time difference)
  - Delivery clock fairness (DBO mode)
- **Traffic Generation:** Simulated financial data packets
- **Benchmarking:** Unified framework for running and comparing all approaches

## File Structure
- `topology/star_topology.py`: Mininet topology definition
- `scripts/sdn_controller.py`: Basic SDN controller (CloudEx-inspired)
- `scripts/jasper_multicast_controller.py`: Jasper-inspired fair multicast controller
- `scripts/dbo_multicast_controller.py`: DBO-inspired controller (simulation logic in framework)
- `scripts/comparison_framework.py`: Benchmarking and comparison framework
- `scripts/traffic_generator.py`: Financial exchange traffic generator
- `run_benchmark.py`: Main script to run all benchmarks
- `requirements.txt`: Dependencies

## How to Run Experiments
1. **Setup:**
   - Install dependencies: `pip install -r requirements.txt`
   - Ensure Mininet and Ryu are installed and working
2. **Run Benchmarks:**
   - Execute `python run_benchmark.py` to run all modes (basic, jasper, dbo)
   - Results and plots are saved in the `results/` directory
3. **Customize Experiments:**
   - Edit `scripts/comparison_framework.py` to change test scenarios (duration, rate, message size)
   - Use setter methods in controllers to adjust delay, clock sync error, or fairness deadlines

## Research Paper Features
- **CloudEx:** Simulated clock synchronization, artificial delays, dynamic delay adjustment
- **Jasper:** Dynamic multicast tree, hold-and-release, fairness window
- **DBO:** Clockless fairness, logical delivery clocks, post-hoc ordering

## Metrics & Plots
- Average latency
- Jain's Fairness Index
- Bandwidth efficiency
- Fairness window (ms)
- Delivery clock fairness (DBO)

## References
- [CloudEx: A Fair-Access Financial Exchange in the Cloud]
- [Jasper: Scalable and Fair Multicast for Financial Exchanges in the Cloud]
- [DBO: Fairness for Cloud-Hosted Financial Exchanges]

## Contributors
- [Your Name]

---

### 8. References  
- **arXiv Paper**: "Jasper: Scalable and Fair Multicast for Financial Exchanges in the Cloud" (https://arxiv.org/html/2402.09527v1#S10) – Core inspiration for multicast tree design and fairness in cloud environments.
- **Mininet Documentation**: Guided simulation environment setup and topology design (http://mininet.org/).  
- **Ryu SDN Controller**: Used for managing the simulated SDON (https://book.ryu-sdn.org/en/html/).
