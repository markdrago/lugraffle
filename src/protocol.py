class LRPacket:
	"""Class for parsing and creating packets for the Lug Raffle protocol"""
	def __init__(self, data):
		if data:
			self.parse_packet(data)

	def parse_packet(self, data):
		if data[:4] != 'LRP1':
			raise LRPacketError('Not a LugRaffle Packet')

		typetag = data[4:7]
		if typetag == '00;':
			self.packet_type = 'RAFFLE_NODE_DISCOVER'
		elif typetag == '01;':
			self.packet_type = 'RAFFLE_NODE_FOUND'
		elif typetag == '10;':
			self.packet_type = 'RAFFLE_OBJECT_ADD'
		elif typetag == '20;':
			self.packet_type = 'RAFFLE_DRAWING_START'
		elif typetag == '21;':
			self.packet_type = 'RAFFLE_DRAWING_RESPONSE_HASH'
		elif typetag == '22;':
			self.packet_type = 'RAFFLE_DRAWING_RESPONSE'
		elif typetag == '23;':
			self.packet_type = 'RAFFLE_DRAWING_RESULT'
		else:
			raise LRPacketError('Unidentified Packet Type')
		
		semicolon = data.find(';', 7)
		
		#a bit of magic here calls the right method
		methodname = 'parse_packet_' + self.packet_type.lower()
		method = getattr(self, methodname)
		method(data[semicolon + 1:])
	
	def parse_packet_raffle_node_discover(self, data):
		print 'Received Packet: RAFFLE_NODE_DISCOVER'
	
	def parse_packet_raffle_node_found(self, data):
		print 'Received Packet: RAFFLE_NODE_FOUND'
		print "data: %s" % data
	
class LRPacketError(Exception):
	"""Base exception thrown due to packet errors."""
	pass

