#!/usr/bin/env python
"""
Mini-Project: Multicast Optimization for SDN in Financial Exchanges
Basic SDN Controller using Ryu
"""

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ether_types, ipv4, udp

class FinancialExchangeController(app_manager.RyuApp):
    """
    Basic SDN controller for financial exchange simulation
    - Handles basic packet forwarding
    - Supports multicast operations
    """
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(FinancialExchangeController, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        # Track multicast groups
        self.multicast_groups = {}
        # CloudEx: Simulated clock offsets per host (for fairness experiments)
        self.clock_offsets = {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0}  # ms offset per port
        # CloudEx: Artificial delay (ms) for fairness tuning
        self.artificial_delay_ms = 0.0
        self.logger.info("Financial Exchange Controller started")

    def set_clock_offset(self, port, offset_ms):
        """Set simulated clock offset for a port (CloudEx)"""
        self.clock_offsets[port] = offset_ms
        self.logger.info(f"Set clock offset for port {port}: {offset_ms} ms")

    def set_artificial_delay(self, delay_ms):
        """Set artificial delay for multicast (CloudEx)"""
        self.artificial_delay_ms = delay_ms
        self.logger.info(f"Set artificial multicast delay: {delay_ms} ms")

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

        # Check if this is a multicast packet
        if dst.startswith('01:00:5e'):  # IPv4 multicast MAC prefix
            self.handle_multicast(msg, datapath, in_port, pkt)
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

    def handle_multicast(self, msg, datapath, in_port, pkt):
        """Handle multicast packets - basic implementation with CloudEx-inspired delay and clock offset"""
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        dpid = datapath.id
        actions = []
        for port in range(1, 5):  # Assuming 4-node star topology
            if port != in_port:
                # CloudEx: Add artificial delay and simulated clock offset
                total_delay = self.artificial_delay_ms + self.clock_offsets.get(port, 0.0)
                if total_delay > 0:
                    import time
                    time.sleep(total_delay / 1000.0)  # convert ms to s
                actions.append(parser.OFPActionOutput(port))
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data
        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                 in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)
        self.logger.info(f"Multicast packet forwarded to all ports from {in_port} with CloudEx delay/offsets")
