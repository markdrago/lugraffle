#!/usr/bin/env python
#Licensed under the MIT license
#Copyright (c) 2007 Mark Drago <markdrago@gmail.com>

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

logging.basicConfig(level=logging.DEBUG,
		    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
		    datefmt='%H:%M:%S',
		    stream=sys.stderr)

class LugRaffle():
    def __init__(self):
    	self.logger = logging.getLogger('LR.LugRaffle')
	self.model = LRModel()

    def main(self):
	reactor.listenUDP(1234, LRServer(self.model))
	reactor.run()

#define what we should do when we receive a packet
class LRServer(DatagramProtocol):
    sendport = 1234
    sendhost = "<broadcast>"

    def __init__(self, model):
	self.model = model
	self.logger = logging.getLogger('LR.LRServer')

    def startProtocol(self):
	self.sendsocket = socket(AF_INET, SOCK_DGRAM)
	self.sendsocket.bind(('', 0))
	self.sendsocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	self.local_ip_list = utils.get_local_ipv4_addresses()

    def datagramReceived(self, data, (host, port)):
	#we should not respond to packets that we sent ourselves
	if host in self.local_ip_list:
	    self.logger.debug("Not replying to packet from self")
	    return
	
	self.logger.info("Received packet from %s:%d" % (host, port))
	try:
	    packet = LRPacket(data)
	except LRPacketError, (errstr):
	    self.logger.warning("Error while parsing packet: %s" % errstr)
	    return
	    
	self.sendsocket.sendto(data, (self.sendhost, self.sendport))

#start listening for connections on our udp port
if __name__ == '__main__':
    lr = LugRaffle()
    lr.main()
