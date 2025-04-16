"""
Order Entry API Server (Flask)
- Accepts order submissions from bots
- Publishes market data and trade events
"""
from flask import Flask, request, jsonify
from exchange.order_book import OrderBook, Order
from competition.scoring import Scoring
import time
import threading

app = Flask(__name__)
order_book = OrderBook()
scoring = Scoring()

@app.route('/submit_order', methods=['POST'])
def submit_order():
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
    return jsonify(order_book.get_book())

@app.route('/trades', methods=['GET'])
def get_trades():
    return jsonify(order_book.get_trades())

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    return jsonify(scoring.get_leaderboard())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
