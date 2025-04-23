"""
Simple Real-Time Web Dashboard for Competition Visualization
"""
from flask import Flask, render_template_string, jsonify, request, redirect, url_for, session
import threading
import time
from competition.scoring import Scoring
from exchange.order_book import OrderBook
import requests
import os
from visualization.docker_control import switch_controller, pause_marketdata as dc_pause, resume_marketdata as dc_resume, reset_demo as dc_reset, get_container_status
import plotly.graph_objs as go
import plotly
import json

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
        .controls { margin: 20px; }
        .controls form { display: inline-block; margin-right: 20px; }
        .chart { width: 60%; margin: 20px auto; }
        .nav { margin: 20px; }
        .nav a { margin-right: 20px; font-weight: bold; color: #337ab7; text-decoration: none; }
    </style>
</head>
<body>
    <div class="nav">
        <a href="/">Dashboard</a>
        <a href="/leaderboard">Competition Leaderboard</a>
    </div>
    <h1>Trading Competition Dashboard</h1>
    <div class="chart">
        <h2>Simulation Overview</h2>
        <table>
            <tr><th>Simulation</th><th>Latency (ms)</th><th>Fairness Index</th><th>Status</th></tr>
            {% for sim in simulations %}
            <tr><td>{{sim['name']}}</td><td>{{sim['latency']}}</td><td>{{sim['fairness']}}</td><td>{{sim['status']}}</td></tr>
            {% endfor %}
        </table>
    </div>
    <div class="controls">
        <h2>Feature Tinkering</h2>
        <form method="post" action="/set_feature">
            <label>Clock Sync Error (CloudEx):</label>
            <input type="number" step="0.01" name="clock_sync_error" value="{{features.clock_sync_error}}"> ms
            <br>
            <label>Fairness Window (Jasper):</label>
            <input type="number" step="0.01" name="jasper_fairness_window" value="{{features.jasper_fairness_window}}"> ms
            <br>
            <label>Enable Hold-and-Release (Jasper):</label>
            <input type="checkbox" name="jasper_hold_release" {% if features.jasper_hold_release %}checked{% endif %}>
            <br>
            <label>Enable Logical Clocks (DBO):</label>
            <input type="checkbox" name="dbo_logical_clocks" {% if features.dbo_logical_clocks %}checked{% endif %}>
            <br>
            <button type="submit">Apply Features</button>
        </form>
    </div>
    <h2>Demo Stock Trading Competition</h2>
    <form method="post" action="/start_competition"><button type="submit">Start Competition</button></form>
    <form method="post" action="/stop_competition"><button type="submit">Stop Competition</button></form>
    <div class="chart">
        <h2>Leaderboard</h2>
        <table>
            <tr><th>Rank</th><th>Trader</th><th>P&L</th></tr>
            {% for rank, (trader, pnl) in enumerate(leaderboard, 1) %}
            <tr><td>{{rank}}</td><td>{{trader}}</td><td>{{'%.2f' % pnl}}</td></tr>
            {% endfor %}
        </table>
    </div>
    <h2>Recent Trades</h2>
    <table>
        <tr><th>Buy</th><th>Sell</th><th>Price</th><th>Qty</th></tr>
        {% for trade in trades[-10:] %}
        <tr><td>{{trade['buy_order_id']}}</td><td>{{trade['sell_order_id']}}</td><td>{{trade['price']}}</td><td>{{trade['qty']}}</td></tr>
        {% endfor %}
    </table>
    <div class="chart">
        <h2>Market Data Chart</h2>
        {{ market_chart|safe }}
    </div>
    <div class="chart">
        <h2>Bot Activity</h2>
        {{ bot_chart|safe }}
    </div>
    <div class="controls">
        <h2>Demo Controls</h2>
        <form method="post" action="/set_controller">
            <label for="controller">Controller:</label>
            <select name="controller" id="controller">
                <option value="sdn_controller.py" {% if controller == 'sdn_controller.py' %}selected{% endif %}>CloudEx (Basic)</option>
                <option value="jasper_multicast_controller.py" {% if controller == 'jasper_multicast_controller.py' %}selected{% endif %}>Jasper</option>
                <option value="dbo_multicast_controller.py" {% if controller == 'dbo_multicast_controller.py' %}selected{% endif %}>DBO</option>
            </select>
            <button type="submit">Switch Controller</button>
        </form>
        <form method="post" action="/pause_marketdata">
            <button type="submit">Pause Market Data</button>
        </form>
        <form method="post" action="/resume_marketdata">
            <button type="submit">Resume Market Data</button>
        </form>
        <form method="post" action="/reset_demo">
            <button type="submit">Reset Demo</button>
        </form>
    </div>
    <p><b>Active Controller:</b> {{controller}}</p>
    <p><b>Container Status:</b> Ryu: {{ryu_status}}, Marketdata: {{marketdata_status}}</p>
</body>
</html>
'''

LEADERBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Competition Leaderboard</title>
    <meta http-equiv="refresh" content="2">
    <style>
        body { font-family: Arial; }
        table { border-collapse: collapse; width: 40%; margin: 40px auto; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: center; font-size: 1.2em; }
        th { background: #222; color: #fff; }
        h1 { text-align: center; }
        .nav { margin: 20px; text-align: center; }
        .nav a { margin-right: 20px; font-weight: bold; color: #337ab7; text-decoration: none; }
    </style>
</head>
<body>
    <div class="nav">
        <a href="/">Dashboard</a>
        <a href="/leaderboard">Competition Leaderboard</a>
    </div>
    <h1>Competition Leaderboard</h1>
    <table>
        <tr><th>Rank</th><th>Trader</th><th>P&L</th></tr>
        {% for rank, (trader, pnl) in enumerate(leaderboard, 1) %}
        <tr><td>{{rank}}</td><td>{{trader}}</td><td>{{'%.2f' % pnl}}</td></tr>
        {% endfor %}
    </table>
</body>
</html>
'''

# Demo state (in a real system, use shared state or env vars)
ACTIVE_CONTROLLER = os.environ.get('RYU_CONTROLLER', 'sdn_controller.py')
MARKETDATA_PAUSED = False

# Simulation and feature state (in-memory for demo)
simulation_metrics = [
    {'name': 'CloudEx', 'latency': 1.0, 'fairness': 0.95, 'status': 'Idle'},
    {'name': 'Jasper', 'latency': 0.8, 'fairness': 0.98, 'status': 'Idle'},
    {'name': 'DBO', 'latency': 1.2, 'fairness': 0.99, 'status': 'Idle'},
]
features = {
    'clock_sync_error': 0.05,
    'jasper_fairness_window': 1.0,
    'jasper_hold_release': True,
    'dbo_logical_clocks': True
}
competition_running = False

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    leaderboard = scoring.get_leaderboard()
    trades = order_book.get_trades()
    # Market data chart (price over time)
    prices = [float(t['price']) for t in trades[-20:]] if trades else []
    seqs = list(range(len(prices)))
    market_chart = plotly.offline.plot({
        "data": [go.Scatter(x=seqs, y=prices, mode='lines+markers', name='Price')],
        "layout": go.Layout(title="Market Data (Last 20 Ticks)", xaxis={'title':'Tick'}, yaxis={'title':'Price'})
    }, output_type='div', include_plotlyjs=False) if prices else "<p>No market data yet.</p>"
    # Bot activity chart (orders per bot)
    bot_counts = {}
    for t in trades[-50:]:
        for oid in [t['buy_order_id'], t['sell_order_id']]:
            bot = oid.split('-')[0]
            bot_counts[bot] = bot_counts.get(bot, 0) + 1
    bot_chart = plotly.offline.plot({
        "data": [go.Bar(x=list(bot_counts.keys()), y=list(bot_counts.values()), name='Orders')],
        "layout": go.Layout(title="Bot Activity (Last 50 Trades)", xaxis={'title':'Bot'}, yaxis={'title':'Orders'})
    }, output_type='div', include_plotlyjs=False) if bot_counts else "<p>No bot activity yet.</p>"
    global ACTIVE_CONTROLLER, MARKETDATA_PAUSED, simulation_metrics, features, competition_running
    ryu_status = get_container_status('ryu')
    marketdata_status = get_container_status('marketdata')
    return render_template_string(DASHBOARD_HTML, leaderboard=leaderboard, trades=trades, controller=ACTIVE_CONTROLLER, market_chart=market_chart, bot_chart=bot_chart, ryu_status=ryu_status, marketdata_status=marketdata_status, simulations=simulation_metrics, features=features)

@app.route('/leaderboard')
def leaderboard_screen():
    leaderboard = scoring.get_leaderboard()
    return render_template_string(LEADERBOARD_HTML, leaderboard=leaderboard)

@app.route('/set_controller', methods=['POST'])
def set_controller():
    global ACTIVE_CONTROLLER
    controller = request.form.get('controller')
    ACTIVE_CONTROLLER = controller
    switch_controller(controller)
    return redirect(url_for('dashboard'))

@app.route('/pause_marketdata', methods=['POST'])
def pause_marketdata():
    global MARKETDATA_PAUSED
    MARKETDATA_PAUSED = True
    dc_pause()
    return redirect(url_for('dashboard'))

@app.route('/resume_marketdata', methods=['POST'])
def resume_marketdata():
    global MARKETDATA_PAUSED
    MARKETDATA_PAUSED = False
    dc_resume()
    return redirect(url_for('dashboard'))

@app.route('/reset_demo', methods=['POST'])
def reset_demo():
    order_book.trades.clear()
    order_book.bids.clear()
    order_book.asks.clear()
    scoring.pnl.clear()
    scoring.trades.clear()
    dc_reset()
    return redirect(url_for('dashboard'))

@app.route('/api/leaderboard')
def api_leaderboard():
    return jsonify(scoring.get_leaderboard())

@app.route('/api/trades')
def api_trades():
    return jsonify(order_book.get_trades())

@app.route('/set_feature', methods=['POST'])
def set_feature():
    global features
    # Get new values from form
    features['clock_sync_error'] = float(request.form.get('clock_sync_error', features['clock_sync_error']))
    features['jasper_fairness_window'] = float(request.form.get('jasper_fairness_window', features['jasper_fairness_window']))
    features['jasper_hold_release'] = 'jasper_hold_release' in request.form
    features['dbo_logical_clocks'] = 'dbo_logical_clocks' in request.form

    # --- Actually update running controllers ---
    # CloudEx (sdn_controller.py)
    try:
        requests.post('http://localhost:5005/api/set_artificial_delay', json={'delay_ms': features['clock_sync_error']})
        # Optionally set clock offsets per port if you expose those controls
    except Exception as e:
        print(f"[WARN] Could not update CloudEx artificial delay: {e}")
    # Jasper (jasper_multicast_controller.py)
    try:
        requests.post('http://localhost:5006/api/set_hold_release_deadline', json={'deadline_ms': features['jasper_fairness_window']})
        requests.post('http://localhost:5006/api/set_hold_release', json={'enabled': features['jasper_hold_release']})
    except Exception as e:
        print(f"[WARN] Could not update Jasper features: {e}")
    # DBO (dbo_multicast_controller.py)
    try:
        requests.post('http://localhost:5007/api/set_logical_clocks', json={'enabled': features['dbo_logical_clocks']})
    except Exception as e:
        print(f"[WARN] Could not update DBO logical clocks: {e}")
    return redirect(url_for('dashboard'))

@app.route('/start_competition', methods=['POST'])
def start_competition():
    global competition_running
    competition_running = True
    # TODO: Start competition logic (bots, order book, etc.)
    return redirect(url_for('dashboard'))

@app.route('/stop_competition', methods=['POST'])
def stop_competition():
    global competition_running
    competition_running = False
    # TODO: Stop competition logic
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)
