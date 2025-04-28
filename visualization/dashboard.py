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
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        body { font-family: Arial; background: #f8f9fa; }
        .container { margin-top: 30px; }
        .card { margin-bottom: 24px; }
        .navbar { margin-bottom: 30px; }
        .table th, .table td { vertical-align: middle; }
        .btn-primary, .btn-danger { min-width: 120px; }
        .chart { margin-top: 20px; }
        .form-group { margin-bottom: 1rem; }
    </style>
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-light bg-light shadow-sm">
  <a class="navbar-brand font-weight-bold" href="/">Trading Dashboard</a>
  <div class="collapse navbar-collapse">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item"><a class="nav-link" href="/">Dashboard</a></li>
      <li class="nav-item"><a class="nav-link" href="/leaderboard">Competition Leaderboard</a></li>
    </ul>
  </div>
</nav>
<div class="container">
  <div class="row">
    <div class="col-md-8">
      <div class="card shadow">
        <div class="card-header bg-primary text-white">Simulation Overview</div>
        <div class="card-body">
          <table class="table table-bordered table-hover">
            <thead class="thead-light">
              <tr><th>Simulation</th><th>Latency (ms)</th><th>Fairness Index</th><th>Status</th></tr>
            </thead>
            <tbody>
            {% for sim in simulations %}
            <tr><td>{{sim['name']}}</td><td>{{sim['latency']}}</td><td>{{sim['fairness']}}</td><td>{{sim['status']}}</td></tr>
            {% endfor %}
            </tbody>
          </table>
        </div>
      </div>
      <div class="card shadow">
        <div class="card-header bg-info text-white">Leaderboard</div>
        <div class="card-body">
          <table class="table table-striped table-bordered">
            <thead class="thead-light">
              <tr><th>Rank</th><th>Trader</th><th>P&amp;L</th></tr>
            </thead>
            <tbody id="leaderboard-tbody">
            {% for item in leaderboard %}
            <tr><td>{{ loop.index }}</td><td>{{ item[0] }}</td><td>{{ '%.2f' % item[1] }}</td></tr>
            {% endfor %}
            </tbody>
          </table>
        </div>
      </div>
      <div class="card shadow">
        <div class="card-header bg-secondary text-white">Recent Trades</div>
        <div class="card-body">
          <table class="table table-sm table-hover">
            <thead class="thead-light">
              <tr><th>Buy</th><th>Sell</th><th>Price</th><th>Qty</th></tr>
            </thead>
            <tbody id="trades-tbody">
            {% for trade in trades[-10:] %}
            <tr><td>{{trade['buy_order_id']}}</td><td>{{trade['sell_order_id']}}</td><td>{{trade['price']}}</td><td>{{trade['qty']}}</td></tr>
            {% endfor %}
            </tbody>
          </table>
        </div>
      </div>
      <div class="card shadow chart">
        <div class="card-header bg-success text-white">Market Data Chart</div>
        <div class="card-body">{{ market_chart|safe }}</div>
      </div>
      <div class="card shadow chart">
        <div class="card-header bg-warning text-dark">Bot Activity</div>
        <div class="card-body">{{ bot_chart|safe }}</div>
      </div>
      <div class="card mt-4">
        <div class="card-header bg-dark text-white">Bot Output</div>
        <div class="card-body">
          <pre id="bot-output" style="height:200px;overflow:auto;background:#222;color:#eee"></pre>
        </div>
      </div>
      <div class="card mt-4">
        <div class="card-header bg-success text-white">Recent Results</div>
        <div class="card-body">
          <div id="results-output" style="height:200px;overflow:auto;background:#f8fff8;color:#222;font-family:monospace;font-size:13px"></div>
        </div>
      </div>
    </div>
    <div class="col-md-4">
      <div class="card shadow">
        <div class="card-header bg-dark text-white">Feature Tinkering</div>
        <div class="card-body">
          <form method="post" action="/set_feature">
            <div class="form-group">
              <label>Clock Sync Error (CloudEx):
                <span data-toggle="tooltip" title="Artificial clock skew for CloudEx simulation.">
                  <i class="fa fa-info-circle text-info"></i>
                </span>
              </label>
              <input type="number" step="0.01" class="form-control" name="clock_sync_error" value="{{features.clock_sync_error}}"> ms
            </div>
            <div class="form-group">
              <label>Fairness Window (Jasper):</label>
              <input type="number" step="0.01" class="form-control" name="jasper_fairness_window" value="{{features.jasper_fairness_window}}"> ms
            </div>
            <div class="form-group form-check">
              <input type="checkbox" class="form-check-input" name="jasper_hold_release" id="jasper_hold_release" {% if features.jasper_hold_release %}checked{% endif %}>
              <label class="form-check-label" for="jasper_hold_release">Enable Hold-and-Release (Jasper)</label>
            </div>
            <div class="form-group form-check">
              <input type="checkbox" class="form-check-input" name="dbo_logical_clocks" id="dbo_logical_clocks" {% if features.dbo_logical_clocks %}checked{% endif %}>
              <label class="form-check-label" for="dbo_logical_clocks">Enable Logical Clocks (DBO)</label>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Apply Features</button>
          </form>
        </div>
      </div>
      <div class="card shadow mt-4">
        <div class="card-header bg-danger text-white">Competition Controls</div>
        <div class="card-body d-flex flex-column">
          <form method="post" action="/start_competition" class="mb-2"><button type="submit" class="btn btn-success btn-block">Start Competition</button></form>
          <form method="post" action="/stop_competition"><button type="submit" class="btn btn-danger btn-block">Stop Competition</button></form>
        </div>
      </div>
      <div class="card shadow mt-4">
        <div class="card-header bg-light">Demo Controls</div>
        <div class="card-body">
          <form method="post" action="/set_controller" class="mb-2">
            <div class="form-group">
              <label for="controller">Controller:</label>
              <select name="controller" id="controller" class="form-control mb-2">
                <option value="sdn_controller.py" {% if controller == 'sdn_controller.py' %}selected{% endif %}>SDN Controller</option>
                <option value="jasper_multicast_controller.py" {% if controller == 'jasper_multicast_controller.py' %}selected{% endif %}>Jasper Multicast</option>
                <option value="dbo_multicast_controller.py" {% if controller == 'dbo_multicast_controller.py' %}selected{% endif %}>DBO Multicast</option>
              </select>
              <button type="submit" class="btn btn-info btn-block">Switch Controller</button>
            </div>
          </form>
          <form method="post" action="/reset_demo" class="mb-2"><button type="submit" class="btn btn-warning btn-block">Reset Demo</button></form>
          <form method="post" action="/pause_marketdata" class="mb-2"><button type="submit" class="btn btn-secondary btn-block">Pause Marketdata</button></form>
          <form method="post" action="/resume_marketdata"><button type="submit" class="btn btn-secondary btn-block">Resume Marketdata</button></form>
        </div>
        <div class="card-footer">
          <p><b>Active Controller:</b> {{controller}}</p>
          <p><b>Container Status:</b> Ryu: {{ryu_status}}, Marketdata: {{marketdata_status}}</p>
        </div>
      </div>
    </div>
  </div>
</div>
<!-- Bootstrap JS, Popper.js, and jQuery -->
<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
<script>
  $(function () {
    $('[data-toggle="tooltip"]').tooltip();
  });
</script>
<script>
  function updateLeaderboard() {
    fetch('/api/leaderboard')
      .then(response => response.json())
      .then(data => {
        let tbody = document.getElementById('leaderboard-tbody');
        if (!tbody) return;
        tbody.innerHTML = '';
        data.forEach(function(item, idx) {
          let row = `<tr><td>${idx+1}</td><td>${item[0]}</td><td>${item[1].toFixed(2)}</td></tr>`;
          tbody.innerHTML += row;
        });
      });
  }
  function updateTrades() {
    fetch('/api/trades')
      .then(response => response.json())
      .then(data => {
        let tbody = document.getElementById('trades-tbody');
        if (!tbody) return;
        tbody.innerHTML = '';
        data.slice(-10).forEach(function(trade) {
          let row = `<tr><td>${trade.buy_order_id}</td><td>${trade.sell_order_id}</td><td>${trade.price}</td><td>${trade.qty}</td></tr>`;
          tbody.innerHTML += row;
        });
      });
  }
  function updateBotOutput() {
    fetch('/api/bot_output')
      .then(response => response.json())
      .then(data => {
        document.getElementById('bot-output').textContent = data.lines.join('');
      });
  }
  function updateResults() {
    fetch('/api/results')
      .then(response => response.json())
      .then(data => {
        let el = document.getElementById('results-output');
        let html = '';
        data.results.forEach(function(res) {
          html += `<b>${res.filename}</b><br><table border='1' style='margin-bottom:8px;'>`;
          res.rows.forEach(function(row) {
            html += '<tr>' + row.map(cell => `<td>${cell}</td>`).join('') + '</tr>';
          });
          html += '</table>';
        });
        el.innerHTML = html;
      });
  }
  setInterval(function() {
    updateLeaderboard();
    updateTrades();
    updateBotOutput();
    updateResults();
  }, 2000);
  document.addEventListener('DOMContentLoaded', function() {
    updateLeaderboard();
    updateTrades();
    updateBotOutput();
    updateResults();
  });
</script>
</body>
</html>
'''

LEADERBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Competition Leaderboard</title>
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
        <tr><th>Rank</th><th>Trader</th><th>P&amp;L</th></tr>
        {% for item in leaderboard %}
        <tr><td>{{ loop.index }}</td><td>{{ item[0] }}</td><td>{{ '%.2f' % item[1] }}</td></tr>
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

@app.route('/api/results')
def api_results():
    import glob
    import csv
    results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
    # Find all csv files, sort by modified time descending
    csv_files = sorted(glob.glob(os.path.join(results_dir, '*.csv')), key=os.path.getmtime, reverse=True)[:5]
    all_results = []
    for path in csv_files:
        with open(path, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
            all_results.append({'filename': os.path.basename(path), 'rows': rows})
    return jsonify({'results': all_results})

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
    print("[DEBUG] set_controller route called")
    global ACTIVE_CONTROLLER
    controller = request.form.get('controller')
    print(f"[DEBUG] Controller selected: {controller}")
    ACTIVE_CONTROLLER = controller
    result = switch_controller(controller)
    print(f"[DEBUG] switch_controller() returned: {result}")
    return redirect(url_for('dashboard'))

@app.route('/pause_marketdata', methods=['POST'])
def pause_marketdata():
    print("[DEBUG] pause_marketdata route called")
    global MARKETDATA_PAUSED
    MARKETDATA_PAUSED = True
    result = dc_pause()
    print(f"[DEBUG] dc_pause() returned: {result}")
    return redirect(url_for('dashboard'))

@app.route('/resume_marketdata', methods=['POST'])
def resume_marketdata():
    print("[DEBUG] resume_marketdata route called")
    global MARKETDATA_PAUSED
    MARKETDATA_PAUSED = False
    result = dc_resume()
    print(f"[DEBUG] dc_resume() returned: {result}")
    return redirect(url_for('dashboard'))

@app.route('/reset_demo', methods=['POST'])
def reset_demo():
    print("[DEBUG] reset_demo route called")
    order_book.trades.clear()
    order_book.bids.clear()
    order_book.asks.clear()
    scoring.pnl.clear()
    scoring.trades.clear()
    result = dc_reset()
    print(f"[DEBUG] dc_reset() returned: {result}")
    return redirect(url_for('dashboard'))

@app.route('/api/leaderboard')
def api_leaderboard():
    return jsonify(scoring.get_leaderboard())

@app.route('/api/trades')
def api_trades():
    return jsonify(order_book.get_trades())

@app.route('/api/bot_output')
def api_bot_output():
    try:
        log_path = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'bot_output.log')
        with open(log_path, 'r') as f:
            lines = f.readlines()[-30:]  # Show last 30 lines
        return jsonify({'lines': lines})
    except Exception as e:
        return jsonify({'lines': [f"Error: {e}\n"]})

@app.route('/set_feature', methods=['POST'])
def set_feature():
    print("[DEBUG] set_feature route called")
    global features
    features['clock_sync_error'] = float(request.form.get('clock_sync_error', features['clock_sync_error']))
    features['jasper_fairness_window'] = float(request.form.get('jasper_fairness_window', features['jasper_fairness_window']))
    features['jasper_hold_release'] = 'jasper_hold_release' in request.form
    features['dbo_logical_clocks'] = 'dbo_logical_clocks' in request.form
    print(f"[DEBUG] Features updated: {features}")
    try:
        resp1 = requests.post('http://localhost:5005/api/set_clock_sync_error', json={'error': features['clock_sync_error']})
        print(f"[DEBUG] set_clock_sync_error resp: {resp1.status_code}")
    except Exception as e:
        print(f"[WARN] Could not update CloudEx clock sync: {e}")
    try:
        resp2 = requests.post('http://localhost:5006/api/set_hold_release', json={'enabled': features['jasper_hold_release']})
        print(f"[DEBUG] set_hold_release resp: {resp2.status_code}")
    except Exception as e:
        print(f"[WARN] Could not update Jasper features: {e}")
    try:
        resp3 = requests.post('http://localhost:5007/api/set_logical_clocks', json={'enabled': features['dbo_logical_clocks']})
        print(f"[DEBUG] set_logical_clocks resp: {resp3.status_code}")
    except Exception as e:
        print(f"[WARN] Could not update DBO logical clocks: {e}")
    return redirect(url_for('dashboard'))

@app.route('/start_competition', methods=['POST'])
def start_competition():
    try:
        print("[DEBUG] start_competition route called")
        global competition_running
        competition_running = True

        print("[DEBUG] About to import start_bots")
        from scripts.traffic_generator import start_bots
        print("[DEBUG] Imported start_bots, about to start thread")
        threading.Thread(target=start_bots, daemon=True).start()
        print("[DEBUG] Thread started, about to reset order book")
        order_book.reset()
        print("[DEBUG] Competition started: bots launched, order book reset")
        return redirect(url_for('dashboard'))
    except Exception as e:
        import traceback
        print("[ERROR] Exception in start_competition:", e)
        traceback.print_exc()
        return "Internal Server Error: " + str(e), 500

@app.route('/stop_competition', methods=['POST'])
def stop_competition():
    print("[DEBUG] stop_competition route called")
    global competition_running
    competition_running = False
    print("Competition stopped by user.")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=False)
