"""
API Server for Exchange Order Entry and Market Data
- Provides RESTful endpoints for bots/clients to submit orders and query market state
- Integrates with OrderBook to match trades
- Used in the SDN trading competition
"""
from flask import Flask, request, jsonify
from exchange.order_book import Order, OrderBook
from competition.scoring import Scoring
import time
import threading

app = Flask(__name__)
order_book = OrderBook()
scoring = Scoring()

@app.route('/submit_order', methods=['POST'])
def submit_order():
    """
    Submit a new buy or sell order to the exchange.
    Expects JSON: {"order_id", "trader_id", "side", "price", "qty"}
    Returns: {"status", "order_id"}
    """
    data = request.json
    order = Order(
        order_id=data.get('order_id'),
        trader_id=data.get('trader_id'),
        side=data.get('side'),
        price=float(data.get('price')),
        qty=int(data.get('qty')),
        timestamp=time.time()
    )
    order_book.add_order(order)
    # After matching, record new trades for scoring
    new_trades = order_book.get_trades()[len(scoring.trades):]
    for trade in new_trades:
        scoring.record_trade(trade)
    return jsonify({'status': 'accepted', 'order_id': order.order_id})

@app.route('/order_book', methods=['GET'])
def get_order_book():
    """
    Get the current order book state.
    Returns: {"bids", "asks"}
    """
    return jsonify(order_book.get_book())

@app.route('/trades', methods=['GET'])
def get_trades():
    """
    Get a list of recent trades.
    Returns: [{"buy_order_id", "sell_order_id", "price", "qty"}]
    """
    return jsonify(order_book.get_trades())

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """
    Get the current leaderboard standings.
    Returns: [{"trader_id", "score"}]
    """
    return jsonify(scoring.get_leaderboard())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
