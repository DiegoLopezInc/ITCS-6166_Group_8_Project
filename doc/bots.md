# Trading Bots Documentation

This document describes the trading bots used in the financial exchange simulation project. Bots are automated agents that interact with the exchange, submit orders, and compete in the trading competition.

## Overview

Trading bots simulate real-world algorithmic traders. They connect to the exchange via the API server and execute various trading strategies to maximize their profit and loss (P&L) during the competition.

## Key Features

- **Order Submission:** Bots send buy and sell orders to the exchange using the REST API.
- **Market Data Consumption:** Bots receive real-time market data updates (e.g., price changes, trade executions) via multicast from the SDN network.
- **Strategy Implementation:** Each bot can be programmed with a unique trading strategy (e.g., market making, momentum, random walk).
- **Competition Participation:** Bots are ranked on a live leaderboard based on their P&L.

## Typical Bot Workflow

1. **Connect** to the exchange API server.
2. **Receive** market data updates via multicast.
3. **Analyze** market conditions and decide on trading actions.
4. **Submit** buy or sell orders to the exchange.
5. **Update** internal state based on trade confirmations and new market data.
6. **Repeat** until the competition ends.

## Example Bot API Usage

- **Submit an Order:**
  - `POST /order` with JSON body: `{ "trader_id": "bot1", "side": "buy", "qty": 10, "price": 100.5 }`
- **Query Market Data:**
  - `GET /market` returns the latest price and order book snapshot.
- **Check Order Status:**
  - `GET /order/{id}` returns the current status of a submitted order.

## Extending Bots

- Implement new trading strategies (e.g., arbitrage, statistical trading)
- Add risk management features
- Integrate with different market data feeds or exchanges

---

For further details, see the code in the `bots/` directory and the API documentation in `exchange/api_server.py`.