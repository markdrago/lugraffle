#Licensed under the MIT license
#Copyright (c) 2007 Mark Drago <markdrago@gmail.com>

class LRPacket:
    """Class for parsing and creating packets for the Lug Raffle protocol"""
    def __init__(self, data):
        if data:
            self.parse_packet(data)

    def parse_packet(self, data):
	data = data.strip("\n")

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

	print "Received Packet: %s" % self.packet_type

	semicolon = data.find(';', 7)
	datasection = data[semicolon + 1:]

	if (self.packet_type == 'RAFFLE_NODE_DISCOVER' or
	    self.packet_type == 'RAFFLE_DRAWING_START'):
	    pass
	elif (self.packet_type == 'RAFFLE_DRAWING_RESPONSE' or
	      self.packet_type == 'RAFFLE_DRAWING_RESPONSE_HASH'):
	    self.content = datasection[:-1]
	    print "Found Content: %s" % self.content
	else:
	    (self.items, self.entries) = self.get_object_lists(datasection)

    def get_object_lists(self, data):
	items = []
	entries = []

	while len(data) > 0:
	    object_type = self.get_next_object_type(data)

	    if object_type == 'ITEM':
		(item, data) = self.get_object_piece(data[2:])
		items.append(item)
		print 'Found Item: %s' % item

	    elif object_type == 'ENTRY':
		(item, entry, data) = self.get_object_entry(data[2:])
		entry_found = (item, entry)
		entries.append(entry_found)
		print 'Found Entry: %s -> %s' % (item, entry)

	return (items, entries)

    def get_object_entry(self, data):
	#get the item and then get the entry
	(item, data) = self.get_object_piece(data)
	(entry, data) = self.get_object_piece(data)
	return (item, entry, data)

    def get_object_piece(self, data):
	#skip length and return what lies between the semicolons
	post_semi1 = data.find(';') + 1
	semi2 = data.find(';', post_semi1)
	return (data[post_semi1:semi2], data[semi2 + 1:])

    def get_next_object_type(self, data):
	if data[:2] == '0;':
	    return 'ITEM'
	elif data[:2] == '1;':
	    return 'ENTRY'
	else:
	    print "data: %s" % data
	    raise LRPacketError('Unknown LR Object Type')

class LRPacketError(Exception):
    """Base exception thrown due to packet errors."""
    pass
