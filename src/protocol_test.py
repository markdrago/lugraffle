#!/usr/bin/env python
#Licensed under the MIT license
#Copyright (c) 2007 Mark Drago <markdrago@gmail.com>

from protocol import *

class LRPacketTest():
    'Class to test the LRPacket class'

    def __init__(self):
        pass

    def run_test(self):
        print 'Testing RAFFLE_NODE_DISCOVER'
        packet_node_discover = LRPacket('LRP100;')
	print
        print 'Testing RAFFLE_NODE_FOUND'
	packet_node_found = LRPacket("LRP101;19;0;13;Mark's Laptop;")
	print
	try:
	    packet_node_found2 = LRPacket("LRP101;26;1;13;Mark's Laptop;4;Jeff;")
	except LRPacketError, (errstr):
	    print "Error in Packet: %s" % errstr
	    
	print
	packet_node_found3 = LRPacket("LRP101;145;0;13;Mark's Laptop;1;13;Mark's Laptop;4;Jeff;1;13;Mark's Laptop;14;Chris Mcnamara;0;22;Asterisk in a Nutshell;1;22;Asterisk in a Nutshell;4;Jeff;")
	print

if __name__ == '__main__':
    tester = LRPacketTest()
    tester.run_test()
