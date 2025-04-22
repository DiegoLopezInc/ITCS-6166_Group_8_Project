# DBO: Fairness for Cloud-Hosted Financial Exchange

## Basic Information
- **Authors:** 
- Eashan Gupta - UIUC, Microsoft Research
- Prateesh Goyal - Microsoft Research
- Ilias Marinos - Microsoft Research
- Chenxingyu Zhao - University of Washington, Microsoft Research
- Radhika Mittal - UIUC
- Ranveer Chandra - Microsoft Research
- **Publication Year:** 2023
- **Journal/Conference:** ACM SIGCOMM '23
- **DOI/URL:** https://doi.org/10.1145/3603269.3604871

## Summary
DBO (Delivery Based Ordering) introduces a novel mechanism to guarantee fairness for high-frequency trading in cloud-hosted financial exchanges. Unlike previous approaches that rely on clock synchronization, DBO uses logical delivery clocks to post-hoc offset network latency differences, ensuring that trades are ordered based on when market data is actually received by each participant. This method overcomes the unpredictable and unbounded latencies of cloud networks, providing guaranteed fairness and low latency (sub-100 microseconds) at high transaction rates.

The paper presents both bare-metal and public cloud deployments, demonstrating DBO's effectiveness in achieving perfect fairness and lower latency inflation compared to prior solutions like CloudEx.

## Key Contributions
- Proposes Delivery Based Ordering (DBO), a clockless mechanism for guaranteed fairness in cloud-hosted financial exchanges.
- Uses logical delivery clocks to order trades based on actual data receipt, eliminating the need for clock synchronization.
- Demonstrates DBO's scalability and performance in real-world deployments, achieving perfect fairness and low latency at high throughput.

## Methodology
DBO assigns each participant a logical delivery clock, tracking time relative to the receipt of market data. Trades are ordered according to these clocks, not absolute time, allowing the system to compensate for unpredictable cloud network latencies. The method is implemented on both bare-metal servers (using programmable NICs) and public cloud VMs, and is evaluated against CloudEx and direct delivery baselines.

## Results
DBO achieves perfect fairness (100%) and sub-100 microsecond p99 latency in both bare-metal and cloud environments, even at transaction rates of 125,000 trades per second. Compared to CloudEx, DBO offers lower latency inflation and does not require clock synchronization, making it more practical for real-world deployments.

## Relevance to Our Project
DBO's delivery-clock-based approach to fairness provides a valuable alternative to clock-synchronization-based solutions for our SDN mini-project. Its methodology and empirical results offer insights for designing fair and efficient order processing in simulated financial exchange networks, particularly in environments with unpredictable network latencies.