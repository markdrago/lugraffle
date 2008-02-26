#!/usr/bin/env python
#Licensed under the MIT license
#Copyright (c) 2007, 2008 Mark Drago <markdrago@gmail.com>

import logging, sys

#import reactor stuff, tell it to use the glib2 main loop for dbus support
from twisted.internet import glib2reactor
glib2reactor.install()
from twisted.internet import reactor

#import our stuff
from lr_model import *
from lr_net import *

class LugRaffle():
    def __init__(self):
	logging.basicConfig(level=logging.DEBUG,
			    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
			    datefmt='%H:%M:%S',
			    stream=sys.stderr)
    	self.logger = logging.getLogger('LR.LugRaffle')
	self.model = LRModel()
	self.server = LRServer(1234, self.model, reactor)

    def main(self):
	reactor.run()

#start listening for connections on our udp port
if __name__ == '__main__':
    lr = LugRaffle()
    lr.main()
