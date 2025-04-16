#!/usr/bin/env python
"""
Mini-Project: Multicast Optimization for SDN in Financial Exchanges
4-Node Star Topology Implementation
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink

class StarTopo(Topo):
    """
    Simple 4-node star topology:
        - 1 central switch (s1)
        - 4 hosts (h1, h2, h3, h4)
        - All hosts connected to central switch
    """
    def build(self):
        # Add central switch
        s1 = self.addSwitch('s1')
        
        # Add 4 hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        
        # Add links with high bandwidth and low latency to simulate financial exchange
        self.addLink(h1, s1, bw=10, delay='1ms')  # 10 Gbps, 1ms delay
        self.addLink(h2, s1, bw=10, delay='1ms')
        self.addLink(h3, s1, bw=10, delay='1ms')
        self.addLink(h4, s1, bw=10, delay='1ms')

def createNetwork():
    """Create and configure the network"""
    topo = StarTopo()
    
    # Create network with Ryu remote controller
    net = Mininet(
        topo=topo,
        controller=lambda name: RemoteController(name, ip='127.0.0.1', port=6633),
        switch=OVSKernelSwitch,
        link=TCLink,
        autoSetMacs=True
    )
    
    # Start the network
    net.start()
    
    info('*** Network started\n')
    info('*** Type "exit" to shut down the network\n')
    
    # Run CLI
    CLI(net)
    
    # Clean up
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    createNetwork()
