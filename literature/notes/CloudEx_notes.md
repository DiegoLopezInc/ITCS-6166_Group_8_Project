# CloudEx: A Fair-Access Financial Exchange in theCloud

## Basic Information
- **Authors:** 
- Ahmad Ghalayini - Stanford University, Stanford, USA
- Jinkun Geng - Stanford University, Stanford, USA
- Vighnesh Sachidananda - Stanford University, Stanford, USA
- Vinay Sriram - Tick Tock Networks, Palo Alto, USA
- Yilong Geng - Tick Tock Networks, Palo Alto, USA
- Balaji Prabhakar - Stanford University, Stanford, USA
- Mendel Rosenblum - Stanford University, Stanford, USA
- Anirudh Sivaraman - NYU, New York, USA
- **Publication Year:** 2021
- **Journal/Conference:** ACM
- **DOI/URL:** https://dl.acm.org/doi/abs/10.1145/3458336.3465278

## Summary
CloudEx proposes a cloud-hosted financial exchange that ensures fairness for all market participants despite unpredictable and variable cloud network latencies. The system uses high-precision software clock synchronization and dynamic message delays to equalize order and market data delivery times. CloudEx was refined through real-world deployments in academic courses, demonstrating its effectiveness and highlighting areas for further optimization.

Key lessons include the feasibility of fair-access exchanges in the cloud, the importance of dynamic delay tuning, and the need for robust fault tolerance. The paper outlines future directions for performance improvements and broader applications beyond financial exchanges.

## Key Contributions
- Introduces CloudEx, a fair-access financial exchange system designed specifically for cloud environments.
- Implements high-precision clock synchronization and dynamic message delay control to ensure fairness in order processing and market data dissemination.
- Demonstrates the system in real-world academic deployments, providing empirical evidence of its effectiveness and areas for further refinement.

## Methodology
CloudEx uses synchronized clocks and artificial message delays to equalize inbound and outbound latencies for all participants. Orders are replicated through multiple gateways to improve fault tolerance and reduce tail latency. The system employs a control strategy to dynamically tune delays based on observed unfairness ratios. Performance and fairness are evaluated through deployments with student participants, measuring order latency and fairness metrics. Future work is outlined for further optimization and broader applicability.

Unfairness: Definitions and Remedies
- Inbound Unfairness Ratio
    If gateway-assigned timestamp is earlier than the previous
- Outbound Unfairness Ratio
    If piece of market data is received later than other gateways
- Sequencer Delay Parameters
    Added delay to the sequencer buffer to ensure fairness
- Hold/Release Buffer Delay Parameters
    Added delay to the hold and release buffer to gateways to ensure fairness
- Consequences for delays
    Cause system to be less responsive

Market participants:
- Gateways, central exchange server, cloud storage
- Each owns a VM that is connected to one of the gateways. 
- Also provided APIs to:
    - Submit market data
        - Symbol to be traded
        - action (buy or sell)
        - number of shares
        - order type
        - limit price (for limit orders)
    - Query market data
    - Subscribe to market data

ZeroMQ:
- Reliable network communication
- Each gateway clock is precisely synchronized to the central exchange server clock

Visualization of the limit order book:
- validates orders from market participants and then assigns a globally synchronized timestamp before forwarding to centralized server.
- orders confirmations from the centralized exchange server are then forwarded to market participants via the order handler.

H/R Buffer:
- Ensure real time market data is available to market participants at the same time.

Sequencer:
- Creates a priority queue based on order gateway-assigned timestamps.

Match Engine (Google Bigtable):
- Two data structures:
    - Order book (tracks pending orders)
    - Portfolio matrix (tracks participants assets and cash balance)
- API:
    - Market participants are provided an API to query historical market data from Bigtable

Market Data Dissemination:
- H/R buffers at the gateways
- Market participants subscribe to data per symbol.
- Release timestamp from matching engine to gateways


## Results
Tested over two trading competitions:
- high school (3 hours, 1000 orders, 1000 trades, 10 symbols)
- college course (8 days, 4.2 million orders, 330000 trades, ??? symbols)

    


## Relevance to Our Project
CloudEx's approach to fairness and latency management directly informs our SDN mini-project's multicast fairness and benchmarking. Its use of clock synchronization, message delay tuning, and empirical evaluation provides a strong foundation for designing and evaluating fair multicast strategies in our simulated financial exchange network.

## Key Figures
[Reference to important figures/tables]

## Citations to Follow
[Other papers cited that might be worth reading]

## Notes
[Any additional thoughts or observations]