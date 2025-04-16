# Jasper: Scalable and Fair Multicast for Financial Exchanges in the Cloud

## Basic Information
- **Authors:** 
- Muhammad Haseeb - New York University
- Jinkun Geng - Stanford University
- Ulysses Butler - New York University
- Xiyu Hao - New York University
- Daniel Duclos-Cavalcanti - Technical University of Munich
- Anirudh Sivaraman - New York University
- **Publication Year:** 2024
- **Journal/Conference:** arXiv
- **DOI/URL:** https://arxiv.org/html/2402.09527v1#S10

## Summary
Jasper introduces a scalable and fair multicast service for financial exchanges operating in the cloud. The system addresses the challenge of delivering market data with low latency and high fairness to thousands of receivers, overcoming the limitations of previous solutions like CloudEx. Jasper leverages a tree of proxies for multicast, rather than direct unicast, and uses a hold-and-release mechanism with synchronized clocks to achieve near-simultaneous delivery.

Through large-scale cloud experiments, Jasper demonstrates its ability to deliver market data to over 1000 receivers with sub-millisecond fairness windows, outperforming prior approaches in both scalability and fairness.

## Key Contributions
- Proposes Jasper, a multicast overlay service that delivers fair and low-latency market data to thousands of receivers in the cloud.
- Employs a tree-based proxy architecture and a hold-and-release mechanism to synchronize data delivery across receivers.
- Demonstrates superior scalability and fairness compared to CloudEx and direct unicast approaches, validated through extensive cloud-based experiments.

## Methodology
Jasper builds multicast trees for each market data stream, minimizing latency and variance through hedging and optimized proxy placement. The system uses scalable delay measurement and attaches deadlines to messages, ensuring receivers process data nearly simultaneously. Performance is benchmarked against direct unicast and CloudEx, showing Jasper's advantages in fairness and scalability.

## Results
Jasper achieves low message holding durations and narrow delivery windows, supporting 1000+ receivers with sub-millisecond fairness. It outperforms CloudEx in both latency and fairness metrics, maintaining consistent performance as the number of receivers scales.

## Relevance to Our Project
Jasper's fair multicast strategies and scalable overlay design are directly relevant to our SDN mini-project. Its methodology informs our implementation of fair multicast in a simulated financial exchange, helping us benchmark and improve fairness and latency in our own network experiments.

## Key Figures
[Reference to important figures/tables]

## Citations to Follow
[Other papers cited that might be worth reading]

## Notes
[Any additional thoughts or observations]