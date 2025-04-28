# ITCS-6166_Group_8_Project  
**Multicast Optimization for Software-Defined Networks in Financial Exchanges**    
Group #8: 
- Diego Lopez (dlopez18@charlotte.edu)
- Khushi Arvindbhai Kalathiya (kkalathi@charlotte.edu)
- Sach Denuwara (sdenuwar@charlotte.edu)
- Thomas Macdougall (tmacdoug@charlotte.edu)

Submission Date: April 28, 2025  
---

### 2. Project Abstract  
This project aims to develop a digital twin simulation to model and optimize a software-defined network (SDN) for financial exchanges, integrating scalable multicast techniques inspired by recent cloud-based solutions like Jasper. The core functionalities include creating a virtual SDN replica, implementing multicast optimization algorithms for fair and low-latency data delivery, and comparing these with existing approaches such as CloudEx and DBO. The intended outcome is a simulation demonstrating how digital twin technology and multicast enhancements can improve bandwidth efficiency, reduce latency, and ensure fairness in cloud-hosted financial systems.

---

### 3. Progress Summary  
The project has progressed through initial planning, tool selection, and partial implementation of the simulation environment. Key milestones achieved include completing a literature review of SDN, digital twins, and multicast solutions (e.g., Jasper, CloudEx, DBO), selecting Mininet as the primary simulation tool, and drafting an 8-node gateway topology to emulate an SDN. For simulation, we are using Mininet with an OpenFlow SDN controller (Ryu) to model the network, while Python scripts are being developed to create a digital twin that mirrors the network’s state and to implement Jasper-inspired multicast trees for data dissemination. The network topology design and multicast optimization algorithms are in progress, with testing scheduled for the next phase using synthetic financial exchange traffic (e.g., stock price updates) to measure latency and fairness. The comparative analysis of fairness mechanisms and final validation remain pending, with the team aiming to integrate findings from all referenced papers by the project’s conclusion.

---

### 4. Contribution of Each Member  

| **Task**                  | **Assigned Member(s)** | **Status**    | **Comments**                          |  
|---------------------------|-----------------------|---------------|---------------------------------------|  
| Task 1: Literature review and project scoping | Diego         | Completed     | Reviewed Jasper, CloudEx, DBO papers  |  
| Task 2: Simulation tool setup and topology design | Kushi          | Completed   | Mininet installed, 4-node gateway topology |  
| Task 3: Multicast algorithm development | Sach          | Completed   | Coding Jasper’s tree in Python       |  
| Task 4: Comparative analysis of fairness mechanisms | Thomas          | Completed       | Will simulate CloudEx, DBO approaches |  
| Task 5: Stock price simulation | Diego          | Completed       | Will simulate CloudEx, DBO approaches using bots and simulated stock exchange |  
| Task 6: Dashboard development | Diego          | Completed       | Developed a Flask-based dashboard to monitor simulation state |  

- **Diego**: Conducted a comprehensive literature review, synthesizing insights from "Jasper: Scalable and Fair Multicast for Financial Exchanges in the Cloud," "CloudEx: A Fair-Access Financial Exchange in the Cloud," and "DBO: Fairness for Cloud-Hosted Financial Exchanges" to define project objectives and scope.  
- **Kushi**: Installed Mininet, configured an SDN controller (Ryu), and designed an 8-node gateway topology to simulate an SDN, integrating basic traffic generation scripts to approximate SDN behavior.  
- **Sach**: Began developing a multicast optimization algorithm in Python, adapting Jasper’s overlay tree structure for efficient and fair data delivery within the Mininet simulation.  
- **Thomas**: Simulated fairness mechanisms from CloudEx (hold-and-release) and DBO (latency correction) within Mininet, preparing to integrate findings into the simulation for a comparative evaluation against Jasper’s approach.

---

### 5. Challenges and Solutions  

- **Challenge**: Complexity in simulating optical network dynamics within Mininet, which is primarily designed for packet-switched networks, and integrating multicast fairness techniques.  
  - **Solution**: Kushi approximated optical switching by defining high-bandwidth links (e.g., 10 Gbps) and low-latency paths (e.g., 1 ms) in the topology using Mininet’s link parameters, while Sach leveraged Jasper’s tree-based multicast design. The digital twin, implemented in Python, compensates by modeling optical-specific behaviors (e.g., wavelength allocation). Thomas will cross-reference CloudEx’s hold-and-release and DBO’s latency correction methods to simplify fairness implementation, which are supported by online SDN tutorials.

- **Challenge**: Generating realistic financial exchange traffic for testing multicast fairness and limited team experience with Mininet and comparative analysis.  
  - **Solution**: Sach is adapting iPerf and custom Python scripts to simulate multicast stock price updates (e.g., 100 KB every 10 ms), with Thomas planning to benchmark fairness using latency variance metrics like Jain’s Fairness Index. Kushi completed Mininet walkthroughs and shared resources, while Diego compiled a shared document summarizing key concepts from all three papers to guide the team.

---

### 6. Additional Notes  
To simulate the network, we use Mininet to create a virtual SDN with a **4-node star topology**, where each node represents a trading endpoint connected to a central SDN switch managed by a Ryu controller. The simulation includes three multicast optimization strategies: CloudEx, Jasper-inspired fair multicast, and DBO. The digital twin is implemented in Python, tracking the network’s real-time state and performance metrics such as end-to-end delay, jitter, and fairness (Jain’s Index). Synthetic financial data is generated and distributed using the multicast approaches, and results are visualized on a live dashboard. The dashboard also allows for real-time control of simulation parameters and displays a live competition leaderboard. Team meetings are held regularly to ensure progress and alignment.

### 6.1 Simulation Approach Explained  
1. **Tool Selection**: Mininet is chosen for SDN emulation, with Ryu for controller logic. The flexible topology allows us to approximate real exchange networks.
2. **Topology**: A **4-node star topology** is used for simplicity and speed, with each endpoint representing a trading engine or bot.
3. **Digital Twin**: Python scripts monitor and control the Mininet network, collecting metrics and enabling real-time parameter adjustment via the dashboard.
4. **Multicast Implementation**: Three multicast controllers (CloudEx, Jasper, DBO) are implemented in Python, each with its own fairness and performance features. The controllers can be switched live from the dashboard.
5. **Testing**: Synthetic financial traffic is injected, and all three mechanisms are benchmarked for latency, fairness, and throughput. Results are displayed on the dashboard, including a real-time leaderboard for trading bots.
6. **Visualization**: The Flask-based dashboard, not working as intended.  

### 6.2 Notebook Visualization

The notebook `results_visualization.ipynb` provides a visual analysis of the results from the benchmarking experiments. This is the best place to go to get an overview of the results from this project.

---

### 7. References  
- **arXiv Paper**: "Jasper: Scalable and Fair Multicast for Financial Exchanges in the Cloud" (https://arxiv.org/html/2402.09527v1#S10) – Core inspiration for multicast tree design and fairness in cloud environments, guiding the optimization algorithm and simulation approach.  
- **ACM Paper**: "CloudEx: A Fair-Access Financial Exchange in the Cloud" (Ghalayini et al., HotOS '21, https://dl.acm.org/doi/abs/10.1145/3458336.3465278) – Provided baseline fairness mechanisms (hold-and-release) for comparison with Jasper’s multicast solution.  
- **ACM Paper**: "DBO: Fairness for Cloud-Hosted Financial Exchanges" (Gupta et al., ACM SIGCOMM '23, https://doi.org/10.1145/3603269.3604871) – Offered an alternative latency-correction approach to evaluate against Jasper, enriching the fairness analysis.  
- **Mininet Documentation**: Guided simulation environment setup and topology design (http://mininet.org/).  
- **Ryu SDN Controller**: Used for managing the simulated SDON and integrating the digital twin (https://book.ryu-sdn.org/en/html/).  
- **Textbook**: "Computer Networking: A Top-Down Approach" by Kurose & Ross – Referenced for SDN and networking fundamentals.
