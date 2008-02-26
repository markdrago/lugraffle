#!/usr/bin/env python
#Licensed under the MIT license
#Copyright (c) 2007, 2008 Mark Drago <markdrago@gmail.com>

import logging, sys
from twisted.internet.protocol import DatagramProtocol
from socket import *

#import reactor stuff, tell it to use the glib2 main loop for dbus support
from twisted.internet import glib2reactor
glib2reactor.install()
from twisted.internet import reactor

#import our stuff
import utils
from protocol import *
from lr_model import *

class LugRaffle():
    def __init__(self):
	logging.basicConfig(level=logging.DEBUG,
			    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
			    datefmt='%H:%M:%S',
			    stream=sys.stderr)
    	self.logger = logging.getLogger('LR.LugRaffle')
	self.model = LRModel()
	self.client = LRClient(1234, self.model)
	self.server = LRServer(1234, self.model)

    def main(self):
	reactor.run()

#class that announces things to the network
class LRClient:
    def __init__(self, port, model):
	self.logger = logging.getLogger('LR.LRClient')
	self.port = port
	self.model = model
	self.model.register_listener('net', self.announce_change, True)

    def announce_change(self, item, entry):
	self.logger.info("announcing %s --> %s" % (item, entry))

#define what we should do when we receive a packet
class LRServer(DatagramProtocol):
    def __init__(self, port, model):
	self.model = model
	self.logger = logging.getLogger('LR.LRServer')
	reactor.listenUDP(port, self)

    def startProtocol(self):
	self.sendsocket = socket(AF_INET, SOCK_DGRAM)
	self.sendsocket.bind(('', 0))
	self.sendsocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	self.local_ip_list = utils.get_local_ipv4_addresses()

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

#start listening for connections on our udp port
if __name__ == '__main__':
    lr = LugRaffle()
    lr.main()
