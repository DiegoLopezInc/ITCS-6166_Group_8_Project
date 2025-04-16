"""
Bot SDK: Interface for connecting to the exchange API
"""
import requests
import time

class TradingBotBase:
    def __init__(self, trader_id, api_url='http://localhost:5001'):
        self.trader_id = trader_id
        self.api_url = api_url

    def submit_order(self, side, price, qty):
        order_id = f"{self.trader_id}-{int(time.time()*1000)}"
        payload = {
            'order_id': order_id,
            'trader_id': self.trader_id,
            'side': side,
            'price': price,
            'qty': qty
        }
        resp = requests.post(f'{self.api_url}/submit_order', json=payload)
        return resp.json()

    def get_order_book(self):
        return requests.get(f'{self.api_url}/order_book').json()

    def get_trades(self):
        return requests.get(f'{self.api_url}/trades').json()
