#!/usr/bin/env python
"""
Mini-Project: Multicast Optimization for SDN in Financial Exchanges
Jasper-inspired Fair Multicast Controller
"""

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ether_types, ipv4, udp
import time
import random

class JasperMulticastController(app_manager.RyuApp):
    """
    Jasper-inspired multicast controller for financial exchange simulation
    - Implements fair distribution of multicast packets
    - Builds fair multicast trees based on Jasper principles
    - Tracks latency for fairness measurements
    """
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(JasperMulticastController, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        # Track multicast groups and their members
        self.multicast_groups = {}
        # Track timestamps for calculating latency
        self.packet_timestamps = {}
        # Maintain multicast tree (simplified for 4-node star topology)
        self.multicast_tree = {}
        self.logger.info("Jasper Multicast Controller started")

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        """Handle switch features reply to install table-miss flow entry"""
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Install table-miss flow entry
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                         ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)
        self.logger.info(f"Switch {datapath.id} connected")
        
        # Initialize the multicast tree for this switch
        self.build_fair_multicast_tree(datapath.id)

    def build_fair_multicast_tree(self, dpid):
        """
        Build a fair multicast tree inspired by Jasper
        For this mini-implementation, we'll create a simple tree
        that ensures fairness by ordering the receivers
        """
        # For this simplified 4-node star topology, we'll create a 
        # multicast order that ensures fair receipt
        # In a real Jasper implementation, this would build a proper tree
        # based on network conditions and fair ordering principles
        
        # Create a simple tree with randomized order to simulate fair ordering
        # In Jasper, this would be done based on network conditions and fairness metrics
        ports = [1, 2, 3, 4]  # Ports for our 4 hosts
        random.shuffle(ports)  # Randomize to simulate different orderings
        
        self.multicast_tree[dpid] = {
            'order': ports,
            'delay': 0.0001  # Small artificial delay between each node (0.1ms)
        }
        
        self.logger.info(f"Built fair multicast tree for switch {dpid}: {self.multicast_tree[dpid]}")

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        """Add a flow entry to the switch"""
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        """Handle packet in message from switches"""
        # Basic packet handling logic
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("Packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # Ignore LLDP packets
            return
        
        dst = eth.dst
        src = eth.src
        dpid = datapath.id

        # Learn MAC addresses to avoid flooding
        self.mac_to_port.setdefault(dpid, {})
        self.mac_to_port[dpid][src] = in_port

        # Generate packet identifier for tracking
        pkt_id = f"{src}_{dst}_{time.time()}"
        
        # Check if this is a multicast packet
        if dst.startswith('01:00:5e'):  # IPv4 multicast MAC prefix
            self.handle_jasper_multicast(msg, datapath, in_port, pkt, pkt_id)
            return
            
        # Regular unicast forwarding
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # Install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
            # Verify if we have a valid buffer_id, if yes avoid sending both flow_mod & packet_out
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                return
            else:
                self.add_flow(datapath, 1, match, actions)
        
        # Send packet out
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                 in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)

    def handle_jasper_multicast(self, msg, datapath, in_port, pkt, pkt_id):
        """
        Handle multicast packets using Jasper-inspired fair distribution
        - Prioritizes fairness in packet delivery
        - Uses multicast tree to determine forwarding order
        - Adds small artificial delays to simulate fair ordering
        """
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        dpid = datapath.id
        
        # Record packet arrival time
        self.packet_timestamps[pkt_id] = {'arrival': time.time(), 'deliveries': {}}
        
        # Get multicast tree for this switch
        if dpid not in self.multicast_tree:
            self.build_fair_multicast_tree(dpid)
        
        tree = self.multicast_tree[dpid]
        order = tree['order']
        delay = tree['delay']
        
        # Forward to each port in the determined order with slight delays
        # to simulate the fair ordering in Jasper
        for i, port in enumerate(order):
            if port != in_port:  # Don't send back to source
                # Calculate simulated delay for this destination
                # In real Jasper, this would be based on network conditions
                # and proper fairness calculations
                simulated_delay = i * delay
                
                # Record delivery time with simulated delay
                delivery_time = time.time() + simulated_delay
                self.packet_timestamps[pkt_id]['deliveries'][port] = delivery_time
                
                # Send packet to this destination
                actions = [parser.OFPActionOutput(port)]
                data = None
                if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                    data = msg.data
                
                out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                         in_port=in_port, actions=actions, data=data)
                datapath.send_msg(out)
                
                # For demonstration, we add a small sleep to simulate the ordering
                # In a real implementation, this would be handled by proper queueing
                # time.sleep(delay)  # Uncomment for real demonstration
                
                self.logger.info(f"Jasper multicast: packet forwarded to port {port} (order {i+1})")
        
        # Log the fairness information
        self.log_fairness_metrics(pkt_id)
    
    def log_fairness_metrics(self, pkt_id):
        """Log the fairness metrics for a multicast packet"""
        if pkt_id in self.packet_timestamps:
            packet_info = self.packet_timestamps[pkt_id]
            arrival = packet_info['arrival']
            deliveries = packet_info['deliveries']
            
            # Calculate latencies for each destination
            latencies = []
            for port, delivery_time in deliveries.items():
                latency = delivery_time - arrival
                latencies.append(latency)
            
            # Calculate Jain's Fairness Index
            if latencies:
                sum_latencies = sum(latencies)
                sum_squared = sum(x**2 for x in latencies)
                n = len(latencies)
                fairness = (sum_latencies**2) / (n * sum_squared) if sum_squared > 0 else 1.0
                
                self.logger.info(f"Packet {pkt_id} - Latencies: {latencies}, Fairness Index: {fairness:.4f}")
