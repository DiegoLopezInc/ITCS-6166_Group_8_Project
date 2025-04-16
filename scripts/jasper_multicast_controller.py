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
        # Jasper: Hold-and-release buffer (per-port)
        self.hold_release_buffer = {}
        # Jasper: Deadline (ms) for hold-and-release (can be dynamic)
        self.hold_release_deadline_ms = 1.0  # Default 1ms
        # Jasper: Enable dynamic tree reshuffling
        self.dynamic_tree = True
        self.logger.info("Jasper Multicast Controller started")

    def set_hold_release_deadline(self, deadline_ms):
        """Set hold-and-release deadline (ms) for all receivers"""
        self.hold_release_deadline_ms = deadline_ms
        self.logger.info(f"Set hold-and-release deadline: {deadline_ms} ms")

    def enable_dynamic_tree(self, enabled=True):
        self.dynamic_tree = enabled
        self.logger.info(f"Dynamic multicast tree reshuffling set to {enabled}")

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
        If dynamic_tree is enabled, reshuffle order each time.
        """
        ports = [1, 2, 3, 4]  # Ports for our 4 hosts
        if self.dynamic_tree:
            import random
            random.shuffle(ports)  # Randomize to simulate dynamic fairness
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
        - Implements hold-and-release: buffer delivery, then release after deadline
        """
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        dpid = datapath.id
        import time
        # Record packet arrival time
        self.packet_timestamps[pkt_id] = {'arrival': time.time(), 'deliveries': {}}
        # Get multicast tree for this switch
        if dpid not in self.multicast_tree or self.dynamic_tree:
            self.build_fair_multicast_tree(dpid)
        tree = self.multicast_tree[dpid]
        order = tree['order']
        delay = tree['delay']
        # Hold-and-release: buffer packets per port, release after deadline
        release_time = time.time() + (self.hold_release_deadline_ms / 1000.0)
        for i, port in enumerate(order):
            if port != in_port:
                # Buffer packet for port
                if port not in self.hold_release_buffer:
                    self.hold_release_buffer[port] = []
                self.hold_release_buffer[port].append((msg, datapath, in_port, parser, ofproto, pkt_id, release_time, i * delay))
        # Immediately schedule release (in real Jasper, would be event-driven)
        self.release_held_packets()
        self.log_fairness_metrics(pkt_id)

    def release_held_packets(self):
        """Release held packets after their hold-and-release deadline"""
        import time
        now = time.time()
        for port, pkts in list(self.hold_release_buffer.items()):
            new_pkts = []
            for (msg, datapath, in_port, parser, ofproto, pkt_id, release_time, extra_delay) in pkts:
                if now >= release_time:
                    # Apply extra delay for fair ordering
                    if extra_delay > 0:
                        time.sleep(extra_delay)
                    actions = [parser.OFPActionOutput(port)]
                    data = None
                    if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                        data = msg.data
                    out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                             in_port=in_port, actions=actions, data=data)
                    datapath.send_msg(out)
                    # Record delivery time
                    self.packet_timestamps[pkt_id]['deliveries'][port] = time.time()
                    self.logger.info(f"Jasper multicast: released packet to port {port}")
                else:
                    new_pkts.append((msg, datapath, in_port, parser, ofproto, pkt_id, release_time, extra_delay))
            if new_pkts:
                self.hold_release_buffer[port] = new_pkts
            else:
                del self.hold_release_buffer[port]

    def log_fairness_metrics(self, pkt_id):
        """Log the fairness metrics for a multicast packet, including fairness window"""
        if pkt_id in self.packet_timestamps:
            packet_info = self.packet_timestamps[pkt_id]
            arrival = packet_info['arrival']
            deliveries = packet_info['deliveries']
            latencies = []
            for port, delivery_time in deliveries.items():
                latency = delivery_time - arrival
                latencies.append(latency)
            fairness = 1.0
            if latencies:
                sum_latencies = sum(latencies)
                sum_squared = sum(x**2 for x in latencies)
                n = len(latencies)
                fairness = (sum_latencies**2) / (n * sum_squared) if sum_squared > 0 else 1.0
                fairness_window = max(latencies) - min(latencies) if len(latencies) > 1 else 0.0
                self.logger.info(f"Packet {pkt_id} - Latencies: {latencies}, Fairness Index: {fairness:.4f}, Fairness Window: {fairness_window*1000:.2f} ms")
