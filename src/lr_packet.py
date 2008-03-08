#Licensed under the MIT license
#Copyright (c) 2007 Mark Drago <markdrago@gmail.com>

import logging

#create logger
logger = logging.getLogger('LR.LRPacket')

class LRPacket:
    """Class for parsing and creating packets for the Lug Raffle protocol"""
    def __init__(self, data=None):
	self.items = []
	self.entries = []
        if data:
            self.parse_packet(data)

    def set_type(self, packet_type):
	self.packet_type = packet_type

    def add_object(self, item, entry):
	obj = (item, entry)
	self.entries.append(obj)

    def produce_packet(self):
	data = 'LRP1'

	if self.packet_type == 'RAFFLE_NODE_DISCOVER':
	    data += '00;'
	elif self.packet_type == 'RAFFLE_NODE_FOUND':
	    data += '01;'
	elif self.packet_type == 'RAFFLE_OBJECT_ADD':
	    data += '10;'
	elif self.packet_type == 'RAFFLE_DRAWING_START':
	    data += '20;'
	elif self.packet_type == 'RAFFLE_DRAWING_RESPONSE_HASH':
	    data += '21;'
	elif self.packet_type == 'RAFFLE_DRAWING_RESPONSE':
	    data += '22;'
	elif self.packet_type == 'RAFFLE_DRAWING_RESULT':
	    data += '23;'
	else:
	    raise LRPacketError('Unidentified Packet Type')

	if (len(self.entries) > 0):
	    data += self.get_lists_as_data(self.entries)

	return data

    def get_lists_as_data(self, entries):
	data = ''
	for entry in entries:
	    if (entry[1] is None):
		data += '0;' + str(len(entry[0])) + ';' + entry[0] + ';'
	    else:
		data += '1;' + str(len(entry[0])) + ';' + entry[0] + ';'
		data += str(len(entry[1])) + ';' + entry[1] + ';'

	data = str(len(data)) + ';' + data
	return data

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

	logger.info("Received Packet: %s" % self.packet_type)

	semicolon = data.find(';', 7)
	datasection = data[semicolon + 1:]

	if (self.packet_type == 'RAFFLE_NODE_DISCOVER' or
	    self.packet_type == 'RAFFLE_DRAWING_START'):
	    pass
	elif (self.packet_type == 'RAFFLE_DRAWING_RESPONSE' or
	      self.packet_type == 'RAFFLE_DRAWING_RESPONSE_HASH'):
	    self.content = datasection[:-1]
	    logger.info("Found Content: %s" % self.content)
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
		logger.info('Found Item: %s' % item)

	    elif object_type == 'ENTRY':
		(item, entry, data) = self.get_object_entry(data[2:])
		entry_found = (item, entry)
		entries.append(entry_found)
		logger.info('Found Entry: %s -> %s' % (item, entry))

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
	    raise LRPacketError('Unknown LR Object Type')

class LRPacketError(Exception):
    """Base exception thrown due to packet errors."""
    pass
