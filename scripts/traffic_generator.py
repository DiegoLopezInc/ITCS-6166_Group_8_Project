#!/usr/bin/env python
"""
Mini-Project: Multicast Optimization for SDN in Financial Exchanges
Traffic Generator for financial data packets
"""

import random
import socket
import struct
import time
import argparse
import threading
import logging

logging.basicConfig(filename='/app/scripts/bot_output.log',
                    format='[BOT %(threadName)s] %(message)s',
                    level=logging.INFO)

class FinancialTrafficGenerator:
    """
    Generate financial exchange traffic for testing multicast implementations
    - Creates simulated stock price updates
    - Supports multicast transmission
    """
    
    def __init__(self, multicast_ip='224.0.0.10', port=5007):
        """Initialize the traffic generator"""
        self.multicast_ip = multicast_ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # Set the time-to-live for messages
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        
        # List of stock symbols for simulation
        self.stock_symbols = ['AAPL', 'MSFT', 'AMZN', 'GOOG', 'META', 'TSLA', 'NVDA']
        
        print(f"Financial Traffic Generator initialized - Multicast IP: {multicast_ip}, Port: {port}")
    
    def generate_stock_update(self, size_bytes=100):
        """
        Generate a simulated stock price update packet
        
        Args:
            size_bytes: Size of the packet in bytes
        
        Returns:
            Byte string containing stock update data
        """
        # Select a random stock symbol
        symbol = random.choice(self.stock_symbols)
        
        # Generate a random price (between $50 and $1000)
        price = random.uniform(50.0, 1000.0)
        
        # Generate a random volume
        volume = random.randint(1, 1000)
        
        # Timestamp
        timestamp = time.time()
        
        # Create the stock update header
        header = f"{symbol},{price:.2f},{volume},{timestamp}"
        
        # Pad to reach the requested size
        padding_size = max(0, size_bytes - len(header))
        padding = 'X' * padding_size
        
        # Return the complete message
        return (header + padding).encode('utf-8')
    
    def send_updates(self, count, rate, size_bytes=100):
        """
        Send a series of stock updates to the multicast group
        
        Args:
            count: Number of updates to send
            rate: Updates per second
            size_bytes: Size of each update in bytes
        """
        interval = 1.0 / rate
        
        print(f"Sending {count} stock updates at {rate} updates/second ({size_bytes} bytes each)...")
        
        for i in range(count):
            # Generate and send the update
            update_data = self.generate_stock_update(size_bytes)
            self.sock.sendto(update_data, (self.multicast_ip, self.port))
            
            # Log progress periodically
            if (i + 1) % 10 == 0 or i == 0 or i == count - 1:
                print(f"Sent update {i+1}/{count}")
            
            # Sleep to maintain the desired rate
            time.sleep(interval)
        
        print(f"Completed sending {count} updates")
    
    def close(self):
        """Close the socket"""
        self.sock.close()

def start_bots():
    """
    Start 4 traffic generator bots with random rates and message sizes.
    """
    rates = [10, 100, 200]
    sizes = [10, 100, 1000]
    bot_threads = []
    for i in range(4):
        rate = random.choice(rates)
        size = random.choice(sizes)
        count = 100  # Number of updates per bot
        def bot_task(rate=rate, size=size, count=count):
            gen = FinancialTrafficGenerator(MULTICAST_GRP, MULTICAST_PORT)
            try:
                logging.info(f"Bot starting: rate={rate}, size={size}, count={count}")
                gen.send_updates(count=count, rate=rate, size_bytes=size)
                logging.info(f"Bot finished: rate={rate}, size={size}, count={count}")
            finally:
                gen.close()
        t = threading.Thread(target=bot_task, daemon=True)
        t.start()
        bot_threads.append(t)
    print(f"[DEBUG] Started 4 bots with random rates and sizes.")
    # Optionally join bots if you want to wait for completion
    # for t in bot_threads:
    #     t.join()

def main():
    """Main function for standalone usage"""
    parser = argparse.ArgumentParser(description='Financial Exchange Traffic Generator')
    parser.add_argument('--count', type=int, default=100, help='Number of updates to send')
    parser.add_argument('--rate', type=float, default=10.0, help='Updates per second')
    parser.add_argument('--size', type=int, default=100, help='Size of each update in bytes')
    parser.add_argument('--ip', type=str, default='224.0.0.10', help='Multicast IP address')
    parser.add_argument('--port', type=int, default=5007, help='UDP port')
    
    args = parser.parse_args()
    
    generator = FinancialTrafficGenerator(args.ip, args.port)
    try:
        generator.send_updates(args.count, args.rate, args.size)
    finally:
        generator.close()

# Market Data Broadcaster for SDN Multicast Demo
MULTICAST_GRP = '224.1.1.1'
MULTICAST_PORT = 5007

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    ttl = 2
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    for i in range(100):
        price = round(100 + random.uniform(-1, 1), 2)
        msg = f"TICKER,PRICE,{price},SEQ,{i}"
        sock.sendto(msg.encode(), (MULTICAST_GRP, MULTICAST_PORT))
        print(f"Market data sent: {msg}")
        time.sleep(0.5)
    start_bots()
    main()
