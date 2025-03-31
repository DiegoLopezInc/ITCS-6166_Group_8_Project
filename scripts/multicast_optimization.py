# Multicast Optimization Script
# This script implements Jasper's multicast tree algorithm.

# TODO: Implement multicast optimization

# IDEA: Create a publisher node that sends data to relay proxies
# which then forward the data to subscribers  

# Imports

import time
import socket
import struct
import threading

# Multicast Configuration
MULTICAST_GROUP = '224.1.1.1' # Choose actual IP
PORT = 5007 # Choose actual port
TTL = 2 # Time-To-Live for Packets

# Publisher - This class will simply send some market data message
# out to the multicast address, where proxies will be listening
class Publisher:
    def __init__(self, address, port):
        # Creates socket using IPv4 addresses, UDP, and sets TTL to 2
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL)
        self.group = (address, port)

    def send_data(self):
        # Constantly sends "Market Data" (Aka time) updates out to the multicast group
        while True:
            message = f"Market Data Update: {time.time()}"
            self.sock.sendto(message.encode(), self.group)
            print(f"[Publisher] Sent: {message}")
            time.sleep(2)

# Proxy Node - This class acts as proxy nodes that will listen in on the address
# that the publisher is sending data to and will then relay this data to the address
# that the subscribers are listening to
class ProxyNode:
    def __init__(self, address, port):
        # Create socket using IPv4 address, UDP, and allow multiple processes to reuse the same address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind the socket to listen to the multicast group
        self.group = (address, port)
        self.socket.bind(self.group)
        # Convert group address into binary
        mreq = struct.pack("4sl", socket.inet_aton(address), socket.INADDR_ANY)
        # Join the multicast group as a listener
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def forward_data(self):
        # Constantly wait and receive data from socket and then log it
        while True:
            data, _ = self.socket.recvfrom(1024)
            print(f"[Relay] Forwarding: {data.decode()}")

            # Create new UDP socket for forwarding to new multicast group
            forward_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            forward_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL)
            new_group = ('224.1.1.2', PORT)
            forward_socket.sendto(data, new_group)
            forward_socket.close()

# Subscriber - Listens for message at the address that the proxies will be
# publishing to
class Subscriber:
    def __init__(self, address, port):
        # Create UDP socket that uses IPv4 and allows addresses to be reused
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind the socket to listen to the multicast group
        group = (address, port)
        self.socket.bind(group)
        # Convert address to binary and add the process to the multicast group
        mreq = struct.pack("4sl", socket.inet_aton(address), socket.INADDR_ANY)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def receive_data(self):
        while True:
            data, _ = self.socket.recvfrom(1024)
            print(f"[Subscriber] Received: {data.decode()}")

# Creates 1 publisher, 1 Proxy Node, and 1 Subscriber (to make sure this works)
if __name__ == "__main__":
    threading.Thread(target=Publisher(MULTICAST_GROUP, PORT).send_data, daemon=True).start()
    threading.Thread(target=ProxyNode(MULTICAST_GROUP, PORT).forward_data, daemon=True).start()
    threading.Thread(target=Subscriber(MULTICAST_GROUP, PORT).receive_data, daemon=True).start()