# Trading Competition: How It Works (Current Implementation)

This document describes the current state of the SDN-based stock trading competition platform, highlighting the workflow, core components, and how bots, the exchange, and the dashboard interact in the live demo.

---

## 1. Core Components (Implemented)

### 1.1 SDN Exchange Simulation
- **Mininet** simulates a 4-node star topology network.
- **Ryu Controllers** manage multicast delivery using different strategies (CloudEx, Jasper, DBO).
- **Multicast** is used to disseminate real-time market data to all endpoints.

### 1.2 Order Entry & Matching
- **API Server (`exchange/api_server.py`)**: RESTful API for bots to submit buy/sell orders and query market state.
- **Order Book (`exchange/order_book.py`)**: Centralized matching engine that processes orders and generates trades.

### 1.3 Trading Bots
- **Bots** (in the `bots/` directory) connect to the API server, receive market data via multicast, and submit orders using custom strategies.
- Each bot is identified by a unique trader ID.

### 1.4 Competition Logic & Scoring
- **Scoring Module (`competition/scoring.py`)**: Tracks each bot’s profit & loss (P&L) and trade history.
- **Leaderboard (`competition/leaderboard.py`)**: Provides up-to-date rankings based on P&L.

### 1.5 Live Dashboard
- **Dashboard (`visualization/dashboard.py`)**: Web interface for:
  - Monitoring simulation metrics and controller status
  - Adjusting SDN/multicast parameters in real time
  - Viewing a live, auto-refreshing competition leaderboard

---

## 2. Directory Structure

```
exchange/
  order_book.py           # Matching engine logic
  api_server.py           # REST API for order entry
bots/
  sample_bot.py           # Example trading bot/client
  bot_interface.py        # SDK for bots
competition/
  scoring.py              # P&L, ranking logic
  leaderboard.py          # Leaderboard logic
visualization/
  dashboard.py            # Real-time web dashboard
```

---

## 3. Competition Workflow (Current Demo)

1. **Start the SDN Network:**  
   Launch Mininet and the Ryu controller (choose CloudEx, Jasper, or DBO).
2. **Start the Exchange:**  
   Run the API server and order book.
3. **Run Trading Bots:**  
   Each bot connects to the API, receives multicast market data, and submits orders.
4. **Order Matching:**  
   The order book matches buy/sell orders and executes trades.
5. **Scoring & Leaderboard:**  
   Each trade updates the bots’ P&L. The leaderboard ranks bots by live P&L.
6. **Live Monitoring:**  
   The dashboard displays simulation metrics and the live leaderboard. Users can adjust SDN parameters on the fly, affecting the running competition.

---

## 4. Key Features

- **Real-Time Market Data:**  
  Market data is multicast to all endpoints, simulating a real exchange environment.
- **Live Parameter Tuning:**  
  Users can adjust SDN and controller parameters from the dashboard, which takes effect immediately.
- **Bot Competition:**  
  Bots compete based on their trading strategies. Rankings are updated live.
- **Visualization:**  
  The dashboard provides a clear view of both network/simulation status and competition results.

---

## 5. Extending the Platform

- Add new bot strategies or risk management features
- Enhance the order book with more order types (limit, cancel, etc.)
- Expand the dashboard with more analytics or downloadable results
- Integrate additional SDN controllers or topologies

---

*This document reflects the current implementation of the SDN trading competition platform. For code details, see the respective modules in the project directories.*
