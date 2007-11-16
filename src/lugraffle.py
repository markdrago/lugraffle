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
import utils, lr_model
from protocol import *

#create logger
logger = logging.getLogger('LR.LRServer')

#define what we should do when we receive a packet
class LRServer(DatagramProtocol):
    sendport = 1234
    sendhost = "<broadcast>"

    def startProtocol(self):
        self.sendsocket = socket(AF_INET, SOCK_DGRAM)
        self.sendsocket.bind(('', 0))
        self.sendsocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.local_ip_list = utils.get_local_ipv4_addresses()

    def datagramReceived(self, data, (host, port)):
        #we should not respond to packets that we sent ourselves
        if host in self.local_ip_list:
	    logger.debug("Not replying to packet from self")
	    return

        logger.info("Received packet from %s:%d" % (host, port))
	try:
	    packet = LRPacket(data)
	except LRPacketError, (errstr):
	    logger.warning("Error while parsing packet: %s" % errstr)
	    return
	    
        self.sendsocket.sendto(data, (self.sendhost, self.sendport))


def start_logger():
    logging.basicConfig(level=logging.DEBUG,
			format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
			datefmt='%H:%M:%S',
			stream=sys.stderr)

#start listening for connections on our udp port
if __name__ == '__main__':
    start_logger()
    reactor.listenUDP(1234, LRServer())
    reactor.run()
