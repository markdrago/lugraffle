#Licensed under the MIT license
#Copyright (c) 2007 Mark Drago <markdrago@gmail.com>

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
	    print 'data: %s' % data
	    object_type = self.get_next_object_type(data)
	    if object_type == 'ITEM':
		item_found = self.get_entry_piece(data[2:])
		print 'Found Item: %s' % item_found
	    elif object_type == 'ENTRY':
		(item, entry) = self.get_object_entry(data[2:])
		print 'Found Entry: %s -> %s' % (item, entry)

        def get_object_entry(self, data):
	    item = self.get_entry_piece(data)
	    semi = data.find(';') + 1
	    semi = data.find(';', semi) + 1
	    entry = self.get_entry_piece(data[semi:])
	    return (item, entry)

        def get_entry_piece(self, data):
	    #skip length
	    post_semi1 = data.find(';') + 1
	    semi2 = data.find(';', post_semi1)
	    return data[post_semi1:semi2]

        def get_next_object_type(self, data):
	    print 'Getting Object Type'
	    if data[:2] == '0;':
		return 'ITEM'
	    elif data[:2] == '1;':
		return 'ENTRY'
	    else:
		raise LRPacketError('Unknown Object Type')

class LRPacketError(Exception):
    """Base exception thrown due to packet errors."""
    pass
