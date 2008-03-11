#!/usr/bin/env python
#Licensed under the MIT license
#Copyright (c) 2007, 2008 Mark Drago <markdrago@gmail.com>

import logging, sys

#import reactor stuff, tell it to use the glib2 main loop for dbus support
from twisted.internet import glib2reactor
glib2reactor.install()
from twisted.internet import reactor

#import our stuff
from lr_net import *
from lr_dbus import *

class LugRaffleDaemon():
    def __init__(self):
	logging.basicConfig(level=logging.DEBUG,
			    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
			    datefmt='%H:%M:%S',
			    stream=sys.stderr)
    	self.logger = logging.getLogger('LR.LugRaffleDaemon')
	self.net = LRNet(1234, reactor)
	self.bus = LRDBus(reactor)

    def main(self):
	reactor.run()

if __name__ == '__main__':
    lrd = LugRaffleDaemon()
    lrd.main()
