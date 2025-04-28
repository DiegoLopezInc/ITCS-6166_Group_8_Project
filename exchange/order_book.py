"""
Central Order Book and Matching Engine for Competition
- Maintains buy and sell order books
- Matches orders and generates trades
- Used by the exchange API server in the SDN trading competition
"""
from collections import deque

class Order:
    """
    Represents a single limit order in the order book.
    Attributes:
        order_id (str): Unique identifier for the order
        trader_id (str): ID of the bot or trader who placed the order
        side (str): 'buy' or 'sell'
        price (float): Order price
        qty (int): Order quantity
        timestamp (float): Time the order was placed
    """
    def __init__(self, order_id, trader_id, side, price, qty, timestamp):
        self.order_id = order_id
        self.trader_id = trader_id
        self.side = side  # 'buy' or 'sell'
        self.price = price
        self.qty = qty
        self.timestamp = timestamp

class OrderBook:
    """
    Central order book for matching buy and sell orders.
    - Maintains two deques: bids (buy orders) and asks (sell orders)
    - Orders are sorted by price/time priority
    - Matches orders and records executed trades
    """
    def __init__(self):
        self.bids = deque()  # buy orders, max price first
        self.asks = deque()  # sell orders, min price first
        self.trades = []

    def add_order(self, order: Order):
        """
        Add a new order to the book and attempt to match orders.
        Args:
            order (Order): The order to add
        """
        if order.side == 'buy':
            self.bids.append(order)
            self.bids = deque(sorted(self.bids, key=lambda o: (-o.price, o.timestamp)))
        else:
            self.asks.append(order)
            self.asks = deque(sorted(self.asks, key=lambda o: (o.price, o.timestamp)))
        self.match()

    def match(self):
        """
        Attempt to match top buy and sell orders. Executes trades if prices cross.
        """
        while self.bids and self.asks and self.bids[0].price >= self.asks[0].price:
            buy = self.bids[0]
            sell = self.asks[0]
            qty = min(buy.qty, sell.qty)
            price = sell.price  # Price priority: taker pays maker's price
            trade = {
                'buy_order_id': buy.order_id,
                'sell_order_id': sell.order_id,
                'price': price,
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

    def get_top_of_book(self):
        """
        Returns the best bid and ask prices and quantities.
        Returns:
            dict: {'bid': (price, qty), 'ask': (price, qty)}
        """
        bid = (self.bids[0].price, self.bids[0].qty) if self.bids else (None, None)
        ask = (self.asks[0].price, self.asks[0].qty) if self.asks else (None, None)
        return {'bid': bid, 'ask': ask}

    def get_trades(self):
        """
        Returns a list of all executed trades.
        Returns:
            list: List of trade dictionaries
        """
        return self.trades
