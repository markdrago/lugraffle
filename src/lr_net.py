import logging

from socket import *
from twisted.internet.protocol import DatagramProtocol

import lr_utils
from lr_packet import *
from lr_model import *
from lr_control import *

#network interface for lug raffle
class LRNet(DatagramProtocol):
    def __init__(self, port, reactor):
        self.port = port
        self.logger = logging.getLogger('LR.LRNet')
        self.model = LRModel.get_model()
        self.model.register_listener('net', self.announce_change, False)
        self.control = LRControl.get_control()
        self.control.register(self)
        reactor.listenUDP(self.port, self)

    def startProtocol(self):
        self.sendsocket = socket(AF_INET, SOCK_DGRAM)
        self.sendsocket.bind(('', 0))
        self.sendsocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.local_ip_list = lr_utils.get_local_ipv4_addresses()

    def datagramReceived(self, data, (host, port)):
        #we should not handle packets that we sent ourselves
        if host in self.local_ip_list:
            self.logger.debug("Not replying to packet from self")
            return
        
        self.logger.info("Received packet from %s:%d" % (host, port))
        try:
            packet = LRPacket(data)
        except LRPacketError, (errstr):
            self.logger.warning("Error while parsing packet: %s" % errstr)
            return
            
        #packet is changing things, tell the model about it
        if (packet.packet_type == 'RAFFLE_NODE_FOUND' or
            packet.packet_type == 'RAFFLE_OBJECT_ADD'):
            for item in packet.items:
                self.model.add_item('net', item)
            for entry in packet.entries:
                self.model.add_entry('net', entry[0], entry[1])

        self.model.dump_model_state()

    def announce_change(self, item, entry):
        packet = LRPacket()
        packet.set_type('RAFFLE_OBJECT_ADD')
        packet.add_object(item, entry)
        data = packet.produce_packet()

        self.logger.info("Sending Data: %s" % data)
        self.sendsocket.sendto(data, ('<broadcast>', self.port))

    def initiate_drawing_cb(self):
        self.logger.info("Initiating Drawing in Network")
