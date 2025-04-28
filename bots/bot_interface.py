"""
Bot SDK: Interface for connecting to the exchange API
"""
import requests
import time
import os

class TradingBotBase:
    def __init__(self, trader_id, api_url=None):
        self.trader_id = trader_id
        self.api_url = api_url or os.environ.get('EXCHANGE_API_URL', 'http://localhost:5001')

    def submit_order(self, side, price, qty):
        order_id = f"{self.trader_id}-{int(time.time()*1000)}"
        payload = {
            'order_id': order_id,
            'trader_id': self.trader_id,
            'side': side,
            'price': price,
            'qty': qty
        }
        try:
            resp = requests.post(f'{self.api_url}/submit_order', json=payload, timeout=3)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            print(f"Order submission failed: {e}")
            return {'status': 'error', 'reason': str(e)}

    def get_order_book(self):
        try:
            return requests.get(f'{self.api_url}/order_book', timeout=3).json()
        except requests.RequestException as e:
            print(f"Failed to fetch order book: {e}")
            return None

    def get_trades(self):
        try:
            return requests.get(f'{self.api_url}/trades', timeout=3).json()
        except requests.RequestException as e:
            print(f"Failed to fetch trades: {e}")
            return None
