#!/usr/bin/env python
#Licensed under the MIT license
#Copyright (c) 2007 Mark Drago <markdrago@gmail.com>

from protocol import *

class LRPacketTest():
    'Class to test the LRPacket class'

    def __init__(self):
        pass

    def run_test(self):
        print "\nTesting RAFFLE_NODE_DISCOVER"
	self.test_packet(True, 'LRP100;')

        print "\nTesting RAFFLE_NODE_FOUND"
	self.test_packet(True,"LRP101;19;0;13;Mark's Laptop;")
	self.test_packet(True,"LRP101;26;1;13;Mark's Laptop;4;Jeff;")
	self.test_packet(True,"LRP101;145;0;13;Mark's Laptop;1;13;Mark's Laptop;4;Jeff;1;13;Mark's Laptop;14;Chris Mcnamara;0;22;Asterisk in a Nutshell;1;22;Asterisk in a Nutshell;4;Jeff;")

	print "\nTesting RAFFLE_OBJECT_ADD"
	self.test_packet(True, "LRP110;24;1;13;Mark's Laptop;5;Chris;")
	
        print "\nTesting RAFFLE_DRAWING_START"
	self.test_packet(True, 'LRP120;')

	print "\nTesting RAFFLE_DRAWING_RESPONSE_HASH"
	self.test_packet(True, 'LRP121;41;0123456789abcdef0123456789abcdef01234567;')

	print "\nTesting RAFFLE_DRAWING_RESPONSE"
	self.test_packet(True, 'LRP122;7;123456;')

	print "\nTesting RAFFLE_DRAWING_RESULT"
	self.test_packet(True, "LRP123;27;1;13;Mark's Laptop;5;Chris;")

	print "\nTesting Bogus Packets"
	self.test_packet(False, 'Tom Stinks;')
	
    def test_packet(self, should_pass, data):
	try:
	    packet = LRPacket(data)
	except LRPacketError, (errstr):
	    if should_pass == False:
		print "Pass: Threw Exception Correctly: %s" % errstr
	    else:
		print "Fail: Threw Unexpected Exception: %s" % errstr
	    return

	print "Pass: Parsed Packet"

if __name__ == '__main__':
    tester = LRPacketTest()
    tester.run_test()
