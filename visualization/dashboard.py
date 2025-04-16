"""
Simple Real-Time Web Dashboard for Competition Visualization
"""
from flask import Flask, render_template_string, jsonify
import threading
import time
from competition.scoring import Scoring
from exchange.order_book import OrderBook

app = Flask(__name__)
scoring = Scoring()
order_book = OrderBook()

DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Trading Competition Dashboard</title>
    <meta http-equiv="refresh" content="2">
    <style>
        body { font-family: Arial; }
        table { border-collapse: collapse; width: 40%; margin: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
        th { background: #222; color: #fff; }
    </style>
</head>
<body>
    <h1>Leaderboard</h1>
    <table>
        <tr><th>Rank</th><th>Trader</th><th>P&L</th></tr>
        {% for rank, (trader, pnl) in enumerate(leaderboard, 1) %}
        <tr><td>{{rank}}</td><td>{{trader}}</td><td>{{'%.2f' % pnl}}</td></tr>
        {% endfor %}
    </table>
    <h2>Recent Trades</h2>
    <table>
        <tr><th>Buy</th><th>Sell</th><th>Price</th><th>Qty</th></tr>
        {% for trade in trades[-10:] %}
        <tr><td>{{trade['buy_order_id']}}</td><td>{{trade['sell_order_id']}}</td><td>{{trade['price']}}</td><td>{{trade['qty']}}</td></tr>
        {% endfor %}
    </table>
</body>
</html>
'''

@app.route('/')
def dashboard():
    leaderboard = scoring.get_leaderboard()
    trades = order_book.get_trades()
    return render_template_string(DASHBOARD_HTML, leaderboard=leaderboard, trades=trades)

@app.route('/api/leaderboard')
def api_leaderboard():
    return jsonify(scoring.get_leaderboard())

@app.route('/api/trades')
def api_trades():
    return jsonify(order_book.get_trades())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)
