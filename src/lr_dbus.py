#Licensed under the MIT license
#Copyright (c) 2008 Mark Drago <markdrago@gmail.com>

import dbus
import dbus.service
import dbus.glib
import utils
import logging
from lr_model import *

#network interface for lug raffle
class LRDBus(dbus.service.Object):
    def __init__(self, reactor):
	self.model = LRModel.get_model()
	self.model.register_listener('dbus', self.announce_change, True)
	self.logger = logging.getLogger('LR.LRDBus')
	self.bus = dbus.SessionBus()
	self.name = dbus.service.BusName('org.lilug.lugraffle')
	dbus.service.Object.__init__(self, self.bus, '/')

    def announce_change(self, item, entry):
	if entry is None:
	    self.item_added(item)
	else:
	    self.entry_added(item, entry)

    @dbus.service.signal(dbus_interface='org.lilug.lugraffle', signature='s')
    def item_added(self, item):
	self.logger.info("Sending DBus Signal for New Item: %s" % item)

    @dbus.service.signal(dbus_interface='org.lilug.lugraffle', signature='ss')
    def entry_added(self, item, entry):
	self.logger.info("Sending DBus Signal for New Entry: %s, %s" % (item, entry))

    @dbus.service.method('org.lilug.lugraffle', in_signature='s')
    def add_item(self, item):
	self.model.add_item('dbus', item)

    @dbus.service.method('org.lilug.lugraffle', in_signature='ss')
    def add_entry(self, item, entry):
	self.model.add_entry('dbus', item, entry)
