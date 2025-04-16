"""
Sample Trading Bot
- Connects to the exchange API
- Submits random buy/sell orders
"""
import random
import time
from bots.bot_interface import TradingBotBase

class SampleBot(TradingBotBase):
    def run(self):
        for _ in range(10):
            side = random.choice(['buy', 'sell'])
            price = round(random.uniform(99, 101), 2)
            qty = random.randint(1, 10)
            print(f"Submitting {side} order: {qty}@{price}")
            resp = self.submit_order(side, price, qty)
            print("Response:", resp)
            time.sleep(1)

if __name__ == '__main__':
    bot = SampleBot(trader_id='bot1')
    bot.run()
