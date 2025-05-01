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
This project aims to develop a simulation to model and optimize a software-defined network (SDN) for financial exchanges, integrating scalable multicast techniques inspired by recent cloud-based solutions like Jasper. The core functionalities include creating a virtual SDN replica, implementing multicast optimization algorithms for fair and low-latency data delivery, and comparing these with existing approaches such as CloudEx and DBO. The intended outcome is a simulation demonstrating how multicast enhancements can improve bandwidth efficiency, reduce latency, and ensure fairness in cloud-hosted financial systems.

---

### 3. Progress Summary  
The project has progressed through initial planning, tool selection, and complete implementation of the simulation environment. Key milestones achieved include completing a literature review of SDN, and multicast solutions (e.g., Jasper, CloudEx, DBO), selecting Mininet as the primary simulation tool, and drafting a 4-node star topology to emulate an SDN. For simulation, we are using Mininet with an OpenFlow SDN controller (Ryu) to model the network, while Python scripts are being developed to create a network and to implement Jasper-inspired multicast trees for data dissemination. The network topology design and multicast optimization algorithms are complete, with testing completed using synthetic financial exchange traffic (e.g., stock price updates) to measure latency and fairness. The comparative analysis of fairness mechanisms and final validation are complete, the team has integrated findings from all referenced papers.

### 3.1 Introduction to the Project

The project is a simulation of a software-defined network (SDN) for financial exchanges, integrating scalable multicast techniques inspired by recent research for cloud-based solutions like Jasper. The core functionalities include creating a virtual SDN, implementing multicast optimization algorithms for fair and low-latency data delivery, and comparing these with other research approaches such as CloudEx and DBO. The intended outcome is a simulation demonstrating how multicast enhancements can improve bandwidth efficiency, reduce latency, and ensure fairness in cloud-hosted financial systems.

### 3.2 Motivation
Financial exchanges are digital markets where financial instruments are traded. Exchange goals are to facilitate trading, price discovery, and fair transactions. Historically, to give every node on the network fair (same) latency, colocation of servers was used. Colocation; all servers are located in the same place with similar hardware. As exchanges or market participants (banks, market makers, prop trading firms, retail brokers…etc.) move their networks to the cloud, algorithms must ensure the network performance remains unchanged. This project provided an opportunity to apply computer networking concepts to modern cloud hosting.

---

### 4. Contribution of Each Member  

| **Task**                  | **Assigned Member(s)** | **Status**    | **Comments**                          |  
|---------------------------|-----------------------|---------------|---------------------------------------|  
| Task 1: Literature review and project scoping | Diego         | Completed     | Reviewed Jasper, CloudEx, DBO papers  |  
| Task 2: Simulation tool setup and topology design | Kushi          | Completed   | Mininet installed, 4-node star topology |  
| Task 3: Multicast algorithm development | Sach          | Completed   | Coding Jasper’s tree in Python       |  
| Task 4: Comparative analysis of fairness mechanisms | Thomas          | Completed       | Simulated CloudEx, DBO approaches |  
| Task 5: Stock price simulation | Diego          | Partial       | Simulated CloudEx, DBO approaches using bots and simulated stock exchange |  
| Task 6: Dashboard development | Diego          | Failed       | Developed a Flask-based dashboard to monitor simulation state |  

- **Diego**: Conducted a comprehensive literature review, synthesizing insights from "Jasper: Scalable and Fair Multicast for Financial Exchanges in the Cloud," "CloudEx: A Fair-Access Financial Exchange in the Cloud," and "DBO: Fairness for Cloud-Hosted Financial Exchanges" to define project objectives and scope.  
- **Kushi**: Installed Mininet, configured an SDN controller (Ryu), and designed an  4-node star topology to simulate an SDN, integrating basic traffic generation scripts to approximate SDN behavior.  
- **Sach**: Began developing a multicast optimization algorithm in Python, adapting Jasper’s overlay tree structure for efficient and fair data delivery within the Mininet simulation.  
- **Thomas**: Simulated fairness mechanisms from CloudEx (hold-and-release) and DBO (latency correction) within Mininet, preparing to integrate findings into the simulation for a comparative evaluation against Jasper’s approach.

---

### 5. Challenges and Solutions  

- **Challenge**: Complexity in simulating optical network dynamics within Mininet, which is primarily designed for packet-switched networks, and integrating multicast fairness techniques.  
  - **Solution**: Kushi approximated optical switching by defining high-bandwidth links (e.g., 10 Gbps) and low-latency paths (e.g., 1 ms) in the topology using Mininet’s link parameters, while Sach leveraged Jasper’s tree-based multicast design. The digital twin, implemented in Python, compensates by modeling optical-specific behaviors (e.g., wavelength allocation). Thomas will cross-reference CloudEx’s hold-and-release and DBO’s latency correction methods to simplify fairness implementation, which are supported by online SDN tutorials.

- **Challenge**: Generating realistic financial exchange traffic for testing multicast fairness and limited team experience with Mininet and comparative analysis.  
  - **Solution**: Sach is adapted custom Python scripts to simulate multicast stock price updates (e.g., 100 KB every 10 ms), with Thomas planning to benchmark fairness using latency variance metrics like Jain’s Fairness Index. Kushi completed Mininet walkthroughs and shared resources, while Diego compiled a shared document summarizing key concepts from all three papers to guide the team.

---

### 6. Additional Notes  
To simulate the network, we use Mininet to create a virtual SDN with a **4-node star topology**, where each node represents a trading endpoint connected to a central SDN switch managed by a Ryu controller. The simulation includes three multicast optimization strategies from research papers we reviewed: CloudEx, Jasper-inspired fair multicast, and DBO. The SDN is implemented in Python, tracking the network’s real-time state and performance metrics such as end-to-end delay, jitter, and fairness (Jain’s Fairness Index). Synthetic messages are generated and distributed using the multicast approaches, and results are saved as CSV files. Team meetings are held regularly to ensure progress and alignment.

### 6.1 Simulation Approach Explained  
1. **Tool Selection**: Mininet is chosen for SDN emulation, with Ryu for controller logic. The flexible topology allows us to miniaturize a real exchange network from limited hardware resources.
2. **Topology**: A **4-node star topology** is used for simplicity and speed, with each endpoint representing a trading engine or bot.
3. **SDN**: Python scripts monitor and control the Mininet network, collecting metrics and saving them to CSV files.
4. **Multicast Implementation**: Three multicast controllers (CloudEx, Jasper, DBO) are implemented in Python, each with its own fairness and performance features.
5. **Testing**: Synthetic messages are injected, and all three mechanisms are benchmarked for latency, fairness, and throughput. Results are saved as CSV files.
6. **Visualization**: The Flask-based dashboard, not working as intended (left out of final submission).  

### 6.2 Notebook Visualization

The notebook `results_visualization.ipynb` provides a visual analysis of the results from the benchmarking experiments. This is the best place to go to get an overview of the results from this project.

### 6.3 Potential Future Work
To enhance scalability (simulate a realistic exchange network), improvements can be made to the network topology. Deploying the system in the cloud will facilitate broader access and easier scaling. The platform can also be repurposed for trading competitions. Furthermore, the evaluation of new algorithms to further research about performance and fairness on cloud-based financial exchanges.

### 6.4 Stretch Goal
Create a trading competition platform for users to compete against each other on a simulated exchange network. With the goal of exposure to the SDN and multicast technologies implemented in this project.
---

### 7. References  
- **arXiv Paper**: "Jasper: Scalable and Fair Multicast for Financial Exchanges in the Cloud" (https://arxiv.org/html/2402.09527v1#S10) – Core inspiration for multicast tree design and fairness in cloud environments, guiding the optimization algorithm and simulation approach.  
- **ACM Paper**: "CloudEx: A Fair-Access Financial Exchange in the Cloud" (Ghalayini et al., HotOS '21, https://dl.acm.org/doi/abs/10.1145/3458336.3465278) – Provided baseline fairness mechanisms (hold-and-release) for comparison with Jasper’s multicast solution.  
- **ACM Paper**: "DBO: Fairness for Cloud-Hosted Financial Exchanges" (Gupta et al., ACM SIGCOMM '23, https://doi.org/10.1145/3603269.3604871) – Offered an alternative latency-correction approach to evaluate against Jasper, enriching the fairness analysis.  
- **Mininet Documentation**: Guided simulation environment setup and topology design (http://mininet.org/).  
- **Ryu SDN Controller**: Used for managing the simulated SDON and integrating the digital twin (https://book.ryu-sdn.org/en/html/).  
- **Textbook**: "Computer Networking: A Top-Down Approach" by Kurose & Ross – Referenced for SDN and networking fundamentals.
