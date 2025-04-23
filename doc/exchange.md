# Exchange Module Documentation

This document describes the core components of the simulated financial exchange implemented in this project. The exchange serves as the central entity for processing market data, handling orders, and coordinating with trading bots and endpoints.

## Overview

The exchange module simulates a simplified electronic financial exchange, including:
- An order book for matching buy/sell orders
- An API server for receiving orders and queries from bots/clients
- Integration with the multicast SDN network for real-time market data dissemination

## Components

### 1. Order Book (`exchange/order_book.py`)
- **Purpose:** Maintains buy and sell orders, matches trades, and updates market state.
- **Key Functions:**
  - Add new orders (buy/sell)
  - Match orders and execute trades
  - Track order status and trade history

### 2. API Server (`exchange/api_server.py`)
- **Purpose:** Provides a RESTful API for bots and external clients to interact with the exchange.
- **Endpoints:**
  - `POST /order`: Submit a new buy or sell order
  - `GET /order/{id}`: Query order status
  - `GET /market`: Get current market data (price, order book snapshot)
- **Integration:** Bots use this API to participate in the trading competition.

### 3. Integration with SDN Multicast
- The exchange publishes market data updates (e.g., trade executions, price changes) to all endpoints using the SDN multicast network.
- Endpoints receive updates in real-time, simulating the dissemination of market data in a real financial exchange.

### 4. Trading Bots
- Bots interact with the exchange via the API server.
- They can implement various trading strategies and compete in the demo stock trading competition.

## Workflow

1. **Bots** submit orders to the exchange via the API server.
2. The **order book** matches orders and executes trades.
3. The **exchange** multicasts market data updates to all endpoints using the SDN network.
4. **Endpoints** (trading engines/clients) receive updates and can act on new market information.

## Example Sequence Diagram

```
Bot --> API Server --> Order Book --> [Trade Execution]
                           |
                           v
                  SDN Multicaster (Controller)
                           |
                           v
                  Endpoints (Trading Engines)
```

## Extending the Exchange

- Add new order types (limit, market, cancel)
- Implement advanced matching algorithms
- Integrate with more sophisticated SDN controllers or topologies

---

For further details, see the code in `exchange/order_book.py` and `exchange/api_server.py`.