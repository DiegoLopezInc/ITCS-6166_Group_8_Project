"""
Central Order Book and Matching Engine for Competition
"""
from collections import deque

class Order:
    def __init__(self, order_id, trader_id, side, price, qty, timestamp):
        self.order_id = order_id
        self.trader_id = trader_id
        self.side = side  # 'buy' or 'sell'
        self.price = price
        self.qty = qty
        self.timestamp = timestamp

class OrderBook:
    def __init__(self):
        self.bids = deque()  # buy orders, max price first
        self.asks = deque()  # sell orders, min price first
        self.trades = []

    def add_order(self, order: Order):
        if order.side == 'buy':
            self.bids.append(order)
            self.bids = deque(sorted(self.bids, key=lambda o: (-o.price, o.timestamp)))
        else:
            self.asks.append(order)
            self.asks = deque(sorted(self.asks, key=lambda o: (o.price, o.timestamp)))
        self.match()

    def match(self):
        while self.bids and self.asks and self.bids[0].price >= self.asks[0].price:
            buy = self.bids[0]
            sell = self.asks[0]
            qty = min(buy.qty, sell.qty)
            trade = {
                'buy_order_id': buy.order_id,
                'sell_order_id': sell.order_id,
                'price': sell.price,
                'qty': qty,
                'timestamp': max(buy.timestamp, sell.timestamp)
            }
            self.trades.append(trade)
            buy.qty -= qty
            sell.qty -= qty
            if buy.qty == 0:
                self.bids.popleft()
            if sell.qty == 0:
                self.asks.popleft()

    def get_book(self):
        return {
            'bids': [(o.price, o.qty) for o in self.bids],
            'asks': [(o.price, o.qty) for o in self.asks]
        }

    def get_trades(self):
        return self.trades
