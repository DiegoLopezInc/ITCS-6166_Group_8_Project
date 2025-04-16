"""
Reactive Trading Bot Example
- Listens to multicast market data
- Trades based on price movements
"""
import socket
import struct
import time
from bots.bot_interface import TradingBotBase

MULTICAST_GRP = '224.1.1.1'
MULTICAST_PORT = 5007

class ReactiveBot(TradingBotBase):
    def listen_and_trade(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', MULTICAST_PORT))
        mreq = struct.pack('4sl', socket.inet_aton(MULTICAST_GRP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        last_price = None
        for _ in range(20):
            data, _ = sock.recvfrom(1024)
            msg = data.decode()
            try:
                price = float(msg.split(',')[2])
            except Exception:
                continue
            print(f"Received market data: {msg}")
            if last_price is not None:
                if price > last_price:
                    print("Price up: submitting buy order")
                    self.submit_order('buy', price, 1)
                elif price < last_price:
                    print("Price down: submitting sell order")
                    self.submit_order('sell', price, 1)
            last_price = price
            time.sleep(1)

if __name__ == '__main__':
    bot = ReactiveBot(trader_id='reactive1')
    bot.listen_and_trade()
