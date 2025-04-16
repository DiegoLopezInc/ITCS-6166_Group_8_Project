#!/usr/bin/env python
"""
Mini-Project: Multicast Optimization for SDN in Financial Exchanges
DBO-inspired Fair Multicast Controller (Clockless Fairness)
"""

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ether_types, ipv4, udp
import time

class DBOMulticastController(app_manager.RyuApp):
    """
    DBO-inspired multicast controller for financial exchange simulation
    - Implements delivery-clock-based fairness (no clock sync required)
    - Tracks logical delivery clocks per receiver
    - Logs post-hoc fairness metrics
    """
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(DBOMulticastController, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.multicast_groups = {}
        # Track per-packet delivery times (for fairness calculation)
        self.packet_deliveries = {}
        self.logger.info("DBO Multicast Controller started")

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                         ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)
        self.logger.info(f"Switch {datapath.id} connected")

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
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
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            return
        dst = eth.dst
        src = eth.src
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})
        self.mac_to_port[dpid][src] = in_port
        # Multicast detection (IPv4 multicast MAC)
        if dst.startswith('01:00:5e'):
            self.handle_dbo_multicast(msg, datapath, in_port, pkt)
            return
        # Unicast
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD
        actions = [parser.OFPActionOutput(out_port)]
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                return
            else:
                self.add_flow(datapath, 1, match, actions)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data
        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                 in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)

    def handle_dbo_multicast(self, msg, datapath, in_port, pkt):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        dpid = datapath.id
        # For DBO: deliver to all ports except source, record delivery times
        pkt_id = hash((time.time(), msg.data[:8]))  # crude unique id
        delivery_times = {}
        for port in range(1, 5):  # 4-node star
            if port != in_port:
                actions = [parser.OFPActionOutput(port)]
                data = None
                if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                    data = msg.data
                out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                         in_port=in_port, actions=actions, data=data)
                datapath.send_msg(out)
                delivery_times[port] = time.time()
        # Store delivery times for post-hoc fairness
        self.packet_deliveries[pkt_id] = delivery_times
        self.log_dbo_fairness(pkt_id)

    def log_dbo_fairness(self, pkt_id):
        if pkt_id in self.packet_deliveries:
            deliveries = self.packet_deliveries[pkt_id]
            if len(deliveries) < 2:
                return
            times = list(deliveries.values())
            min_time = min(times)
            logical_clocks = [t - min_time for t in times]
            fairness = 1.0
            if logical_clocks:
                sum_lat = sum(logical_clocks)
                sum_sq = sum(x**2 for x in logical_clocks)
                n = len(logical_clocks)
                fairness = (sum_lat**2) / (n * sum_sq) if sum_sq > 0 else 1.0
                fairness_window = max(logical_clocks) - min(logical_clocks) if len(logical_clocks) > 1 else 0.0
                self.logger.info(f"DBO Packet {pkt_id} - Logical Clocks: {[round(x*1000,2) for x in logical_clocks]}, Fairness Index: {fairness:.4f}, Fairness Window: {fairness_window*1000:.2f} ms")
