
## Getting Started

### Prerequisites
- Python 3.8+
- Mininet
- Ryu SDN Controller
- Additional Python packages listed in requirements.txt

### Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Install Mininet following instructions at [mininet.org](http://mininet.org)
4. Install Ryu: `pip install ryu`

### Running the Simulation
1. Start the Ryu controller:
```bash
ryu-manager ryu.app.simple_switch_13
```

2. Launch the Mininet topology:
```bash
sudo python3 mininet-topo.py
```

3. Run the digital twin:
```bash
python3 digital_twin.py
```

## Simulation Components

### Network Topology
The project uses an 8-node ring topology to simulate an SDON. Each node represents an optical switch managed by the SDN controller.

### Digital Twin Implementation
The digital twin is a Python-based virtual replica that:
- Mirrors the network's real-time state
- Updates via OpenFlow messages from the SDN controller
- Visualizes network conditions
- Optimizes multicast algorithms

### Multicast Optimization
Our project implements and compares three approaches:
1. **Jasper**: Tree-based multicast with fairness optimization
2. **CloudEx**: Hold-and-release fairness mechanism
3. **DBO**: Latency correction techniques

## Performance Metrics
- End-to-end delay
- Jitter
- Fairness (using Jain's Fairness Index)
- Bandwidth efficiency

## Additional Resources
- [Literature Review](../literature/literature_review.md)
- [API Documentation](./api.md)
- [Testing Guide](./testing.md)

## Contributing
See our [contribution guidelines](./contributing.md) for details on how to contribute to this project.