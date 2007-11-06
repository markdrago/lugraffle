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

        print 'Testing RAFFLE_NODE_FOUND'
	packet_node_found = LRPacket("LRP101;45;0;13;Mark's Laptop;")
        packet_node_found2 = LRPacket("LRP101;45;1;13;Mark's Laptop;4;Jeff;")

if __name__ == '__main__':
    tester = LRPacketTest()
    tester.run_test()
